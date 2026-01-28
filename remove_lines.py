"""Remove specific colored pixels (and their neighbors) from sheet music frames."""

from pathlib import Path

import numpy as np
from PIL import Image


def remove_colored_lines(
    input_dir: str = "sheet_music_frames",
    output_dir: str = "sheet_music_frames_noline",
) -> None:
    """
    Replace cyan/blue colored pixels and their neighbors with f6f6f6.

    Uses HSV color space to detect cyan/blue hues that represent playback lines.

    Args:
        input_dir: Directory containing input PNG images.
        output_dir: Directory to save processed images.
    """
    # Replacement color
    replacement_color = np.array([0xF6, 0xF6, 0xF6], dtype=np.uint8)

    # Create output directory
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    input_path = Path(input_dir)
    png_files = sorted(input_path.glob("*.png"))

    if not png_files:
        print(f"No PNG files found in {input_dir}")
        return

    print(f"Processing {len(png_files)} images...")

    for png_file in png_files:
        print(f"Processing: {png_file.name}")

        # Load image as RGB
        img = Image.open(png_file).convert("RGB")
        img_array = np.array(img)

        # Convert to HSV for better color detection
        img_hsv = np.array(img.convert("HSV"))

        # Extract HSV channels
        h = img_hsv[:, :, 0]  # Hue: 0-255 (0=red, ~128=cyan, ~170=blue)
        s = img_hsv[:, :, 1]  # Saturation: 0-255
        v = img_hsv[:, :, 2]  # Value: 0-255

        # Detect cyan/blue hues (hue roughly 100-170 in 0-255 scale)
        # Cyan is around 128, blue is around 170
        # Need some saturation to avoid grays
        mask = (h >= 100) & (h <= 175) & (s >= 30) & (v >= 50)

        # Expand mask to include neighboring pixels (8-connected)
        expanded_mask = np.copy(mask)
        height, width = mask.shape

        # Shift mask in all 8 directions and combine
        for dy in [-1, 0, 1]:
            for dx in [-1, 0, 1]:
                if dy == 0 and dx == 0:
                    continue
                shifted = np.zeros_like(mask)
                src_y = slice(max(0, -dy), height - max(0, dy))
                src_x = slice(max(0, -dx), width - max(0, dx))
                dst_y = slice(max(0, dy), height - max(0, -dy))
                dst_x = slice(max(0, dx), width - max(0, -dx))
                shifted[dst_y, dst_x] = mask[src_y, src_x]
                expanded_mask |= shifted

        # Apply replacement color
        img_array[expanded_mask] = replacement_color

        # Save to output directory
        result = Image.fromarray(img_array)
        result.save(output_path / png_file.name)

    print(f"Done! Processed images saved to {output_dir}")


if __name__ == "__main__":
    remove_colored_lines()
