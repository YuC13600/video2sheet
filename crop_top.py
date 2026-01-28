"""Crop the top rows from sheet music frames."""

from pathlib import Path

from PIL import Image


def crop_top_rows(
    input_dir: str = "sheet_music_frames_noline",
    output_dir: str = "final_frames",
    rows_to_crop: int = 24,
) -> None:
    """
    Remove the top N pixel rows from each image.

    Args:
        input_dir: Directory containing input PNG images.
        output_dir: Directory to save cropped images.
        rows_to_crop: Number of pixel rows to remove from the top.
    """
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

        img = Image.open(png_file)
        width, height = img.size

        # Crop: (left, upper, right, lower)
        cropped = img.crop((0, rows_to_crop, width, height))
        cropped.save(output_path / png_file.name)

    print(f"Done! Cropped images saved to {output_dir}")


if __name__ == "__main__":
    crop_top_rows()
