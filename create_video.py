import subprocess

def create_video(audio_file, image_file, output_file):
    subprocess.run([
        "ffmpeg", "-y",
        "-loop", "1", "-i", image_file,
        "-i", audio_file,
        "-vf", "scale=trunc(iw/2)*2:trunc(ih/2)*2",  # Ensures dimensions are divisible by 2
        "-c:v", "libx264", "-tune", "stillimage",
        "-c:a", "aac", "-b:a", "192k", "-pix_fmt", "yuv420p",
        "-shortest", output_file
    ])
