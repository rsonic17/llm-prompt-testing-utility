
# 📧 LLM Email Parser App

An interactive Flask-based app that:
- Accepts `.eml` email uploads
- Parses HTML + attachments
- Sends content to Claude via AWS Bedrock
- Receives structured JSON + regex function
- Safely runs regex and compares output
- Displays everything in a Vue + Tailwind UI

---

## 🚀 Features

- Full HTML email rendering
- Claude LLM integration via Bedrock
- Safe regex `exec()` and field comparison
- Confidence scoring + inline match analysis
- Vue + Alpine + Prism-powered frontend

---

## 🛠 Setup

### 1. Clone & Create Environment

```bash
python -m venv venv
.env\Scripts\Activate.ps1
pip install -r requirements.txt
```

### 2. Configure `.env`

```
AWS_ACCESS_KEY_ID=your-key
AWS_SECRET_ACCESS_KEY=your-secret
AWS_DEFAULT_REGION=us-east-1
BEDROCK_MODEL_ID=anthropic.claude-3-haiku-20240307-v1:0
```

### 3. Run the App

```bash
python app/main.py
```

Then visit: [http://localhost:5000](http://localhost:5000)

---

## 🧪 File Structure

```
llm_email_parser_app/
├── app/
│   ├── main.py
│   ├── llm.py
│   ├── parser.py
│   ├── prompt.py
│   ├── regex_evaluator.py
│   ├── utils.py
│   ├── templates/index.html
│   └── static/{styles.css, app.js}
├── uploads/
├── attachments/
├── requirements.txt
├── .env
├── .gitignore
└── README.md
```

---

## 🧠 Security

- Regex functions sandboxed and logged
- No dangerous eval/imports allowed
- `.env` excluded from Git

---

## 📄 License

MIT (You’re free to use, modify, or fork.)
