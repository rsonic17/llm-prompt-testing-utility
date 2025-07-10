
def build_prompt(plain_text: str, html_content: str = "", from_addr: str = "", to_addr: str = "") -> str:
    """
    Claude prompt builder — forces regex to match JSON output precisely, avoids hardcoded values.
    """
    prompt = f"""
You are an intelligent document parser.

Your job is to extract structured data from the email below. The email may contain multiple invoice line items. Field names and formats may vary — be flexible.

---

### GLOBAL FIELDS TO EXTRACT

These must always be extracted. Normalize them regardless of naming:

- buyer_name
- supplier_name
- payment_amount
- credit_card_number
- card_last_four
- from_email_address (header: "{from_addr}")
- to_email_address (header: "{to_addr}")

---

### INVOICES (MULTIPLE POSSIBLE)

Extract these for each invoice:

- invoice_number
- invoice_date
- invoice_amount

Return them under a list called `invoices`.

---

### OUTPUT FORMAT

Respond with **two clearly separated code blocks**:

#### 1. JSON block with all extracted fields and nested invoices
#### 2. Python block named `extract_fields(text)` that uses regex to extract same values

The Python regex function must:
- Use `re.search` or `re.findall` for single fields
- Use `re.finditer` for the invoice loop
- Avoid hardcoding values
- Match regex values exactly to those returned in your JSON

---

Example:

```json
{{
  "buyer_name": "...",
  "supplier_name": "...",
  "payment_amount": "...",
  "credit_card_number": "...",
  "card_last_four": "...",
  "from_email_address": "...",
  "to_email_address": "...",
  "invoices": [
    {{
      "invoice_number": "...",
      "invoice_date": "...",
      "invoice_amount": "..."
    }}
  ]
}}
```

```python
def extract_fields(text):
    import re
    invoices = []
    for match in re.finditer(r"...", text, re.DOTALL):
        invoices.append({{
            "invoice_number": match.group(1),
            "invoice_date": match.group(2),
            "invoice_amount": match.group(3)
        }})

    return {{
        "buyer_name": re.search(r"...", text).group(1) if re.search(r"...", text) else "",
        "supplier_name": re.search(r"...", text).group(1) if re.search(r"...", text) else "",
        ...
        "invoices": invoices
    }}
```

---

Now return both code blocks, nothing else.

---

EMAIL BODY

Plain Text:
----------------------------------------
{plain_text}
----------------------------------------

HTML (optional):
[START HTML]
{html_content}
[END HTML]
    """
    return prompt.strip()
