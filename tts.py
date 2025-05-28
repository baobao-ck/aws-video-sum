import boto3
import os
import uuid
from pydub import AudioSegment

polly = boto3.client("polly")

def split_text(text, max_length=2900):
    # Split the text into roughly sentence-sized chunks
    import textwrap
    return textwrap.wrap(text, max_length, break_long_words=False, break_on_hyphens=True)

def text_to_speech(text, output_path):
    print("🔊 Splitting long text for TTS...")
    chunks = split_text(text)

    combined = AudioSegment.empty()

    for i, chunk in enumerate(chunks):
        print(f"🗣️ Synthesizing chunk {i+1}/{len(chunks)}...")

        response = polly.synthesize_speech(
            Text=chunk,
            OutputFormat="mp3",
            VoiceId="Joanna"
        )

        chunk_filename = f"/tmp/part_{uuid.uuid4().hex}.mp3"
        with open(chunk_filename, "wb") as f:
            f.write(response["AudioStream"].read())

        part_audio = AudioSegment.from_mp3(chunk_filename)
        combined += part_audio
        os.remove(chunk_filename)

    combined.export(output_path, format="mp3")
    print(f"✅ Narration saved to: {output_path}")
