import streamlit as st
from utils_ui import render_app_ui
from email_parser import parse_eml_file
from llm import build_email_prompt  # ✅ Add this import

from dotenv import load_dotenv
load_dotenv()

st.set_page_config(layout="wide")

if "app_reset" not in st.session_state:
    st.session_state["app_reset"] = False

top_col1, top_col2 = st.columns([8, 1])
with top_col2:
    if st.button("🔄 Refresh App"):
        st.session_state.clear()
        st.session_state["app_reset"] = True
        st.rerun()

for key in ["user_prompt", "email_data", "extracted_data", "improved_prompt", "comparison"]:
    if key not in st.session_state:
        st.session_state[key] = "" if "prompt" in key or key == "comparison" else {}

st.markdown("### 📬 Upload Email (.eml)")
uploaded_file = st.file_uploader(
    "Drag and drop file here",
    type=["eml"],
    key="uploader_reset" if st.session_state.get("app_reset") else "uploader"
)

if uploaded_file is not None:
    try:
        st.session_state.email_data = parse_eml_file(uploaded_file)
        st.success("✅ Email parsed successfully!")

        st.write("📤 From:", st.session_state.email_data.get("from_address"))
        st.write("📥 To:", st.session_state.email_data.get("to_address"))

        print("📥 Uploaded email parsed. Keys:", list(st.session_state.email_data.keys()))
    except Exception as e:
        st.error("❌ Failed to parse email.")
        print("❌ Email parsing failed:", str(e))

render_app_ui()
