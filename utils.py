import bleach

def sanitize_html(html: str) -> str:
    """
    Clean HTML content by removing unwanted tags and attributes.
    Keeps essential formatting tags for readability.

    Args:
        html (str): Raw HTML content

    Returns:
        str: Cleaned, safe HTML
    """
    return bleach.clean(
        html,
        tags=["p", "br", "ul", "li", "strong", "em", "b", "i", "a", "div"],
        attributes={"a": ["href"]},
        strip=True
    )
