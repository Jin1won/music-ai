import os
from yt_dlp import YoutubeDL

def export_mp3_from_url(url, file_name):
    download_dir = os.path.join(os.getcwd(), 'downloads')
    
    os.makedirs(download_dir, exist_ok=True)
    file_path = os.path.join(download_dir, file_name)
    ydl_opts = {
        'format': 'bestaudio',
        'outtmpl': file_path + '.%(ext)s',
        'nocheckcertificate': True,
        "noplaylist": True,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '320'
        }],
        'audio_quality': 0
    }
    with YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])