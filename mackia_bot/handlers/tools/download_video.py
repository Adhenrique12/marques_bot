import yt_dlp

async def download_video_ydl(url: str, event, client, entity) -> None:
    """
    Downloads a video from a link
    """
    msg = await event.respond('Downloading video ...')

    ydl_opts = {
        'format' : 'best',
        'outtmpl' : '%(title)s.%(ext)s',
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = await ydl.extract_info(url, download=True)
            return await ydl.prepare_filename(info), info
        
        await client.edit_message(entity, msg.id, text="Download successful!")
    except Exception as e:
        await client.edit_message(entity, msg.id, text="Error occurred during download: {str(e)}")


        

    

    