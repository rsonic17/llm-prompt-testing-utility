import email
from email import policy
from email.parser import BytesParser
from bs4 import BeautifulSoup
import io
from PyPDF2 import PdfReader

def parse_eml_file(file_obj):
    # Parse using email module
    if hasattr(file_obj, 'read'):
        file_obj.seek(0)
        msg = BytesParser(policy=policy.default).parse(file_obj)
    else:
        with open(file_obj, 'rb') as f:
            msg = BytesParser(policy=policy.default).parse(f)

    html_body = ""
    text_body = ""
    attachments = []

    # Walk through parts
    if msg.is_multipart():
        for part in msg.walk():
            ctype = part.get_content_type()
            disposition = part.get("Content-Disposition", "")
            filename = part.get_filename()

            if ctype == "text/plain" and "attachment" not in disposition:
                text_body += part.get_content()
            elif ctype == "text/html" and "attachment" not in disposition:
                html_body += part.get_content()
            elif "attachment" in disposition and filename:
                data = part.get_payload(decode=True)
                ext = filename.split(".")[-1].lower()
                parsed_content = None

                if ext == "pdf":
                    try:
                        reader = PdfReader(io.BytesIO(data))
                        parsed_content = "\n".join(
                            page.extract_text() for page in reader.pages if page.extract_text()
                        )
                    except Exception as e:
                        print(f"⚠️ PDF parsing error ({filename}):", str(e))
                        parsed_content = None
                else:
                    try:
                        parsed_content = data.decode(errors="ignore")
                    except Exception as e:
                        print(f"⚠️ Non-PDF attachment decode error ({filename}):", str(e))
                        parsed_content = None

                attachments.append({
                    "filename": filename,
                    "content_type": ctype,
                    "text": parsed_content
                })
    else:
        # Handle single-part emails
        if msg.get_content_type() == "text/plain":
            text_body = msg.get_content()
        elif msg.get_content_type() == "text/html":
            html_body = msg.get_content()

    # Convert HTML to text if plain not available
    if not text_body and html_body:
        soup = BeautifulSoup(html_body, "html.parser")
        text_body = soup.get_text()

    email_dict = {
        "html": html_body,
        "text": text_body,
        "from_address": msg.get("From", ""),
        "to_address": msg.get("To", ""),
        "subject": msg.get("Subject", ""),
        "date": msg.get("Date", ""),
        "attachments": attachments
    }

    print("✅ Parsed email fields:", list(email_dict.keys()))
    return email_dict
