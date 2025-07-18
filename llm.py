import os
import json
import boto3

bedrock = boto3.client("bedrock-runtime", region_name=os.getenv("AWS_REGION", "us-east-1"))
ANTHROPIC_VERSION = "bedrock-2023-05-31"

CLAUDE_MODELS = [
    "anthropic.claude-3-haiku-20240307-v1:0",
    "anthropic.claude-3-5-haiku-20241022-v1:0"
]
LLAMA_MODELS = [
    "meta.llama3-3-70b-instruct-v1:0"
]

INFERENCE_PROFILE_ARN_MAP = {
    "anthropic.claude-3-5-haiku-20241022-v1:0": os.getenv("BEDROCK_INFERENCE_PROFILE_35"),
    "meta.llama3-3-70b-instruct-v1:0": os.getenv("BEDROCK_INFERENCE_PROFILE_LLAMA3")
}

def get_available_models():
    return CLAUDE_MODELS + LLAMA_MODELS

def build_email_prompt(email_data: dict) -> str:
    prompt = f"""=== EMAIL METADATA ===
From: {email_data.get("from_address", "[missing]")}
To: {email_data.get("to_address", "[missing]")}
Subject: {email_data.get("subject", "")}
Date: {email_data.get("date", "")}

=== EMAIL BODY ===
{email_data.get("text", "").strip()}

=== ATTACHMENT CONTENT ===
{email_data.get("attachment_text_summary", "").strip()}

=== EMBEDDED IMAGE TEXT (OCR) ===
{email_data.get("embedded_image_text", "").strip()}
"""
    print("\n========== DEBUG: FULL LLM PROMPT BEGIN ==========")
    print(prompt)
    print("=========== DEBUG: FULL LLM PROMPT END ============\n")
    return prompt

def query_claude(prompt: str, model_id: str = None):
    model_id = model_id or os.getenv("BEDROCK_MODEL_ID", CLAUDE_MODELS[0])
    profile_arn = INFERENCE_PROFILE_ARN_MAP.get(model_id)
    effective_model_id = profile_arn or model_id

    print("\n================ Sending Prompt to Bedrock ================\n")
    print(prompt[:1000] + ("\n... [truncated]" if len(prompt) > 1000 else ""))
    print(f"\n🔍 Requested Model ID: {model_id}")
    print(f"🧠 Effective Model/ARN Used: {effective_model_id}")
    print("===========================================================\n")

    try:
        if model_id in LLAMA_MODELS:
            with open("llama_debug_prompt.txt", "w") as f:
                f.write(prompt)
            body = {
                "prompt": f"[INST] {prompt} [/INST]",
                "max_gen_len": 4096,
                "temperature": 0,
                "top_p": 0.9
            }

        elif model_id in CLAUDE_MODELS:
            body = {
                "anthropic_version": ANTHROPIC_VERSION,
                "messages": [{"role": "user", "content": prompt}],
                "max_tokens": 4096,
                "temperature": 0,
                "top_p": 0.9
            }

        else:
            return {"extracted_data": f"[Unsupported model: {model_id}]"}

        response = bedrock.invoke_model(
            modelId=effective_model_id,
            body=json.dumps(body),
            contentType="application/json",
            accept="application/json"
        )

        response_body = response["body"].read()
        parsed = json.loads(response_body)

        if model_id in CLAUDE_MODELS:
            text_response = parsed["content"][0].get("text", "").strip()
        elif model_id in LLAMA_MODELS:
            text_response = parsed.get("generation", "").strip()
        else:
            text_response = "[ERROR] Unexpected model response format"

        print("✅ Model responded successfully.\n")
        print(text_response[:1000])
        return {"extracted_data": text_response}

    except Exception as e:
        print(f"❌ Bedrock call failed for model {model_id}: {type(e).__name__} - {e}")
        return {"extracted_data": f"[LLM Error: {type(e).__name__}] {e}"}
