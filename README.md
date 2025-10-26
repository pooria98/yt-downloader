# 🎥 Youtube Downloader (yt-dlp GUI)

A simple GUI youtube downloader built with [yt-dlp](https://github.com/yt-dlp/yt-dlp) and [customtkinter](https://github.com/TomSchimansky/CustomTkinter).

## ✨ Features

- Batch download (multiple URLs)
- Quality selection (1080p, 720p, etc.)
- MP4 / WebM / MP3 output
- embedded subtitles
- embedded chapters as video bookmarks (for players like potplayer)
- Progress bar + status
- Remembers last options

## 🚀 Installation

### Executable

Just download the zip file from [releases](https://github.com/pooria98/yt-downloader/releases/tag/v1.0) and simply run video_downloader.exe

### Manual usage with python

have python installed on your machine

```bash
git clone https://github.com/yourusername/yt-downloader.git
cd yt-downloader
pip install -r requirements.txt
python video_downloader.py
```

You need FFmpeg binaries on PATH if you want to output to mp4 format.

## FFmpeg

This application uses FFmpeg for media processing.  
FFmpeg is licensed under the GNU General Public License v3.  
Source: https://ffmpeg.org/
