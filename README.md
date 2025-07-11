# 🧠 LLM-Powered Email Extraction App

This Streamlit web app lets you upload `.eml` email files and use Anthropic Claude (via AWS Bedrock) to:

- Extract structured JSON data from emails
- Automatically generate cleaner, reusable prompts
- Compare prompt quality side-by-side in a 4-column interface

---

## 🚀 Features

- ✅ **.eml File Upload & Parsing** — Extracts `text`, `html`, sender, subject, attachments (PDFs included)
- 🤖 **Claude-Powered Extraction** — Uses `user_prompt` to pull out JSON info from emails
- ✨ **Improved Prompt Generator** — Claude rewrites your prompt in scalable, few-shot natural language
- 📊 **Prompt Comparison Tool** — See a side-by-side markdown table comparing your prompt vs Claude’s
- 🖼 **Fixed 4-Column UI** — Horizontal layout: Email Preview | JSON | Improved Prompt | Comparison
- 🌙 **Dark Panel Layout** — Panels styled for readability in dark mode, no HTML clutter

---

## 🛠️ Technologies Used

| Tool            | Purpose                               |
|-----------------|----------------------------------------|
| **Streamlit**   | Frontend Web App                      |
| **AWS Bedrock** | Claude 3 Haiku (LLM prompt processing) |
| **boto3**       | Python SDK for AWS                    |
| **PyPDF2**      | PDF Attachment Parsing                |
| **BeautifulSoup** | HTML to Text Conversion             |
| **Bleach**      | HTML Sanitization (optional)          |

---

## 📦 Installation

### 🐍 Python Environment

```bash
git clone https://github.com/rsonic17/llm-prompt-testing-utility.git
cd llm-prompt-testing-utility
python -m venv venv
source venv/bin/activate   # or venv\Scripts\activate on Windows
pip install -r requirements.txt
```

### 🔐 Setup AWS Credentials

Ensure you have:

- AWS credentials in `~/.aws/credentials`
- AWS region and model ID set via environment:

```bash
export AWS_REGION=us-east-1
export BEDROCK_MODEL_ID=anthropic.claude-3-haiku-20240307-v1:0
```

You can also use a `.env` file and `python-dotenv`.

---

## 🧪 Usage

```bash
streamlit run app.py
```

1. Upload a `.eml` file
2. Paste a Claude-compatible prompt (use `{email_data}` as placeholder)
3. Click:
   - `🧠 Extract with LLM`
   - `✨ Suggest Better Prompt`
   - `📝 Compare Prompts`
4. View results in 4 scrollable panels

---

## 🔤 Prompt Format (Example)

Paste this in the "User Prompt" box:

```
Extract the following fields from this email:
- Buyer Name
- Sender Email
- Date
- Payment Amount

Output JSON like:

{
  "buyer": "...",
  "sender": "...",
  "amount": "...",
  "date": "..."
}

Email:
{email_data}
```

---

## 🖼 UI Overview

> 📸 _You can add screenshots here later._

| Panel              | Purpose                      |
|--------------------|------------------------------|
| 📄 Email Preview   | Raw email text               |
| 📦 LLM Extracted Data | Claude’s structured JSON |
| 🌟 Improved Prompt | Claude's few-shot rewrite    |
| 📑 Prompt Comparison | Markdown table comparison  |

---

## 👥 Contributing

Pull requests are welcome. Please open an issue to discuss any major changes.

---

## 📄 License

MIT License © 2025 [Your Name / Org]
