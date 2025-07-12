import streamlit as st
from utils_ui import render_app_ui
from parser import parse_eml_file

# Set Streamlit to wide layout
st.set_page_config(layout="wide")

# Initialize app reset key
if "app_reset" not in st.session_state:
    st.session_state["app_reset"] = False

# 🔄 Native Refresh Button in top-right corner
top_col1, top_col2 = st.columns([8, 1])
with top_col2:
    if st.button("🔄 Refresh App"):
        st.session_state.clear()
        st.session_state["app_reset"] = True  # Trigger uploader key reset
        st.rerun()

# Initialize session state
for key in [
    "user_prompt",
    "email_data",
    "extracted_data",
    "improved_prompt",
    "comparison"
]:
    if key not in st.session_state:
        st.session_state[key] = "" if "prompt" in key or key == "comparison" else {}

# 📬 Email uploader — reset by toggling key on refresh
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
        print("📥 Uploaded email parsed. Keys:", list(st.session_state.email_data.keys()))
    except Exception as e:
        st.error("❌ Failed to parse email.")
        print("❌ Email parsing failed:", str(e))

# Render full UI
render_app_ui()
