import os
import json
import threading
import yt_dlp
import customtkinter as ctk
from tkinter import filedialog, messagebox

CONFIG_FILE = "config.json"


# ---------------- CONFIG ----------------
def load_config():
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {"last_folder": os.path.expanduser("~")}


def save_config(cfg):
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(cfg, f, indent=4)


config = load_config()


# ---------------- DOWNLOAD LOGIC ----------------
def select_folder():
    folder = filedialog.askdirectory()
    if folder:
        path_entry.delete(0, "end")
        path_entry.insert(0, folder)
        config["last_folder"] = folder
        save_config(config)


def hook(d):
    if d["status"] == "downloading":
        percent_str = d.get("_percent_str", "0%").replace("%", "")
        try:
            percent = float(percent_str)
        except ValueError:
            percent = 0
        progress_bar.set(percent / 100)
        progress_label.configure(text=f"{percent:.1f}% - {d.get('filename', '')[-30:]}")
    elif d["status"] == "finished":
        progress_bar.set(1)
        progress_label.configure(text="Download complete!")


def download_videos():
    urls_text = urls_entry.get("1.0", "end").strip()
    output_path = path_entry.get().strip()
    quality = quality_dropdown.get()
    output_format = format_dropdown.get()

    if not urls_text:
        messagebox.showerror("Error", "Please enter one or more URLs.")
        return
    if not output_path:
        messagebox.showerror("Error", "Please select a download folder.")
        return

    urls = [u.strip() for u in urls_text.splitlines() if u.strip()]
    download_button.configure(state="disabled")
    progress_label.configure(text="Starting...")
    progress_bar.set(0)

    threading.Thread(
        target=run_downloads,
        args=(urls, output_path, quality, output_format),
        daemon=True,
    ).start()


def run_downloads(urls, output_path, quality, output_format):
    try:
        is_audio = output_format == "MP3"
        ydl_opts = {
            "outtmpl": os.path.join(output_path, "%(title)s.%(ext)s"),
            "progress_hooks": [hook],
            "format": quality_formats[quality] if not is_audio else "bestaudio/best",
            "merge_output_format": "mp4" if output_format == "MP4" else None,
            "postprocessors": [],
        }

        if is_audio:
            ydl_opts["postprocessors"].append(
                {
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "mp3",
                    "preferredquality": "192",
                }
            )
        elif output_format == "MP4":
            ydl_opts["postprocessors"].append(
                {"key": "FFmpegVideoConvertor", "preferedformat": "mp4"}
            )

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            for url in urls:
                progress_label.configure(text=f"Downloading: {url}")
                ydl.download([url])

        messagebox.showinfo("Success", f"All downloads complete! ({len(urls)} items)")
    except Exception as e:
        messagebox.showerror("Error", str(e))
    finally:
        download_button.configure(state="normal")
        progress_label.configure(text="")


# ---------------- UI ----------------
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

root = ctk.CTk()
root.title("🎥 Advanced Video Downloader")
root.geometry("600x520")
root.resizable(False, False)

ctk.CTkLabel(root, text="Video URLs (one per line):", anchor="w").pack(pady=(10, 5))
urls_entry = ctk.CTkTextbox(root, width=560, height=100)
urls_entry.pack(pady=5)

ctk.CTkLabel(root, text="Download Folder:", anchor="w").pack(pady=(10, 5))
path_frame = ctk.CTkFrame(root)
path_frame.pack(pady=5)
path_entry = ctk.CTkEntry(path_frame, width=440)
path_entry.insert(0, config.get("last_folder", ""))
path_entry.pack(side="left", padx=(5, 10))
ctk.CTkButton(path_frame, text="Browse", command=select_folder, width=80).pack(
    side="left"
)

ctk.CTkLabel(root, text="Quality:", anchor="w").pack(pady=(10, 5))
quality_formats = {
    "Best Available": "bestvideo+bestaudio/best",
    "1080p": "bestvideo[height<=1080]+bestaudio/best[height<=1080]",
    "720p": "bestvideo[height<=720]+bestaudio/best[height<=720]",
    "480p": "bestvideo[height<=480]+bestaudio/best[height<=480]",
    "Audio Only (best)": "bestaudio/best",
}
quality_dropdown = ctk.CTkOptionMenu(root, values=list(quality_formats.keys()))
quality_dropdown.set("Best Available")
quality_dropdown.pack(pady=5)

ctk.CTkLabel(root, text="Output Format:", anchor="w").pack(pady=(10, 5))
format_dropdown = ctk.CTkOptionMenu(root, values=["MP4", "WebM", "MP3"])
format_dropdown.set("MP4")
format_dropdown.pack(pady=5)

download_button = ctk.CTkButton(
    root, text="⬇️  Start Download", command=download_videos, width=220, height=40
)
download_button.pack(pady=15)

progress_bar = ctk.CTkProgressBar(root, width=500)
progress_bar.set(0)
progress_bar.pack(pady=5)

progress_label = ctk.CTkLabel(root, text="")
progress_label.pack(pady=5)

root.mainloop()
