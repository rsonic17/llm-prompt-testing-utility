import os
import json
import boto3

# Setup Bedrock client
bedrock = boto3.client("bedrock-runtime", region_name=os.getenv("AWS_REGION", "us-east-1"))

# Claude 3 Haiku (default), pulled from env or fallback
BEDROCK_MODEL_ID = os.getenv("BEDROCK_MODEL_ID", "anthropic.claude-3-haiku-20240307-v1:0")
ANTHROPIC_VERSION = "bedrock-2023-05-31"

def query_claude(prompt: str):
    print("\n================ Sending Prompt to Claude ================\n")
    print(prompt[:1000] + ("\n... [truncated]" if len(prompt) > 1000 else ""))
    print(f"\n🔍 Using Bedrock model ID: {BEDROCK_MODEL_ID}")
    print("==========================================================\n")

    body = {
        "anthropic_version": ANTHROPIC_VERSION,
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 4096,
        "temperature": 0.3,
        "top_p": 1.0
    }

    try:
        response = bedrock.invoke_model(
            modelId=BEDROCK_MODEL_ID,
            body=json.dumps(body),
            contentType="application/json",
            accept="application/json"
        )
        response_body = response["body"].read()
        parsed = json.loads(response_body)

        # Extract first content block
        if isinstance(parsed.get("content"), list):
            text_response = parsed["content"][0].get("text", "").strip()
        else:
            text_response = "[ERROR] Claude response format unexpected."

        print("✅ Claude responded.\n")
        print(text_response[:1000])
        return {"extracted_data": text_response}

    except Exception as e:
        print("❌ Claude call failed:", str(e))
        return {"extracted_data": f"[Claude error] {str(e)}"}
