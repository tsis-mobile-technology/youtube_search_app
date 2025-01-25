from flask import Flask, request, jsonify
from yt_dlp import YoutubeDL

app = Flask(__name__)

def search_youtube_videos_with_ytdlp(search_term):
    """
    yt-dlp를 사용하여 YouTube 검색을 수행하고 상위 3개 영상의 URL을 반환합니다.

    Args:
        search_term (str): 검색어입니다.

    Returns:
        list: 최대 3개의 YouTube 영상 URL 목록입니다.
    """
    ydl_opts = {
        'noplaylist': True,
        'quiet': True,
        'extract_flat': 'in_playlist',
        'forceurl': True,
        'default_search': 'ytsearch',
    }

    with YoutubeDL(ydl_opts) as ydl:
        try:
            info_dict = ydl.extract_info(f"ytsearch3:{search_term}", download=False)
            entries = info_dict.get('entries', [])
            video_urls = [entry.get('url') for entry in entries if entry]
            return video_urls[:3]
        except Exception as e:
            print(f"Error during YouTube search with yt-dlp: {e}")
            return []

@app.route('/search', methods=['GET'])
def search():
    """
    검색어를 쿼리 파라미터로 받아 YouTube 검색을 수행하는 API 엔드포인트입니다.

    /search?query=<검색어>
    """
    search_term = request.args.get('query')

    if not search_term:
        return jsonify({'error': 'Missing search query parameter'}), 400

    video_urls = search_youtube_videos_with_ytdlp(search_term)

    if video_urls:
        return jsonify({'video_urls': video_urls})
    else:
        return jsonify({'error': 'No videos found or error during search'}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000) #  For production environments, consider using a robust server like Gunicorn or uWSGI