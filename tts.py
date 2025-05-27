import boto3

def text_to_speech(text, output_path):
    polly = boto3.client("polly")
    response = polly.synthesize_speech(Text=text, OutputFormat="mp3", VoiceId="Joanna")
    with open(output_path, "wb") as f:
        f.write(response["AudioStream"].read())