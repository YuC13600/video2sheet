import os
import argparse
from pathlib import Path
from PIL import Image
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
import io


def create_sheet_pdf(frames_dir='sheet_music_frames', output_pdf='sheet_music.pdf', song_name=None):
    """
    Combine sheet music frame images into a single PDF with optional song title

    Parameters:
        frames_dir: Directory containing frame PNG files
        output_pdf: Output PDF filename
        song_name: Optional song name to display at top of first page
    """

    # Get all PNG files sorted by name
    frame_files = sorted([f for f in os.listdir(frames_dir) if f.endswith('.png')])

    if not frame_files:
        print(f"No PNG files found in {frames_dir}")
        return

    print(f"Found {len(frame_files)} frames")

    # Load first frame to get dimensions
    first_frame_path = os.path.join(frames_dir, frame_files[0])
    first_image = Image.open(first_frame_path)
    frame_width, frame_height = first_image.size

    print(f"Frame dimensions: {frame_width}x{frame_height}")

    # Use portrait orientation (A4: 8.27" x 11.69")
    pdf_width = 8.27 * 72  # A4 width in points (portrait)
    pdf_height = 11.69 * 72  # A4 height in points

    # Calculate scaling factor to fit frame width to PDF width with margins
    margin = 36  # 0.5 inch margins
    available_width = pdf_width - (2 * margin)
    scale_factor = available_width / frame_width
    scaled_frame_height = frame_height * scale_factor

    # Create PDF
    c = canvas.Canvas(output_pdf, pagesize=(pdf_width, pdf_height))

    # Add title on first page if song_name provided
    y_position = pdf_height - margin

    if song_name:
        # Add song title
        c.setFont("Helvetica-Bold", 24)
        title_width = c.stringWidth(song_name, "Helvetica-Bold", 24)
        c.drawString((pdf_width - title_width) / 2, y_position, song_name)
        y_position -= 40  # Space after title

    # Add frames to PDF
    for i, frame_file in enumerate(frame_files):
        frame_path = os.path.join(frames_dir, frame_file)
        img = Image.open(frame_path)

        # Check if we need a new page
        if y_position - scaled_frame_height < margin:
            c.showPage()
            y_position = pdf_height - margin

        # Convert PIL Image to ImageReader for reportlab
        img_buffer = io.BytesIO()
        img.save(img_buffer, format='PNG')
        img_buffer.seek(0)
        img_reader = ImageReader(img_buffer)

        # Draw image on PDF
        c.drawImage(img_reader,
                   margin,
                   y_position - scaled_frame_height,
                   width=available_width,
                   height=scaled_frame_height)

        y_position -= scaled_frame_height + 10  # Add small spacing between frames

        if (i + 1) % 5 == 0:
            print(f"Processed {i + 1}/{len(frame_files)} frames...")

    # Save PDF
    c.save()

    print(f"\nPDF created successfully: {output_pdf}")
    print(f"Total frames: {len(frame_files)}")
    if song_name:
        print(f"Song name: {song_name}")


def main():
    parser = argparse.ArgumentParser(description='Combine sheet music frames into a PDF')
    parser.add_argument('--frames_dir',
                       default='sheet_music_frames',
                       help='Directory containing frame PNG files (default: sheet_music_frames)')
    parser.add_argument('--output',
                       default='sheet_music.pdf',
                       help='Output PDF filename (default: sheet_music.pdf)')
    parser.add_argument('--song_name',
                       help='Song name to display at top of first page')

    args = parser.parse_args()

    create_sheet_pdf(args.frames_dir, args.output, args.song_name)


if __name__ == "__main__":
    main()
