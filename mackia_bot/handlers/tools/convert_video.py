import asyncio
import subprocess

async def convert_video(client, entity, msg, video_file):
    try:
        msg = await client.edit_message(entity, msg.id, text="Converting ...")
        output_file = 'output.mp4'
        
        # Run ffmpeg asynchronously with your specified command
        process = await asyncio.create_subprocess_exec(
            'ffmpeg', '-i', video_file, '-max_muxing_queue_size', '9999', '-c:v', 'libx264', '-crf', '28', 
            '-maxrate', '3M', '-preset', 'ultrafast', '-flags', '+global_header', '-pix_fmt', 'yuv420p', 
            '-profile:v', 'baseline', '-movflags', '+faststart', '-c:a', 'aac', '-ac', '2', output_file,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )

        # Track progress
        while True:
            line = await process.stderr.readline()
            if not line:
                break
            # Update progress message here if needed
            print(line.decode('utf-8').strip())

        await process.wait()

        if process.returncode == 0:
            await client.edit_message(entity, msg.id, text="Conversion successful!")
        else:
            await client.edit_message(entity, msg.id, text="Conversion failed!")

    except Exception as e:
        await client.edit_message(entity, msg.id, text=f"An error occurred: {str(e)}")

# Usage
# await convert_video(client, entity, msg, video_file)


