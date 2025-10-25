import os
import re
from pathlib import Path

def renumber_frames(directory='sheet_music_frames'):
    """
    Renumber all PNG frames in the directory to be consecutive starting from 0

    Parameters:
        directory: Directory containing the frame files
    """

    # Get all PNG files in the directory
    frame_files = []
    for filename in os.listdir(directory):
        if filename.endswith('.png'):
            # Extract the number from the filename
            match = re.match(r'frame_(\d+)\.png', filename)
            if match:
                frame_number = int(match.group(1))
                frame_files.append((frame_number, filename))

    # Sort by the original frame number
    frame_files.sort(key=lambda x: x[0])

    print(f"Found {len(frame_files)} frame files")
    print(f"Original range: frame_{frame_files[0][0]:05d}.png to frame_{frame_files[-1][0]:05d}.png")

    # Create temporary directory for renamed files
    temp_dir = Path(directory) / 'temp_rename'
    temp_dir.mkdir(exist_ok=True)

    # Rename files to temporary location with new sequential numbers
    for new_index, (old_number, old_filename) in enumerate(frame_files):
        old_path = os.path.join(directory, old_filename)
        new_filename = f'frame_{new_index:05d}.png'
        temp_path = os.path.join(temp_dir, new_filename)

        os.rename(old_path, temp_path)
        if (new_index + 1) % 10 == 0 or new_index == len(frame_files) - 1:
            print(f"Renamed {new_index + 1}/{len(frame_files)} files...")

    # Move files back to original directory
    for filename in os.listdir(temp_dir):
        src = os.path.join(temp_dir, filename)
        dst = os.path.join(directory, filename)
        os.rename(src, dst)

    # Remove temporary directory
    temp_dir.rmdir()

    print(f"\nRenumbering complete!")
    print(f"New range: frame_00000.png to frame_{len(frame_files)-1:05d}.png")
    print(f"All {len(frame_files)} frames are now consecutively numbered")

if __name__ == "__main__":
    renumber_frames('sheet_music_frames')
