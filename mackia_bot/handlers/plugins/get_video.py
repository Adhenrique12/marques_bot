from telethon import events
from telethon.tl.types import DocumentAttributeVideo
import yt_dlp
import ffmpeg
import subprocess
import os
from handlers.tools import convert_size, clear

convert = convert_size.convert_size



@events.register(events.NewMessage(pattern='/down (.+)'))
async def handler(event):
    clear.clear()
    entity = await event.get_chat()
    client = event.client
    url = event.pattern_match.group(1)

    msg = await event.respond('Downloading video ...')

    ydl_opts = {
        'format' : 'best',
        'outtmpl' : '%(title)s.%(ext)s',
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        video_file = ydl.prepare_filename(info)

    # Convert video to MP4 format suitable for Telegram
    msg = await client.edit_message(entity, msg.id, text="Converting ...")
    output_file = 'output.mp4'
    subprocess.run(['ffmpeg', '-i', video_file, '-c:v', 'libx264', '-c:a', 'aac', '-strict', 'experimental', output_file])

    probe = ffmpeg.probe(output_file)
    video_streams = [stream for stream in probe['streams'] if stream['codec_type'] == 'video']
    if not video_streams:
        raise ValueError('No video stream found')

    video_stream = video_streams[0]
    width = int(video_stream['width'])
    height = int(video_stream['height'])
    duration = float(probe['format']['duration'])

    msg = await client.edit_message(entity, msg.id, text="Uploading ...")

    async def progress_callback(current, total):
            message = await client.get_messages(entity, ids=msg.id)

            percent = (current / total) * 100
            upload_text = None

            if 20.0 < percent < 30.0:
                upload_text = f"'Uploaded 1/4 out of', {convert(total)}"
            elif 50.0 < percent < 60.0:
                upload_text = f"'Uploaded 2/4 out of', {convert(total)}"
            elif 70.0 < percent < 80.0:
                upload_text = f"'Uploaded 3/4 out of', {convert(total)}"
            elif 80.0 < percent < 95.0:
                upload_text = f"'Uploaded 4/4 out of', {convert(total)}"

            if upload_text and message.text != upload_text:
                await client.edit_message(entity, msg.id, text=upload_text)
    
    await client.send_file(event.chat_id, 
                           output_file, 
                           caption=info['title'], 
                           progress_callback=progress_callback,
                           attributes=(
                                DocumentAttributeVideo(
                                    int(float(duration)),
                                    width,
                                    height,
                                    supports_streaming=True
                                ),
                           )
            )
    await client.delete_messages(entity, msg)
    os.remove(video_file)
    os.remove(output_file)