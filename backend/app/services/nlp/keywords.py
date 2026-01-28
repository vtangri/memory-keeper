try:
    import spacy
    from spacy.matcher import PhraseMatcher
except ImportError:
    spacy = None
    PhraseMatcher = None
from collections import Counter
from typing import List, Dict, Any
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class KeywordDetector:
    """
    Detects keywords, named entities, and themes in text using spaCy.
    Customizable with family-specific and historical dictionaries.
    """

    def __init__(self, model_name="en_core_web_sm"):
        self.nlp = None
        self.matcher = None
        
        if not spacy:
            logger.warning("spaCy not installed. Keyword detection disabled.")
            return

        try:
            self.nlp = spacy.load(model_name)
        except OSError:
            logger.warning(f"spaCy model '{model_name}' not found. Loading blank 'en' model for testing.")
            self.nlp = spacy.blank("en")

        if self.nlp:
            self.matcher = PhraseMatcher(self.nlp.vocab, attr="LOWER")
            self._initialize_custom_dictionaries()

    def _initialize_custom_dictionaries(self):
        """
        Initialize custom dictionaries for historical events, family roles, etc.
        In a real app, these might load from a JSON/YAML config or DB.
        """
        # 1. Family Terms
        family_terms = ["mother", "father", "grandmother", "grandfather", "aunt", "uncle", "sister", "brother", "grandma", "grandpa"]
        family_patterns = [self.nlp.make_doc(text) for text in family_terms]
        self.matcher.add("FAMILY_ROLE", family_patterns)

        # 2. Life Milestones
        milestones = ["marriage", "wedding", "graduation", "born", "birth", "retired", "retirement", "school", "college", "war"]
        milestone_patterns = [self.nlp.make_doc(text) for text in milestones]
        self.matcher.add("MILESTONE", milestone_patterns)

        # 3. Emotions/Themes (Simple keyword based)
        themes = {
            "JOY": ["happy", "delighted", "wonderful", "best day", "celebration"],
            "HARDSHIP": ["struggle", "poor", "difficult", "hard times", "war", "sad"],
        }
        for label, terms in themes.items():
            patterns = [self.nlp.make_doc(text) for text in terms]
            self.matcher.add(f"THEME_{label}", patterns)


    def detect_keywords(self, text: str) -> Dict[str, Any]:
        """
        Analyze text to extract entities, custom keywords, and themes.
        """
        if not self.nlp or not self.matcher:
             return {"entities": [], "custom_concepts": [], "weighted_keywords": []}

        doc = self.nlp(text)
        
        # 1. Standard NER (People, Dates, Locations)
        entities = []
        for ent in doc.ents:
            if ent.label_ in ["PERSON", "DATE", "GPE", "EVENT", "ORG"]:
                entities.append({
                    "text": ent.text,
                    "label": ent.label_,
                    "start": ent.start_char,
                    "end": ent.end_char
                })

        # 2. Custom Rule-Based Matching
        matches = self.matcher(doc)
        custom_keywords = []
        for match_id, start, end in matches:
            span = doc[start:end]
            label = self.nlp.vocab.strings[match_id]
            custom_keywords.append({
                "text": span.text,
                "label": label
            })

        # 3. Aggregate Stats
        # Simple frequency count of significant nouns/verbs for "Key Topics"
        # Filtering out stop words and lighter verbs
        useful_tokens = [
            token.lemma_.lower() 
            for token in doc 
            if not token.is_stop and not token.is_punct and token.pos_ in ["NOUN", "PROPN", "ADJ"]
        ]
        topic_counts = Counter(useful_tokens).most_common(5)

        return {
            "entities": entities,
            "custom_concepts": custom_keywords,
            "weighted_keywords": [{"text": t[0], "count": t[1]} for t in topic_counts]
        }

if __name__ == "__main__":
    detector = KeywordDetector()
    sample = "I remember when Grandma moved to New York in 1945. It was a difficult time during the war, but her wedding was beautiful."
    results = detector.detect_keywords(sample)
    print("Entities:", results["entities"])
    print("Concepts:", results["custom_concepts"])
