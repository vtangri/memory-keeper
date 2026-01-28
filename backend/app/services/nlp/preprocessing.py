import re
import spacy
from nltk.stem import PorterStemmer
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TextPreprocessor:
    """
    A module for preprocessing text specifically designer for elderly speech patterns.
    Implements cleaning, tokenization, stemming, and lemmatization.
    """

    def __init__(self, model_name="en_core_web_sm"):
        """
        Initialize the preprocessor with spaCy model and NLTK stemmer.
        """
        self.nlp = None
        self.stemmer = None
        
        try:
            self.nlp = spacy.load(model_name)
        except (OSError, ImportError, NameError):
            logger.warning(f"spaCy model '{model_name}' not found. Text processing will be limited.")

        try:
            self.stemmer = PorterStemmer()
        except (ImportError, NameError):
             logger.warning("NLTK Stemmer not found.")
        
        # Regex patterns for elderly speech / conversational filler
        self.filler_patterns = [
            r"\b(um|uh|er|ah|like|you know|i mean)\b",  # Common fillers
            r"\b(w-w-wait|th-th-then)\b",               # Stutters (simplistic)
        ]
        self.repetition_pattern = r"(\b\w+\b)( \1\b)+"  # Word repetition "very very"

    def clean_text(self, text: str) -> str:
        """
        Cleans the input text by removing fillers, normalizing whitespace,
        and handling repetitions.
        """
        if not text:
            return ""

        cleaned = text.lower()
        
        # Remove filler words
        for pattern in self.filler_patterns:
            cleaned = re.sub(pattern, "", cleaned, flags=re.IGNORECASE)
            
        # Reduce repetitions (e.g., "very very" -> "very")
        # Note: sometimes repetition is emphatic, but for NLP analysis we often want to reduce it
        cleaned = re.sub(self.repetition_pattern, r"\1", cleaned)
        
        # Remove extra whitespace
        cleaned = re.sub(r"\s+", " ", cleaned).strip()
        
        return cleaned

    def process(self, text: str) -> dict:
        """
        Full preprocessing pipeline: Clean -> Tokenize -> Lemmatize -> Stem.
        Returns a dictionary with raw, cleaned, lemmas, and stems.
        """
        cleaned_text = self.clean_text(text)
        
        if not self.nlp:
            # Fallback if spaCy is missing: simple split
            tokens = cleaned_text.split()
            return {
                "original": text,
                "cleaned": cleaned_text,
                "tokens": tokens,
                "lemmas": tokens, # No lemmatization without spacy
                "stems": tokens
            }

        doc = self.nlp(cleaned_text)
        
        tokens = [token.text for token in doc]
        lemmas = [token.lemma_ for token in doc if not token.is_punct and not token.is_space]
        stems = []
        if self.stemmer:
             stems = [self.stemmer.stem(token.text) for token in doc if not token.is_punct and not token.is_space]
        
        return {
            "original": text,
            "cleaned": cleaned_text,
            "tokens": tokens,
            "lemmas": lemmas,
            "stems": stems
        }

if __name__ == "__main__":
    # Example Usage
    preprocessor = TextPreprocessor()
    sample_text = "Well, um, it was a very very long time ago, you know? I was just a child."
    result = preprocessor.process(sample_text)
    print("Original:", result["original"])
    print("Cleaned:", result["cleaned"])
    print("Lemmas:", result["lemmas"])
