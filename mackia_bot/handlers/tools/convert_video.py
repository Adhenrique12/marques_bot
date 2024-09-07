import ffmpeg

def convert_video(input_file):
    output_file = "output.mp4"
    try:
        # Get video metadata
        probe = ffmpeg.probe(input_file)
        video_stream = next((stream for stream in probe['streams'] if stream['codec_type'] == 'video'), None)
        audio_stream = next((stream for stream in probe['streams'] if stream['codec_type'] == 'audio'), None)
        # If the video width is greater than 640, then convert
        if video_stream is not None and video_stream['width'] > 640:
            (
                ffmpeg
                .input(input_file)
                #.filter('scale', 640, -2)
                .output(output_file, vcodec='libx264', acodec='copy', movflags='faststart', r=30, map='0', preset='ultrafast', crf=30)
                .run(overwrite_output=True)
            )
        else:
            # Check if the input is a GIF
            if video_stream['codec_name'] == 'gif':
                (
                    ffmpeg
                    .input(input_file)
                    .output(output_file, vcodec='libx264', acodec='aac' if audio_stream else None)
                    .run(overwrite_output=True)
                )
            else:
                (
                    ffmpeg
                    .input(input_file)
                    .output(output_file, vcodec='copy', acodec='copy', movflags='faststart', r=30, map='0', preset='ultrafast')
                    .run(overwrite_output=True)
                )
    except ffmpeg.Error as e:
        print(f"An error occurred during video conversion: {e.stderr.decode('utf-8')}")

