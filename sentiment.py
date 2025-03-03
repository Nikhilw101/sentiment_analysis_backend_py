import nltk
import re
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from textblob import TextBlob  # Adding ensemble method
import emoji

nltk.download('vader_lexicon', quiet=True)
nltk.download('punkt', quiet=True)

# Enhanced preprocessing patterns
URL_PATTERN = re.compile(r'https?\S+|www\.\S+')
HASHTAG_PATTERN = re.compile(r'#\w+')
SPECIAL_CHARS = re.compile(r'[^\w\s!?.,]')
REPEAT_CHARS = re.compile(r'(.)\1{2,}')

# Initialize analyzers
vader = SentimentIntensityAnalyzer()

# Expanded custom lexicon
LEXICON_UPDATES = {
    **{e: 4.0 for e in ['🔥', '❤️', '👍', '🎉']},
    **{e: -4.0 for e in ['💩', '👎', '😡', '🤮']},
    'epic': 3.5,
    'sucks': -3.0,
    'rofl': 2.7,
    'meh': -1.8,
    'banger': 3.2,
    'cringe': -2.5,
    'based': 2.0,
    'mid': -0.5,
    'woke': -1.0  # Context-dependent
}
vader.lexicon.update(LEXICON_UPDATES)

def preprocess(text):
    """Advanced text preprocessing"""
    text = emoji.demojize(text)  # Convert emojis to text
    text = URL_PATTERN.sub('', text)
    text = HASHTAG_PATTERN.sub('', text)
    text = SPECIAL_CHARS.sub('', text)
    text = REPEAT_CHARS.sub(r'\1', text)  # Reduce repeated chars
    text = text.lower().strip()
    return text

def analyze_sentiment(text):
    """Ensemble method combining VADER and TextBlob"""
    processed = preprocess(text)
    
    # VADER analysis
    vader_scores = vader.polarity_scores(processed)
    
    # TextBlob analysis
    blob = TextBlob(processed)
    tb_polarity = blob.sentiment.polarity
    tb_subjectivity = blob.sentiment.subjectivity
    
    # Combined score
    combined = (vader_scores['compound'] * 0.7) + (tb_polarity * 0.3)
    
    # Sentiment determination
    thresholds = {
        'positive': 0.15,
        'negative': -0.15,
        'neutral_low': -0.05,
        'neutral_high': 0.05
    }
    
    if combined > thresholds['positive']:
        sentiment = 'positive'
    elif combined < thresholds['negative']:
        sentiment = 'negative'
    elif thresholds['neutral_low'] <= combined <= thresholds['neutral_high']:
        sentiment = 'neutral'
    else:
        sentiment = 'mixed'
    
    return {
        'sentiment': sentiment,
        'confidence': abs(combined),
        'vader': vader_scores,
        'textblob': {'polarity': tb_polarity, 'subjectivity': tb_subjectivity},
        'processed_text': processed
    }