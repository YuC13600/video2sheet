import cv2
import os
from pathlib import Path


def extract_sheet_music_frames(
    video_path, output_dir="output_frames", interval_seconds=9
):
    """
    Extract sheet music from upper portion of piano performance video at regular time intervals

    Parameters:
        video_path: Path to video file
        output_dir: Output directory
        interval_seconds: Time interval in seconds between saved frames
    """

    # Create output directory
    Path(output_dir).mkdir(parents=True, exist_ok=True)

    # Open video
    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        print(f"Cannot open video file: {video_path}")
        return

    # Get video info
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    print(f"Video info: {width}x{height}, {fps:.2f} FPS, {total_frames} frames total")

    # Calculate frame interval based on desired time interval
    frame_interval = int(fps * interval_seconds)
    print(
        f"Saving one frame every {interval_seconds} seconds (every {frame_interval} frames)"
    )

    # Calculate upper half height (you can adjust this ratio)
    upper_half_height = int(height // 2.5)

    frame_count = 0
    saved_count = 0

    print("Processing video...")

    while True:
        ret, frame = cap.read()

        if not ret:
            break

        frame_count += 1

        # Show progress
        if frame_count % 100 == 0:
            print(f"Processed: {frame_count}/{total_frames} frames")

        # Save frame at regular intervals
        if frame_count % frame_interval == 0:
            # Crop upper portion
            upper_frame = frame[0:upper_half_height, :]

            output_path = os.path.join(output_dir, f"frame_{saved_count:05d}.png")
            cv2.imwrite(output_path, upper_frame)
            saved_count += 1

    cap.release()

    print(f"\nProcessing complete!")
    print(f"Total frames processed: {frame_count}")
    print(f"Frames saved: {saved_count}")
    print(f"Time interval: {interval_seconds} seconds")
    print(f"Output directory: {output_dir}")


# Usage example
if __name__ == "__main__":
    # Change to your video path
    video_path = "temp.mkv"

    # Optional parameters:
    # output_dir: Output directory name
    # interval_seconds: Time interval in seconds between saved frames (default: 9)

    extract_sheet_music_frames(
        video_path=video_path, output_dir="sheet_music_frames", interval_seconds=10
    )
