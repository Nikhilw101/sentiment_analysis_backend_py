import requests
from config import YOUTUBE_API_KEY

YOUTUBE_API_URL = "https://www.googleapis.com/youtube/v3/commentThreads"

def fetch_comments(video_id, max_results=100):
    """
    Fetches comments (with text and like counts) for a given YouTube video ID.
    """
    comments = []
    params = {
        "key": YOUTUBE_API_KEY,
        "textFormat": "plainText",
        "part": "snippet",
        "videoId": video_id,
        "maxResults": 50  # Maximum per page
    }
    nextPageToken = None
    fetched = 0

    while True:
        if nextPageToken:
            params["pageToken"] = nextPageToken

        response = requests.get(YOUTUBE_API_URL, params=params)
        if response.status_code != 200:
            break  # Could add logging here

        data = response.json()
        items = data.get("items", [])
        for item in items:
            snippet = item["snippet"]["topLevelComment"]["snippet"]
            comment = {
                "text": snippet.get("textDisplay", ""),
                "likeCount": snippet.get("likeCount", 0)
            }
            comments.append(comment)
            fetched += 1
            if fetched >= max_results:
                return comments

        nextPageToken = data.get("nextPageToken")
        if not nextPageToken:
            break

    return comments
