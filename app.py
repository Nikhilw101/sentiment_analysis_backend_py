from flask import Flask, request, jsonify
from youtube_api import fetch_comments, get_video_details
from sentiment import analyze_sentiment
from flask_cors import CORS  # Import Flask-CORS
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route("/api/comments", methods=["GET"])
def get_comments():
    video_id = request.args.get("videoId")
    logger.info(f"Received request for video ID: {video_id}")
    
    if not video_id:
        logger.error("No video ID provided")
        return jsonify({"error": "Parameter 'videoId' is required."}), 400

    try:
        max_results = int(request.args.get("maxResults", 1000))
    except ValueError:
        max_results = 1000

    try:
        # Get video details first
        logger.info(f"Fetching video details for {video_id}")
        video_details = get_video_details(video_id)
        if not video_details:
            logger.error(f"Could not fetch video details for {video_id}")
            return jsonify({"error": "Could not fetch video details."}), 404

        # Fetch and process comments
        logger.info(f"Fetching comments for {video_id}")
        comments = fetch_comments(video_id, max_results)
        if not comments:
            logger.error(f"No comments found for {video_id}")
            return jsonify({"error": "No comments found for this video."}), 404

        processed_comments = []
        sentiment_stats = {
            "positive": 0,
            "negative": 0,
            "neutral": 0
        }

        logger.info(f"Processing {len(comments)} comments")
        for comment in comments:
            sentiment_result = analyze_sentiment(comment["text"])
            sentiment_stats[sentiment_result["sentiment"]] += 1
            
            processed_comment = {
                "text": comment["text"],
                "likeCount": comment["likeCount"],
                "publishedAt": comment["publishedAt"],
                "sentiment": sentiment_result["sentiment"],
                "scores": sentiment_result["scores"]
            }
            processed_comments.append(processed_comment)

        response_data = {
            "videoId": video_id,
            "videoTitle": video_details["title"],
            "videoPublishedAt": video_details["publishedAt"],
            "comments": processed_comments,
            "sentimentStats": sentiment_stats
        }
        
        logger.info(f"Successfully processed video {video_id} with {len(processed_comments)} comments")
        return jsonify(response_data)

    except Exception as e:
        logger.error(f"Error processing request for {video_id}: {str(e)}")
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(debug=True)
