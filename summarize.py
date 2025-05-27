import boto3
import json

def summarize_text(text):
    client = boto3.client("bedrock-runtime")
    prompt = f"Summarize this document for a video narration:\n\n{text[:8000]}"
    body = json.dumps({
        "prompt": f"\n\nHuman: {prompt}\n\nAssistant:",
        "max_tokens": 500,
        "temperature": 0.5,
        "stop_sequences": ["\n\n"]
    })

    response = client.invoke_model(
        modelId="anthropic.claude-v2",
        body=body,
        contentType="application/json"
    )
    result = json.loads(response["body"].read())
    return result["completion"]