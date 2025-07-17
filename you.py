'''import yt_dlp

url = input("Enter YouTube video URL: ").strip()

options = {
    'format': 'mp4',  # Download single .mp4 stream, no merge needed
    'outtmpl': '%(title)s.%(ext)s',
    'noplaylist': True,
    'merge_output_format': 'mp4',
    'quiet': False,
}

try:
    with yt_dlp.YoutubeDL(options) as ydl:
        ydl.download([url])
    print("✅ Download complete!")
except Exception as e:
    print(f"❌ Error: {e}")
'''
'''
import yt_dlp
import tkinter as tk
from tkinter import filedialog, messagebox

def download_video():
    url = url_entry.get().strip()
    if not url:
        messagebox.showwarning("Missing URL", "Please enter a YouTube video URL.")
        return

    folder = filedialog.askdirectory(title="Select Download Folder")
    if not folder:
        return

    options = {
        'format': 'best[ext=mp4][height<=480]',  # Muxed formats only (video+audio), max 480p
        'outtmpl': folder + '/%(title)s.%(ext)s',
        'noplaylist': True,
        'quiet': False,
        'merge_output_format': None  # No ffmpeg merging
    }

    try:
        with yt_dlp.YoutubeDL(options) as ydl:
            ydl.download([url])
        messagebox.showinfo("Success", "✅ Download complete with audio!")
    except Exception as e:
        messagebox.showerror("Error", f"❌ Error: {e}")

# GUI Setup
root = tk.Tk()
root.title("YouTube Downloader (No ffmpeg)")
root.geometry("400x150")

tk.Label(root, text="Enter YouTube URL:").pack(pady=5)
url_entry = tk.Entry(root, width=50)
url_entry.pack(pady=5)

download_btn = tk.Button(root, text="Download", command=download_video)
download_btn.pack(pady=10)

root.mainloop()
'''

import yt_dlp
import tkinter as tk
from tkinter import filedialog, messagebox
import winsound  # For sound on Windows

def play_success_sound():
    winsound.MessageBeep(winsound.MB_ICONASTERISK)

def play_error_sound():
    winsound.MessageBeep(winsound.MB_ICONHAND)

def download_video():
    url = url_entry.get().strip()
    if not url:
        play_error_sound()
        messagebox.showwarning("Missing URL", "Please enter a YouTube video URL.")
        return

    folder = filedialog.askdirectory(title="Select Download Folder")
    if not folder:
        return

    download_type = download_var.get()

    # Format selection logic
    if download_type == "Video (480p)":
        format_str = 'best[ext=mp4][height<=480]'
    elif download_type == "Audio Only (mp3)":
        format_str = 'bestaudio[ext=m4a]/bestaudio'
    else:
        format_str = 'best[ext=mp4][height<=480]'

    postprocessors = []
    if download_type == "Audio Only (mp3)":
        postprocessors = [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }]

    options = {
        'format': format_str,
        'outtmpl': folder + '/%(title)s.%(ext)s',
        'noplaylist': True,
        'quiet': False,
        'merge_output_format': None,
        'postprocessors': postprocessors
    }

    try:
        with yt_dlp.YoutubeDL(options) as ydl:
            ydl.download([url])
        play_success_sound()
        messagebox.showinfo("Success", "✅ Download complete!")
    except Exception as e:
        play_error_sound()
        messagebox.showerror("Error", f"❌ Error: {e}")

# ---------------- GUI Setup ----------------
root = tk.Tk()
root.title("🎵 YouTube Downloader Pro")
root.geometry("500x250")
root.config(bg="#1e1e2f")

# Style
label_style = {"bg": "#1e1e2f", "fg": "#f0f0f0", "font": ("Arial", 12)}
entry_style = {"bg": "#29293d", "fg": "#ffffff", "insertbackground": "white", "font": ("Arial", 11)}

# Widgets
tk.Label(root, text="Enter YouTube URL:", **label_style).pack(pady=10)
url_entry = tk.Entry(root, width=50, **entry_style)
url_entry.pack(pady=5)

tk.Label(root, text="Choose format:", **label_style).pack(pady=5)
download_var = tk.StringVar(value="Video (480p)")
format_menu = tk.OptionMenu(root, download_var, "Video (480p)", "Audio Only (mp3)")
format_menu.config(font=("Arial", 11), bg="#3a3a5c", fg="white", width=20)
format_menu.pack(pady=5)

download_btn = tk.Button(root, text="⬇️ Download", command=download_video,
                         bg="#00b894", fg="white", font=("Arial", 12), width=20)
download_btn.pack(pady=20)

root.mainloop()
