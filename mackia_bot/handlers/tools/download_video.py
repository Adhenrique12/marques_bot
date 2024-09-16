import yt_dlp


async def get_video_resolutions(url: str):
    ydl_opts = {
        'listformats': True,
    }
    format_ids = []
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            info_dict = ydl.extract_info(url, download=False)
            formats = info_dict.get('formats', [])
            for f in formats:
                format_id = f['format_id']
                format_ids.append(format_id)
                print(f"Format ID: {format_id}, Resolution: {f.get('resolution')}, Size: {f.get('filesize') or 'Unknown'}")
        except yt_dlp.utils.DownloadError as e:
            print(f"DownloadError: {e}")
        except yt_dlp.utils.ExtractorError as e:
            print(f"ExtractorError: {e}")
        except yt_dlp.utils.PostProcessingError as e:
            print(f"PostProcessingError: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
    return format_ids



async def download_video_ydl(url: str,format_id: str, event, client, entity):
    """
    Downloads a video from a link
    """
    msg = await event.respond('Downloading video ...')


    ydl_opts = {
        'format' : format_id,
        'outtmpl' : '%(title)s.%(ext)s',
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
            await client.delete_messages(entity, msg)
            return filename, info
    except Exception as e:
        await client.edit_message(entity, msg.id, text=f"Error occurred during download: {str(e)}")