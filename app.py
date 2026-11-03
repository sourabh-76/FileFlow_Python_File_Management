from pathlib import Path
import streamlit as st
from datetime import datetime

# -------------------- Page setup --------------------
st.set_page_config(
    page_title="FileFlow | File Manager",
    page_icon="📁",
    layout="wide",
    initial_sidebar_state="expanded",
)

DATA_DIR = Path("project_files")
DATA_DIR.mkdir(exist_ok=True)

# -------------------- Styling --------------------
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700;800&family=Space+Grotesk:wght@500;600;700&display=swap');

    html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }
    .stApp {
        background:
          radial-gradient(circle at 85% 2%, rgba(99,102,241,.13), transparent 26%),
          radial-gradient(circle at 5% 30%, rgba(14,165,233,.09), transparent 25%),
          #0b1020;
        color: #eef2ff;
    }
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #111a31 0%, #0d1427 100%);
        border-right: 1px solid rgba(148,163,184,.14);
    }
    .block-container { padding-top: 2.2rem; max-width: 1400px; }
    h1, h2, h3 { font-family: 'Space Grotesk', sans-serif !important; }
    .hero {
        padding: 28px 32px; border-radius: 24px;
        background: linear-gradient(115deg, rgba(30,41,86,.96), rgba(22,35,65,.92));
        border: 1px solid rgba(129,140,248,.28);
        box-shadow: 0 18px 55px rgba(0,0,0,.22);
        margin-bottom: 22px;
    }
    .eyebrow { color: #a5b4fc; text-transform: uppercase; letter-spacing: 2px;
        font-size: 11px; font-weight: 800; }
    .hero h1 { font-size: clamp(30px, 4vw, 46px); margin: 7px 0 6px; color: #fff; }
    .hero p { color: #cbd5e1; margin: 0; font-size: 15px; }
    .metric {
        background: rgba(20,30,55,.82); border: 1px solid rgba(148,163,184,.16);
        padding: 18px 20px; border-radius: 18px; min-height: 105px;
    }
    .metric-label { color: #94a3b8; font-size: 12px; font-weight: 700; }
    .metric-value { color: #f8fafc; font-family: 'Space Grotesk'; font-size: 27px;
        font-weight: 700; margin-top: 5px; }
    .section-card {
        background: rgba(17,26,49,.78); border: 1px solid rgba(148,163,184,.15);
        border-radius: 20px; padding: 22px;
    }
    .muted { color: #94a3b8; font-size: 13px; }
    div.stButton > button, div.stDownloadButton > button {
        border-radius: 11px; font-weight: 700; min-height: 43px;
    }
    div[data-testid="stTextInput"] input, div[data-testid="stTextArea"] textarea {
        background: #111b32; border: 1px solid #334155; border-radius: 10px; color: #f8fafc;
    }
    div[data-testid="stSelectbox"] > div > div {
        background: #111b32; border-radius: 10px;
    }
    .file-row {
        background: rgba(30,41,59,.55); border: 1px solid rgba(148,163,184,.12);
        padding: 12px 15px; border-radius: 12px; margin: 7px 0;
    }
    footer { visibility: hidden; }
    </style>
    """,
    unsafe_allow_html=True,
)

# -------------------- Helpers --------------------
def safe_path(filename: str) -> Path:
    """Keep all operations inside the project_files directory."""
    cleaned = filename.strip()
    if not cleaned or cleaned in {".", ".."} or Path(cleaned).name != cleaned:
        raise ValueError("Enter a valid file name without folder paths.")
    return DATA_DIR / cleaned

def list_files():
    return sorted(
        [p for p in DATA_DIR.iterdir() if p.is_file()],
        key=lambda p: p.name.lower()
    )

def human_size(size):
    if size < 1024:
        return f"{size} B"
    if size < 1024**2:
        return f"{size / 1024:.1f} KB"
    return f"{size / (1024**2):.2f} MB"

files = list_files()
total_size = sum(p.stat().st_size for p in files)

# -------------------- Sidebar --------------------
with st.sidebar:
    st.markdown("## 📁 FileFlow")
    st.caption("A simple, clean file management workspace")
    st.markdown("---")
    page = st.radio(
        "WORKSPACE",
        ["Dashboard", "Create file", "Read file", "Update file", "Delete file"],
        label_visibility="visible",
    )
    st.markdown("---")
    st.markdown("**Storage location**")
    st.code(str(DATA_DIR.resolve()), language="text")
    st.caption("Files created here are stored locally in the project_files folder.")
    st.markdown("---")
    st.caption("Built with Python · pathlib · Streamlit")

# -------------------- Header --------------------
st.markdown(
    """
    <div class="hero">
      <div class="eyebrow">PERSONAL FILE WORKSPACE</div>
      <h1>Manage your files, effortlessly.</h1>
      <p>Create, explore, edit and organise your text files from one simple dashboard.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

# -------------------- Dashboard --------------------
if page == "Dashboard":
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(f'<div class="metric"><div class="metric-label">TOTAL FILES</div><div class="metric-value">{len(files)}</div></div>', unsafe_allow_html=True)
    with c2:
        st.markdown(f'<div class="metric"><div class="metric-label">STORAGE USED</div><div class="metric-value">{human_size(total_size)}</div></div>', unsafe_allow_html=True)
    with c3:
        st.markdown(f'<div class="metric"><div class="metric-label">WORKSPACE STATUS</div><div class="metric-value" style="font-size:22px">● Ready</div></div>', unsafe_allow_html=True)

    st.write("")
    left, right = st.columns([1.35, 1])
    with left:
        st.markdown("### Recent files")
        if files:
            for file in sorted(files, key=lambda p: p.stat().st_mtime, reverse=True)[:8]:
                modified = datetime.fromtimestamp(file.stat().st_mtime).strftime("%d %b %Y · %I:%M %p")
                st.markdown(
                    f'<div class="file-row">📄 <b>{file.name}</b><br><span class="muted">{human_size(file.stat().st_size)} &nbsp;·&nbsp; {modified}</span></div>',
                    unsafe_allow_html=True,
                )
        else:
            st.info("Your workspace is empty. Create your first file to get started.")
    with right:
        st.markdown("### Quick actions")
        st.caption("Choose an operation from the sidebar to get started.")
        if st.button("＋  Create a new file", use_container_width=True):
            st.session_state["quick_page"] = "Create file"
            st.rerun()
        if st.button("⌕  Browse existing files", use_container_width=True):
            st.session_state["quick_page"] = "Read file"
            st.rerun()
        if st.session_state.get("quick_page"):
            st.session_state.pop("quick_page", None)
        st.markdown(
            """
            <div class="section-card">
              <div class="eyebrow">HOW IT WORKS</div>
              <p>① Create a file and add content</p>
              <p>② Read saved content anytime</p>
              <p>③ Append, overwrite or rename</p>
              <p style="margin-bottom:0">④ Delete files you no longer need</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.write("")
    with st.expander("View all files"):
        if files:
            st.dataframe(
                [{"File name": p.name, "Size": human_size(p.stat().st_size),
                  "Last modified": datetime.fromtimestamp(p.stat().st_mtime).strftime("%d %b %Y, %I:%M %p")}
                 for p in files],
                use_container_width=True,
                hide_index=True,
            )
        else:
            st.caption("No files found.")

# -------------------- Create --------------------
elif page == "Create file":
    st.markdown("### ＋ Create a file")
    st.caption("Give your file a name and add the content you want to save.")
    with st.form("create_form", clear_on_submit=True):
        filename = st.text_input("File name", placeholder="e.g. my_notes.txt")
        content = st.text_area("File content", placeholder="Start writing here...", height=220)
        submitted = st.form_submit_button("Create file", type="primary", use_container_width=True)
    if submitted:
        try:
            target = safe_path(filename)
            if target.exists():
                st.warning("A file with this name already exists. Choose another name.")
            else:
                target.write_text(content, encoding="utf-8")
                st.success(f"'{target.name}' was created successfully.")
                st.rerun()
        except Exception as err:
            st.error(f"Could not create file: {err}")

# -------------------- Read --------------------
elif page == "Read file":
    st.markdown("### ⌕ Read a file")
    if not files:
        st.info("No files available yet. Create a file first.")
    else:
        selected = st.selectbox("Choose a file", [p.name for p in files])
        target = safe_path(selected)
        try:
            content = target.read_text(encoding="utf-8")
            st.markdown(f"**Preview · `{selected}`**")
            st.text_area("File content", value=content, height=300, disabled=True)
            st.download_button(
                "⬇ Download this file",
                data=content,
                file_name=selected,
                mime="text/plain",
                use_container_width=True,
            )
        except UnicodeDecodeError:
            st.error("This file is not a UTF-8 text file, so it cannot be previewed here.")
        except Exception as err:
            st.error(f"Could not read file: {err}")

# -------------------- Update --------------------
elif page == "Update file":
    st.markdown("### ✎ Update a file")
    st.caption("Append new text, replace the existing content, or rename a file.")
    if not files:
        st.info("No files available to update. Create a file first.")
    else:
        selected = st.selectbox("Select a file to update", [p.name for p in files])
        target = safe_path(selected)
        operation = st.radio(
            "Choose an operation",
            ["Append content", "Overwrite content", "Rename file"],
            horizontal=True,
        )
        if operation in ["Append content", "Overwrite content"]:
            new_content = st.text_area(
                "New content",
                placeholder="Type the content you want to add..." if operation == "Append content" else "Enter the replacement content...",
                height=220,
                key="update_content",
            )
            if st.button("Save changes", type="primary", use_container_width=True):
                try:
                    if operation == "Append content":
                        with target.open("a", encoding="utf-8") as file:
                            if target.stat().st_size > 0:
                                file.write("\n")
                            file.write(new_content)
                        st.success("Content appended successfully.")
                    else:
                        target.write_text(new_content, encoding="utf-8")
                        st.success("File content overwritten successfully.")
                    st.rerun()
                except Exception as err:
                    st.error(f"Could not update file: {err}")
        else:
            new_name = st.text_input("New file name", placeholder="e.g. updated_notes.txt")
            if st.button("Rename file", type="primary", use_container_width=True):
                try:
                    destination = safe_path(new_name)
                    if destination.exists():
                        st.warning("A file with that name already exists.")
                    else:
                        target.rename(destination)
                        st.success(f"File renamed to '{destination.name}'.")
                        st.rerun()
                except Exception as err:
                    st.error(f"Could not rename file: {err}")

# -------------------- Delete --------------------
elif page == "Delete file":
    st.markdown("### 🗑 Delete a file")
    st.caption("Deleted files cannot be recovered from this workspace.")
    if not files:
        st.info("No files available to delete.")
    else:
        selected = st.selectbox("Choose a file", [p.name for p in files])
        target = safe_path(selected)
        st.warning(f"You are about to permanently delete **{selected}** ({human_size(target.stat().st_size)}).")
        confirm = st.checkbox("I understand that this action cannot be undone.")
        if st.button("Delete permanently", type="primary", disabled=not confirm, use_container_width=True):
            try:
                target.unlink()
                st.success(f"'{selected}' was deleted successfully.")
                st.rerun()
            except Exception as err:
                st.error(f"Could not delete file: {err}")

st.markdown(
    "<p style='text-align:center;color:#64748b;font-size:12px;margin-top:42px'>FILEFLOW · Your files, your workspace · Made with Streamlit</p>",
    unsafe_allow_html=True,
)
