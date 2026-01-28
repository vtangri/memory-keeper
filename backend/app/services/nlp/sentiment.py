try:
    from textblob import TextBlob
    from nltk.sentiment import SentimentIntensityAnalyzer
    import nltk
except ImportError:
    TextBlob = None
    SentimentIntensityAnalyzer = None
    nltk = None
import logging
from typing import Dict, List, Any
import math

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SentimentAnalyzer:
    """
    Analyzes emotional tone of elderly narratives.
    Combines VADER (rule-based) and TextBlob (polarity) with custom heuristics
    for 'Nostalgia' and 'Sensitive Topics'.
    """

    def __init__(self):
        self.sia = None
        
        if nltk and SentimentIntensityAnalyzer:
            # Ensure VADER lexicon is downloaded
            try:
                nltk.data.find('sentiment/vader_lexicon.zip')
            except LookupError:
                logger.info("Downloading VADER lexicon...")
                nltk.download('vader_lexicon', quiet=True)
            self.sia = SentimentIntensityAnalyzer()
        else:
            logger.warning("NLTK/VADER not available. Sentiment analysis will be dummy.")
        
        # Heuristics for unique emotional states
        self.nostalgia_markers = [
            "back in the day", "used to", "remember when", "good old days", 
            "miss those", "cherish", "unforgettable"
        ]
        
        self.sensitive_markers = [
            "died", "passed away", "funeral", "accident", "lost him", "lost her",
            "hospital", "pain", "suffered", "cried", "hurt", "scared"
        ]

    def _detect_custom_emotion(self, text: str, markers: List[str]) -> float:
        """
        Simple frequency-based score for custom emotional categories.
        Returns a score between 0.0 and 1.0 (normalized roughly).
        """
        text_lower = text.lower()
        count = sum(1 for marker in markers if marker in text_lower)
        # S-curve normalization: 1 match -> 0.5, 3 matches -> 0.95
        if count == 0: return 0.0
        return 1.0 - (0.5 ** count)

    def analyze(self, text: str) -> Dict[str, Any]:
        """
        Perform comprehensive sentiment analysis on a segment of text.
        """
        if not text:
            return {"sentiment": "neutral", "scores": {}, "flags": []}

        # 1. Baseline Sentiment (VADER)
        # compound score: -1 (negative) to +1 (positive)
        vader_scores = {'compound': 0.0, 'pos': 0.0, 'neg': 0.0, 'neu': 1.0}
        if self.sia:
            vader_scores = self.sia.polarity_scores(text)
        
        # 2. Subjectivity (TextBlob)
        # 0.0 (objective) to 1.0 (subjective)
        subjectivity = 0.5
        if TextBlob:
            blob = TextBlob(text)
            subjectivity = blob.sentiment.subjectivity
        
        # 3. Custom Dimensions
        nostalgia_score = self._detect_custom_emotion(text, self.nostalgia_markers)
        trauma_score = self._detect_custom_emotion(text, self.sensitive_markers)
        
        # 4. Classification Logic
        compound = vader_scores['compound']
        
        primary_tone = "NEUTRAL"
        if trauma_score > 0.5:
            primary_tone = "SENSITIVE/SAD"
        elif nostalgia_score > 0.5 and compound > 0:
            primary_tone = "NOSTALGIC_POSITIVE"
        elif nostalgia_score > 0.5 and compound < 0:
            primary_tone = "NOSTALGIC_MELANCHOLY"
        elif compound >= 0.5:
            primary_tone = "POSITIVE"
        elif compound <= -0.5:
            primary_tone = "NEGATIVE"
        
        return {
            "primary_tone": primary_tone,
            "scores": {
                "compound": compound,
                "pos": vader_scores['pos'],
                "neg": vader_scores['neg'],
                "neu": vader_scores['neu'],
                "subjectivity": subjectivity,
                "nostalgia": nostalgia_score,
                "trauma_sensitivity": trauma_score
            },
            "is_sensitive": trauma_score > 0.3 or compound < -0.6
        }

    def analyze_conversation_flow(self, segments: List[str]) -> List[float]:
        """
        Generates an 'emotional journey map' by tracking the compound score
        across a list of conversation turns.
        """
        if not self.sia: return [0.0] * len(segments)
        return [self.sia.polarity_scores(seg)['compound'] for seg in segments]

if __name__ == "__main__":
    analyzer = SentimentAnalyzer()
    
    samples = [
        "I remember the summer of '69, it was the best time of my life. We played outside all day.",
        "Then my brother got sick and passed away. It was a very dark winter.",
        "I just had oatmeal for breakfast."
    ]
    
    for s in samples:
        print(f"Text: {s[:50]}...")
        print(f"Analysis: {analyzer.analyze(s)}\n")
