import os
import json
import traceback
import logging
from flask import Flask, request, render_template, jsonify
from werkzeug.utils import secure_filename
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

from app.parser import parse_eml_file
from app.llm import query_claude
from app.utils import sanitize_html

UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route("/", methods=["GET"])
def index():
    logging.debug("Serving index.html")
    return render_template("index.html")

@app.route("/upload", methods=["POST"])
def upload_file():
    try:
        uploaded_file = request.files['file']
        filename = secure_filename(uploaded_file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        uploaded_file.save(filepath)

        logging.info(f"[UPLOAD] File saved to: {filepath}")
        email_content = parse_eml_file(filepath)
        logging.debug(f"[UPLOAD] Parsed email keys: {list(email_content.keys())}")

        safe_html = sanitize_html(email_content.get('html', ''))

        return jsonify({
            "html": safe_html,
            "text": email_content.get('text', ''),
            "from": email_content.get("from_address", ""),
            "to": email_content.get("to_address", ""),
            "date": email_content.get("date", "")
        })

    except Exception as e:
        logging.error("UPLOAD ERROR", exc_info=True)
        return jsonify({"error": str(e)}), 500

@app.route("/extract", methods=["POST"])
def extract_data():
    try:
        data = request.json
        prompt_template = data.get("prompt", "")
        email_text = data.get("email_text", "")
        from_email = data.get("from", "")
        to_email = data.get("to", "")
        received_date = data.get("date", "")

        # Compose a more complete email block for LLM
        combined_text = f"From: {from_email}\nTo: {to_email}\nDate: {received_date}\n\n{email_text}"
        prompt = prompt_template.replace("{email_data}", combined_text)

        logging.info("[EXTRACT] Starting LLM Extraction...")
        logging.debug("[EXTRACT] Prompt preview: %s", prompt[:1000])

        result = query_claude(prompt)

        logging.info("[EXTRACT] LLM Extraction complete")
        logging.debug("[EXTRACT] LLM Raw JSON:\n%s", json.dumps(result, indent=2))
        return jsonify(result)

    except Exception as e:
        logging.error("EXTRACTION ERROR", exc_info=True)
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
