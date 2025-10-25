# video2sheet

Convert piano performance videos into printable sheet music PDFs.

## Overview

video2sheet extracts sheet music from piano tutorial videos and compiles them into a formatted PDF document. Perfect for capturing sheet music from YouTube tutorials, online lessons, or any video where sheet music is displayed on screen.

## Features

- ✂️ **Smart Frame Extraction** - Automatically crops sheet music region from videos
- ⏱️ **Time-based Sampling** - Extract frames at regular intervals (default: every 9 seconds)
- 📄 **PDF Generation** - Compile frames into a clean, printable A4 PDF
- 🎵 **Song Titles** - Add custom song names to your sheet music
- 🔧 **Frame Management** - Tools to renumber and organize extracted frames

## Requirements

- Python 3.13
- Conda package manager

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd video2sheet
```

2. Create the conda environment:
```bash
conda env create -f environment.yml
conda activate video2sheet
```

## Quick Start

```bash
# 1. Edit video2png.py (line 78) to point to your video file
# 2. Extract frames from video
python video2png.py

# 3. Generate PDF with song title
python frames2pdf.py --song_name "Your Song Name" --output "song.pdf"
```

## Detailed Usage

### Step 1: Extract Frames from Video

Edit `video2png.py` line 78 to specify your video file path:
```python
video_path = './your_video.webm'  # or .mp4, .avi, etc.
```

Then run:
```bash
python video2png.py
```

This will:
- Extract the upper half of each frame (where sheet music typically appears)
- Save one frame every 9 seconds by default
- Output frames to `sheet_music_frames/` directory

**Optional**: Adjust the extraction interval by modifying line 87:
```python
interval_seconds=9  # Change to desired interval
```

### Step 2: (Optional) Renumber Frames

If you manually add, remove, or reorder frames, use the renumber utility:

```bash
python renumber_frames.py
```

This ensures frames are numbered consecutively: `frame_00000.png`, `frame_00001.png`, etc.

### Step 3: Generate PDF

```bash
python frames2pdf.py --song_name "Song Title" --output "output.pdf"
```

**Arguments:**
- `--song_name` - Song title to display at top of first page (optional)
- `--output` - Output PDF filename (default: `sheet_music.pdf`)
- `--frames_dir` - Input frames directory (default: `sheet_music_frames`)

**Example:**
```bash
python frames2pdf.py --song_name "Clair de Lune" --output "clair_de_lune.pdf"
```

## Project Structure

```
video2sheet/
├── video2png.py          # Extract frames from video
├── renumber_frames.py    # Renumber frames consecutively
├── frames2pdf.py         # Generate PDF from frames
├── environment.yml       # Conda environment specification
├── environment-lock.yml  # Locked dependency versions
└── sheet_music_frames/   # Output directory for frames
```

## How It Works

1. **Frame Extraction** - `video2png.py` processes your video:
   - Calculates frame interval based on video FPS and desired time interval
   - Crops the upper half of each frame (adjustable in code)
   - Saves frames as PNG images

2. **Frame Processing** - `renumber_frames.py` (optional):
   - Scans for all frame PNG files
   - Renumbers them consecutively to fill any gaps
   - Uses temporary directory to avoid conflicts

3. **PDF Generation** - `frames2pdf.py`:
   - Loads all frames in order
   - Scales them to fit A4 portrait pages
   - Stacks them vertically with automatic page breaks
   - Adds optional song title at the top

## Tips

- **Video Format**: Works with most common video formats (.mp4, .webm, .avi, .mov)
- **Frame Interval**: Adjust based on how fast the sheet music scrolls (slower = longer interval)
- **Manual Editing**: You can manually delete unwanted frames or add missing ones before generating the PDF
- **Crop Ratio**: If your video shows sheet music in a different region, modify line 38 in `video2png.py`

## Troubleshooting

**Problem**: Frames show too much or too little of the video
- **Solution**: Adjust the crop ratio in `video2png.py` line 38. Change `height // 2` to a different fraction.

**Problem**: Too many/few frames extracted
- **Solution**: Adjust `interval_seconds` parameter in `video2png.py` line 87.

**Problem**: Frames have gaps in numbering
- **Solution**: Run `python renumber_frames.py` to fix numbering.

**Problem**: PDF pages are blank or images don't show
- **Solution**: Ensure frames exist in the correct directory and are valid PNG files.

## License

This repository is licensed under GPL-3.0. See [LICENSE](./LICENSE) for details.

## Contributing

Contributions are welcome! Please feel free to submit issues or pull requests.
