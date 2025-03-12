import os
import subprocess

def split_video(video_path, output_dir, num_parts):
    """
    Splits a video into a specified number of equal-length segments.

    Args:
        video_path (str): Path to the input video file.
        output_dir (str): Directory where the split videos will be saved.
        num_parts (int): Number of equal-length segments to split into.
    """
    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Get video duration using ffprobe
    cmd = [
        "ffprobe", "-v", "error", "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1", video_path
    ]
    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    try:
        total_duration = float(result.stdout.strip())
    except ValueError:
        print("Error: Unable to determine video duration.")
        return

    # Calculate segment duration
    segment_duration = total_duration / num_parts

    # Split the video using ffmpeg
    for i in range(num_parts):
        start_time = i * segment_duration
        output_file = os.path.join(output_dir, f"segment_{i+1:02d}.mp4")

        ffmpeg_cmd = [
            "ffmpeg", "-y", "-i", video_path, "-ss", str(start_time), "-t", str(segment_duration),
            "-c", "copy", output_file
        ]

        subprocess.run(ffmpeg_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print(f"Created segment {i+1}/{num_parts}: {output_file}")

    print("Splitting complete.")

# Example usage
# split_video("input.mp4", "output_segments", 48)

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Split a video into equal-length segments.")
    parser.add_argument("video_path", help="Path to the input video file.")
    parser.add_argument("output_dir", help="Directory where the split videos will be saved.")
    parser.add_argument("num_parts", type=int, help="Number of equal-length segments to split into.")
    args = parser.parse_args()

    split_video(args.video_path, args.output_dir, args.num_parts)

    # Example usage:
    # python split_videos.py input.mp4 output_directory 48