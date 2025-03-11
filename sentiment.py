from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import re
import unicodedata

def clean_text(text):
    """
    Clean the text by removing URLs, emojis, special characters, and extra whitespace
    Ensures pure text-based analysis
    """
    # Remove URLs
    text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)
    
    # Remove emojis and special characters
    text = ''.join(c for c in text if not unicodedata.category(c).startswith('So'))
    
    # Remove all non-alphanumeric characters except spaces
    text = re.sub(r'[^\w\s]', '', text)
    
    # Convert to lowercase for consistency
    text = text.lower()
    
    # Remove extra whitespace
    text = ' '.join(text.split())
    
    return text

def calculate_confidence(scores, compound_score):
    """
    Calculate confidence score based on VADER scores
    Returns a percentage between 0-100
    """
    # Get the dominant score (positive, negative, or neutral)
    max_score = max(scores["pos"], scores["neg"], scores["neu"])
    
    # Calculate base confidence from the strength of the compound score
    compound_confidence = abs(compound_score) * 100
    
    # Calculate score distribution confidence
    score_confidence = max_score * 100
    
    # Weighted average of both confidence measures
    final_confidence = (compound_confidence * 0.7 + score_confidence * 0.3)
    
    # Cap at 100 and round to 2 decimal places
    return min(round(final_confidence, 2), 100)

def analyze_sentiment(text):
    """
    Analyze the sentiment of text using VADER sentiment analyzer.
    Pure text-based analysis without emoji consideration.
    """
    analyzer = SentimentIntensityAnalyzer()
    
    # Clean the text thoroughly
    cleaned_text = clean_text(text)
    
    # Get sentiment scores from pure text
    scores = analyzer.polarity_scores(cleaned_text)
    
    # Determine sentiment category with adjusted thresholds
    compound_score = scores['compound']
    
    if compound_score >= 0.05:
        sentiment = "positive"
    elif compound_score <= -0.05:
        sentiment = "negative"
    else:
        sentiment = "neutral"
    
    # Calculate confidence score
    confidence = calculate_confidence(scores, compound_score)
    
    return {
        "text": cleaned_text,
        "sentiment": sentiment,
        "confidence": confidence,
        "scores": {
            "positive": scores["pos"],
            "negative": scores["neg"],
            "neutral": scores["neu"],
            "compound": scores["compound"]
        }
    }