import yt_dlp
import os

def download_video_ydl(link: str) -> None:
    """
    Downloads a video from a link
    """
    os.system("yt-dlp --rm-cache-dir")
    ydl_opts = {
        "outtmpl": "video.mp4",
        "format": "bestvideo+bestaudio/best",
        "merge_output_format": "mp4",
        "nocheckcertificate": True,
        "quiet": True,
        "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
        "socket_timeout": 10 
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([link])
        print("Download complete")
    except Exception as e:
        print(f"Error occurred during download: {str(e)}")