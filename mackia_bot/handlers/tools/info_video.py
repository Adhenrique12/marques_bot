import ffmpeg


async def info_video(output_file):
    probe = ffmpeg.probe(output_file)
    video_streams = [stream for stream in probe['streams'] if stream['codec_type'] == 'video']
    if not video_streams:
        raise ValueError('No video stream found')

    video_stream = video_streams[0]
    width = int(video_stream['width'])
    height = int(video_stream['height'])
    duration = float(probe['format']['duration'])

    return width, height, duration