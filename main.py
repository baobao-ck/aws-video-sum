import boto3
import os
from extract_text import extract_text_from_file
from summarize import summarize_text
from tts import text_to_speech
from create_video import create_video

s3 = boto3.client("s3")
input_bucket = "summarizer-input-bucket"
output_bucket = "summarizer-output-bucket"

def process_file(file_key):
    local_file = "/tmp/input.pdf"
    s3.download_file(input_bucket, file_key, local_file)

    print("Extracting text...")
    raw_text = extract_text_from_file(local_file)

    print("Summarizing...")
    summary = summarize_text(raw_text)

    print("Creating narration...")
    audio_file = "/tmp/narration.mp3"
    text_to_speech(summary, audio_file)

    print("Creating video...")
    video_file = "/tmp/summary_video.mp4"
    image_file = "default.jpg"
    create_video(audio_file, image_file, video_file)

    print("Uploading result to S3...")
    s3.upload_file(video_file, output_bucket, file_key + ".mp4")
    print("✅ Video ready!")

if __name__ == "__main__":
    file_key = input("Enter file name from input bucket (e.g., test.pdf): ")
    process_file(file_key)