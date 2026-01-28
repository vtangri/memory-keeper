try:
    import sklearn
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.linear_model import LogisticRegression
    from sklearn.multiclass import OneVsRestClassifier
    from sklearn.pipeline import Pipeline
    from sklearn.preprocessing import MultiLabelBinarizer
    import joblib
except ImportError:
    sklearn = None
    joblib = None
import os
import logging
from typing import List, Dict, Any, Tuple

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class StoryClassifier:
    """
    Multi-label text classification system for categorizing story segments.
    """

    def __init__(self, model_path="data/classifier_model.pkl"):
        self.model_path = model_path
        self.pipeline = None
        self.mlb = None
        
        if sklearn:
            self.mlb = MultiLabelBinarizer()
            # If model exists, load it
            if os.path.exists(model_path):
                self.load_model()
            else:
                logger.info("No pre-trained model found at init.")
        else:
            logger.warning("Scikit-learn not available.")

    def train(self, texts: List[str], labels: List[List[str]]):
        """
        Train the classification model on a dataset.
        """
        if not texts or not labels or not sklearn:
            logger.error("Empty training data or missing dependencies.")
            return

        # Transform labels to binary matrix
        y = self.mlb.fit_transform(labels)
        
        # Create Pipeline: Tfidf -> Classifier
        # Using LogisticRegression inside OneVsRest for multi-label support
        self.pipeline = Pipeline([
            ('tfidf', TfidfVectorizer(max_features=5000, stop_words='english')),
            ('clf', OneVsRestClassifier(LogisticRegression(solver='liblinear')))
        ])
        
        logger.info("Training classifier...")
        self.pipeline.fit(texts, y)
        logger.info("Training complete.")
        
        self.save_model()

    def predict(self, text: str) -> List[Tuple[str, float]]:
        """
        Predict categories for a single text.
        Returns list of (Category, ConfidenceScore). 
        Note: LogisticRegression predict_proba gives prob for True/False per class.
        """
        if not self.pipeline:
            logger.warning("Model not trained yet.")
            return []

        # Predict
        # proba returns a list of arrays (one per class) in OvR? 
        # Actually for OVR + LogReg, predict_proba returns (n_samples, n_classes)
        probs = self.pipeline.predict_proba([text])[0]
        
        results = []
        for idx, score in enumerate(probs):
            if score > 0.3: # Threshold for "Active" tag
                label = self.mlb.classes_[idx]
                results.append((label, float(score)))
                
        return sorted(results, key=lambda x: x[1], reverse=True)

    def save_model(self):
        try:
            os.makedirs(os.path.dirname(self.model_path), exist_ok=True)
            joblib.dump((self.pipeline, self.mlb), self.model_path)
            logger.info(f"Model saved to {self.model_path}")
        except Exception as e:
            logger.error(f"Failed to save model: {e}")

    def load_model(self):
        try:
            self.pipeline, self.mlb = joblib.load(self.model_path)
            logger.info("Model loaded successfully.")
        except Exception as e:
            logger.error(f"Failed to load model: {e}")

if __name__ == "__main__":
    # Sample Training
    train_texts = [
        "I went to elementary school in 1950.",
        "I worked at the factory for 40 years as a manager.",
        "The war began when I was 18, I joined the navy.",
        "My mother cooked the best apple pie.",
        "We got married in a small church."
    ]
    train_labels = [
        ["childhood", "education"],
        ["career"],
        ["wartime", "military"],
        ["childhood", "family"],
        ["family", "marriage"]
    ]
    
    classifier = StoryClassifier(model_path="data/test_model.pkl")
    classifier.train(train_texts, train_labels)
    
    # Test
    test = "I met my wife at school."
    print(f"Prediction for '{test}':", classifier.predict(test))
