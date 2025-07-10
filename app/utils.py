import bleach
import re

def sanitize_html(html: str) -> str:
    """
    Clean HTML to be safe for rendering in the browser.
    """
    allowed_tags = list(bleach.sanitizer.ALLOWED_TAGS) + [
        "p", "div", "span", "br", "hr", "table", "thead", "tbody", "tr", "td", "th"
    ]
    allowed_attrs = {
        '*': ['style', 'class'],
        'a': ['href', 'title'],
        'img': ['src', 'alt'],
    }
    return bleach.clean(html, tags=allowed_tags, attributes=allowed_attrs)

def clean_text(text: str) -> str:
    """
    Pre-clean junk characters from email before sending to LLM.
    """
    if not text:
        return ""

    text = re.sub(r'\x1b[^m]*m', '', text)
    text = re.sub(r'[\x00-\x1F\x7F-\x9F]', '', text)
    text = text.replace('\u200b', '')
    text = re.sub(r'\r\n|\r', '\n', text)
    text = re.sub(r'\n{3,}', '\n\n', text)
    text = re.sub(r'[ \t]{2,}', ' ', text)

    return text.strip()

def compare_fields(llm_data: dict, regex_data: dict) -> dict:
    return {}
