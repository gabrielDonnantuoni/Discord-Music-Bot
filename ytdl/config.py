ytdl_format_options = {
    'format': 'bestaudio/best',
    # 'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'age_limit': 24,
    'no_warnings': True,
    'default_search': 'auto',
    # 'extractor_args': {'youtube': {'skip': ['dash', 'hls', 'thumbnails', 'description']}},
    'source_address': '0.0.0.0'  # bind to ipv4 since ipv6 addresses cause issues sometimes # noqa: E501
}

ffmpeg_options = {
    'options': '-vn'
}

yt_url_pattern = {
    'youtube#video': {
        'pattern':'https://www.youtube.com/watch?v=',
        'id': 'videoId'
    },
    'youtube#playlist': {
        'url': 'https://www.youtube.com/playlist?list=',
        'id': 'playlistId'
    },
}
