import json
import boto3
import os
import logging
import re

_bedrock_client = None

def get_bedrock_client():
    global _bedrock_client
    if _bedrock_client is None:
        region = os.environ.get("AWS_REGION") or os.environ.get("AWS_DEFAULT_REGION")
        if not region:
            raise RuntimeError("Missing AWS_REGION in environment")
        _bedrock_client = boto3.client("bedrock-runtime", region_name=region)
    return _bedrock_client

def query_claude(prompt: str) -> dict:
    bedrock = get_bedrock_client()
    model_id = os.environ.get("BEDROCK_MODEL_ID")

    if not model_id:
        raise RuntimeError("BEDROCK_MODEL_ID is not set in environment variables")

    body = {
        "anthropic_version": "bedrock-2023-05-31",
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 4096,
        "temperature": 0.3
    }

    logging.info("[EXTRACT] Sending prompt to Claude. First 500 characters:\n%s", prompt[:500])

    try:
        response = bedrock.invoke_model(
            modelId=model_id,
            body=json.dumps(body).encode("utf-8"),
            contentType="application/json"
        )
        raw = response["body"].read().decode("utf-8")
        logging.debug("[RAW Claude Response]:\n%s", raw[:1000])

        try:
            parsed = json.loads(raw)
            if isinstance(parsed, dict) and parsed.get("content"):
                content_text = parsed["content"][0]["text"]
            else:
                content_text = raw
        except Exception:
            content_text = raw

        logging.debug("[Claude content text (first 500 chars)]:\n%s", content_text[:500])

        # Try direct JSON parse if it's a clean object
        try:
            if content_text.strip().startswith("{"):
                extracted_data = json.loads(content_text)
                return {
                    "extracted_data": extracted_data,
                    "regex_code": ""
                }
        except Exception as e:
            logging.warning("[Fallback] Direct JSON parse failed: %s", e)

        # Fallback: extract largest valid JSON object from text
        try:
            json_block = extract_json_block(content_text)
            if json_block:
                extracted_data = json.loads(json_block)
                return {
                    "extracted_data": extracted_data,
                    "regex_code": ""
                }
        except Exception as e:
            logging.error("[ERROR] Failed to parse JSON block: %s", e)

        return {
            "extracted_data": {},
            "regex_code": ""
        }

    except Exception as e:
        logging.exception("[ERROR] Claude API call failed")
        return {
            "extracted_data": {},
            "regex_code": "",
            "error": str(e)
        }

def extract_json_block(text):
    """Tries to extract the first valid JSON object from a string"""
    braces = 0
    start = None
    for i, char in enumerate(text):
        if char == '{':
            if braces == 0:
                start = i
            braces += 1
        elif char == '}':
            braces -= 1
            if braces == 0 and start is not None:
                block = text[start:i+1]
                try:
                    json.loads(block)
                    return block
                except:
                    continue
    return None
