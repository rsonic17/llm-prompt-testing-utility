import streamlit as st
import json
from llm import query_claude

PANEL_HEIGHT = 800
PANEL_STYLE = """
    height: {height}px;
    overflow-y: auto;
    overflow-x: auto;
    border: 1px solid #444;
    border-radius: 6px;
    padding: 12px;
    background-color: #1e1e1e;
    color: #f0f0f0;
    font-family: 'Courier New', monospace;
    font-size: 12px;
    white-space: pre-wrap;
    word-wrap: break-word;
    box-shadow: 0 1px 3px rgba(0,0,0,0.3);
"""

def format_json_nicely(content):
    try:
        if isinstance(content, str):
            parsed = json.loads(content.replace("'", "\""))
        else:
            parsed = content
        return json.dumps(parsed, indent=2)
    except Exception as e:
        print(f"⚠️ JSON formatting failed: {e}")
        return content

def clean_improved_prompt(text):
    lines = text.strip().splitlines()
    # Skip leading intro lines until actual prompt starts
    for i, line in enumerate(lines):
        if "prompt" in line.lower() and len(line.strip()) < 80:
            return "\n".join(lines[i+1:]).strip()
    return text.strip()

def render_readonly_panel(title, content, key_prefix, height, is_json=False, html_mode=False):
    if is_json and content:
        content = format_json_nicely(content)

    if html_mode:
        display_content = content if content else f"<i>No {title.lower()} yet.</i>"
        st.markdown(f"**{title}**", unsafe_allow_html=True)
        st.markdown(
            f"<div style='{PANEL_STYLE.format(height=height)}'>{display_content}</div>",
            unsafe_allow_html=True
        )
    else:
        display_content = content if content else f"No {title.lower()} yet."
        st.markdown(f"**{title}**")
        st.markdown(
            f"<div style='{PANEL_STYLE.format(height=height)}'>{display_content}</div>",
            unsafe_allow_html=True
        )

def render_app_ui():
    st.markdown("""
    <style>
        .stColumns { gap: 1rem; }
        .stColumns > div { min-width: 0; flex: 1; }
        .element-container { width: 100% !important; }
        table {
            border-collapse: collapse;
            width: 100%;
            font-size: 12px;
        }
        th, td {
            border: 1px solid #666;
            padding: 8px;
            text-align: left;
            vertical-align: top;
        }
        th {
            background-color: #333;
        }
    </style>
    """, unsafe_allow_html=True)

    st.markdown("## 🧠 User Prompt")
    st.session_state.user_prompt = st.text_area(
        "Paste your prompt below (use `{email_data}` as placeholder):",
        value=st.session_state.user_prompt,
        height=180
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("🧠 Extract with LLM"):
            email_body = st.session_state.email_data.get("text", "")
            prompt = st.session_state.user_prompt.replace("{email_data}", email_body)
            result = query_claude(prompt)
            st.session_state.extracted_data = result["extracted_data"]

    with col2:
        if st.button("✨ Suggest Better Prompt"):
            email_snippet = st.session_state.email_data.get("text", "")[:1000]
            sample_output = (
                "The email is from `notifications@paymode.com` to `carla.wells@sunbeltrentals.com` on May 14, 2025.\n"
                "The buyer is Scranton Manufacturing Co Inc and the last 4 digits of the payment card are 0906.\n"
                "The total amount paid was $7,435.21."
            )

            improvement_prompt = f"""
You are a prompt optimization expert.

Rewrite the user's extraction prompt into a clean, scalable, few-shot natural language prompt.

Requirements:
- Clear and user-friendly
- Reusable across various email formats
- Contains one natural-language example output
- Avoid technical jargon

Return **only** the rewritten prompt.

## Original Prompt
{st.session_state.user_prompt}

## Email Snippet
{email_snippet}

## Example Output
{sample_output}
"""
            result = query_claude(improvement_prompt)
            st.session_state.improved_prompt = clean_improved_prompt(result["extracted_data"])

    with col3:
        if st.button("📝 Compare Prompts"):
            comparison_prompt = f"""
Compare the following two prompts.

Step 1: Create a markdown table comparing:
- Clarity
- Completeness
- Flexibility
- Reusability
- Ease of Understanding

Step 2: Add 2–3 sentences explaining which is better and why.

Return only markdown.

## Prompt A (User Prompt)
{st.session_state.user_prompt}

## Prompt B (Improved Prompt)
{st.session_state.improved_prompt}
"""
            result = query_claude(comparison_prompt)

            # Convert markdown table to HTML table for better display
            markdown = result["extracted_data"]

            # Convert simple markdown table to HTML
            html_table = markdown
            if markdown.startswith("|"):
                try:
                    rows = [row.strip() for row in markdown.strip().splitlines() if row.strip()]
                    header = rows[0].split("|")[1:-1]
                    body = rows[2:]  # skip header & separator
                    table_html = "<table><tr>" + "".join(f"<th>{h.strip()}</th>" for h in header) + "</tr>"
                    for row in body:
                        cols = row.split("|")[1:-1]
                        table_html += "<tr>" + "".join(f"<td>{c.strip()}</td>" for c in cols) + "</tr>"
                    table_html += "</table>"
                    markdown_tail = "\n\n".join(markdown.split("\n\n")[1:])
                    st.session_state.comparison = table_html + f"<br><br>{markdown_tail.strip()}"
                except Exception as e:
                    print("⚠️ Table conversion failed:", str(e))
                    st.session_state.comparison = markdown
            else:
                st.session_state.comparison = markdown

    st.markdown("---")

    colA, colB, colC, colD = st.columns(4, gap="small")

    with colA:
        render_readonly_panel("📄 Email Preview", st.session_state.email_data.get("text", ""), "email_preview", PANEL_HEIGHT)

    with colB:
        render_readonly_panel("📦 LLM Extracted Data", st.session_state.extracted_data, "llm_extracted", PANEL_HEIGHT, is_json=True)

    with colC:
        render_readonly_panel("🌟 Improved Prompt", st.session_state.improved_prompt, "improved_prompt", PANEL_HEIGHT)

    with colD:
        render_readonly_panel("📑 Prompt Comparison", st.session_state.comparison, "prompt_comparison", PANEL_HEIGHT, html_mode=True)
