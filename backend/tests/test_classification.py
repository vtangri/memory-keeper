import unittest
import shutil
import os
from app.services.nlp.classification import StoryClassifier

class TestStoryClassifier(unittest.TestCase):
    MODEL_PATH = "data/test_classifier.pkl"

    def setUp(self):
        self.classifier = StoryClassifier(model_path=self.MODEL_PATH)
        self.train_texts = [
            "school was fun",
            "work was hard", 
            "war was scary",
            "school and work"
        ]
        self.train_labels = [
             ["childhood"],
             ["career"],
             ["wartime"],
             ["childhood", "career"]
        ]
        self.classifier.train(self.train_texts, self.train_labels)

    def tearDown(self):
        if os.path.exists(self.MODEL_PATH):
            os.remove(self.MODEL_PATH)

    def test_prediction(self):
        # "school" -> childhood
        results = self.classifier.predict("school")
        labels = [r[0] for r in results]
        self.assertIn("childhood", labels)

    def test_multi_label_prediction(self):
        # "school and work" -> childhood, career
        results = self.classifier.predict("school work")
        labels = [r[0] for r in results]
        self.assertIn("childhood", labels)
        self.assertIn("career", labels)

if __name__ == '__main__':
    unittest.main()
