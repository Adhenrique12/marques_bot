from telethon import events, Button
from telethon.tl.types import DocumentAttributeVideo
import os
from handlers.tools import convert_size, clear, convert_video, download_video, info_video


convert = convert_size.convert_size


@events.register(events.NewMessage(pattern='/down (.+)'))
async def handler(event):
    clear.clear()
    entity = await event.get_chat()
    client = event.client
    url = event.pattern_match.group(1)
    msg_start = await event.reply("Start Download")

    #Select the resoluction of the video
    @client.on(events.CallbackQuery)
    async def callback(event):
        format_id = event.data.decode('utf-8')
        await client.delete_messages(entity, msg_op)
        
        # Download video and get the info(for the name)
        file_name, info = await download_video.download_video_ydl(url, format_id, event, client, entity)

        # Convert video to MP4 format suitable for Telegram
        output_file = await convert_video.convert_video(client, entity, msg_start, file_name)
    
        # Get info for telegram stream video player
        width, height, duration = await info_video.info_video(output_file)

        msg = await client.edit_message(entity, msg_start.id, text="Uploading ...")

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
        os.remove(file_name)
        os.remove(output_file)


    resolutions = await download_video.get_video_resolutions(url)
    buttons = [[Button.inline(res, res.encode('utf-8'))] for res in resolutions]
    msg_op = await event.respond("Escolha a resolução do vídeo:", buttons=buttons)
    


    # Download video and get the info(for the name)
    #video_file, info = await download_video.download_video_ydl(url, event, client, entity)

    