import requests
from config import YOUTUBE_API_KEY
from datetime import datetime

YOUTUBE_API_URL = "https://www.googleapis.com/youtube/v3/commentThreads"
YOUTUBE_VIDEO_URL = "https://www.googleapis.com/youtube/v3/videos"

def get_video_details(video_id):
    """
    Fetches video title and other details for a given YouTube video ID.
    """
    params = {
        "key": YOUTUBE_API_KEY,
        "part": "snippet",
        "id": video_id
    }
    
    response = requests.get(YOUTUBE_VIDEO_URL, params=params)
    if response.status_code == 200:
        data = response.json()
        if data.get("items"):
            return {
                "title": data["items"][0]["snippet"]["title"],
                "publishedAt": data["items"][0]["snippet"]["publishedAt"]
            }
    return None

def fetch_comments(video_id, max_results=1000):
    """
    Fetches comments (with text and like counts) for a given YouTube video ID.
    Returns comments sorted by relevance and includes timestamps.
    """
    comments = []
    params = {
        "key": YOUTUBE_API_KEY,
        "textFormat": "plainText",
        "part": "snippet",
        "videoId": video_id,
        "maxResults": 100,  # Maximum allowed per page
        "order": "relevance"  # Sort by relevance (considers likes and engagement)
    }
    nextPageToken = None
    fetched = 0

    while True:
        if nextPageToken:
            params["pageToken"] = nextPageToken

        response = requests.get(YOUTUBE_API_URL, params=params)
        if response.status_code != 200:
            break

        data = response.json()
        items = data.get("items", [])
        for item in items:
            snippet = item["snippet"]["topLevelComment"]["snippet"]
            comment = {
                "text": snippet.get("textDisplay", ""),
                "likeCount": snippet.get("likeCount", 0),
                "publishedAt": snippet.get("publishedAt", ""),
                "updatedAt": snippet.get("updatedAt", "")
            }
            comments.append(comment)
            fetched += 1
            if fetched >= max_results:
                break

        if fetched >= max_results:
            break

        nextPageToken = data.get("nextPageToken")
        if not nextPageToken:
            break

    # Sort comments by likes and date
    comments.sort(key=lambda x: (-x["likeCount"], x["publishedAt"]), reverse=True)
    
    return comments
