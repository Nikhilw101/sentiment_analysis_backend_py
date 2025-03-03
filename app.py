from flask import Flask, request, jsonify
from youtube_api import fetch_comments
from sentiment import analyze_sentiment
from flask_cors import CORS  # Import Flask-CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes
@app.route("/api/comments", methods=["GET"])
def get_comments():
    video_id = request.args.get("videoId")
    if not video_id:
        return jsonify({"error": "Parameter 'videoId' is required."}), 400

    try:
        max_results = int(request.args.get("maxResults", 100))
    except ValueError:
        max_results = 100

    comments = fetch_comments(video_id, max_results)
    processed_comments = []
    for comment in comments:
        sentiment_scores = analyze_sentiment(comment["text"])
        processed_comments.append({
            "text": comment["text"],
            "likeCount": comment["likeCount"],
            "sentiment": sentiment_scores["sentiment"],
            "scores": sentiment_scores
        })

    return jsonify({
        "videoId": video_id,
        "comments": processed_comments
    })

if __name__ == "__main__":
    app.run(debug=True)
