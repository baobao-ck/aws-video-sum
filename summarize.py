# Paste the new content here exactly
# For example:
import boto3
import json
import time

client = boto3.client("bedrock-runtime", region_name="us-east-1")

def summarize_large_text(text, chunk_size=1500, max_retries=5):
    chunks = [text[i:i + chunk_size] for i in range(0, len(text), chunk_size)]
    summary_chunks = []

    for i, chunk in enumerate(chunks):
        print(f"Summarizing chunk {i + 1}/{len(chunks)} (length={len(chunk)})")
        retries = 0
        while retries < max_retries:
            try:
                body = json.dumps({
                    "prompt": f"\n\nHuman: Summarize the following text:\n{chunk}\n\nAssistant:",
                    "max_tokens_to_sample": 500,
                    "temperature": 0.7,
                    "top_k": 250,
                    "top_p": 0.9,
                    "stop_sequences": ["\n\nHuman:"]
                })

                response = client.invoke_model(
                    modelId="anthropic.claude-v2",
                    body=body,
                    contentType="application/json",
                    accept="application/json"
                )

                response_body = json.loads(response["body"].read())
                summary = response_body["completion"]
                summary_chunks.append(summary)
                break

            except client.exceptions.ThrottlingException:
                print("⏳ Throttled, retrying...")
                time.sleep(2)
                retries += 1
            except Exception as e:
                print(f"❌ Failed to summarize chunk {i + 1}: {e}")
                retries += 1

        else:
            raise Exception("Max retries reached for summarize_text")

    return "\n".join(summary_chunks)
