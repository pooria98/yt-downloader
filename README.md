# 🎥 Simple Video Downloader (yt-dlp GUI)

A simple and modern GUI video downloader built with [yt-dlp](https://github.com/yt-dlp/yt-dlp) and [customtkinter](https://github.com/TomSchimansky/CustomTkinter).

## ✨ Features

- Modern dark UI
- Batch download (multiple URLs)
- Quality selection (1080p, 720p, etc.)
- MP4 / WebM / MP3 output
- Progress bar + status
- Remembers last output folder

## 🚀 Installation

### Executable (windows)

Just download the zip file from [releases](https://github.com/pooria98/yt-downloader/releases/tag/v1.0) and simply run video_downloader.exe

### Manual usage with python (cross platform)

```bash
git clone https://github.com/yourusername/yt-downloader.git
cd yt-downloader
pip install -r requirements.txt
python video_downloader.py
```

You need FFmpeg binaries on PATH if you want to output to mp4 format.

### FFmpeg

This application uses FFmpeg for media processing.  
FFmpeg is licensed under the GNU General Public License v3.  
Source: https://ffmpeg.org/
