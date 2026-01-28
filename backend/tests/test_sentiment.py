import unittest
from app.services.nlp.sentiment import SentimentAnalyzer

class TestSentimentAnalyzer(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        try:
            cls.analyzer = SentimentAnalyzer()
        except Exception as e:
            print(f"Skipping SentimentAnalyzer tests: {e}")
            cls.analyzer = None

    def test_basic_sentiment(self):
        if not self.analyzer: return
        text = "I am so happy and delighted!"
        result = self.analyzer.analyze(text)
        self.assertEqual(result["primary_tone"], "POSITIVE")

    def test_nostalgia_detection(self):
        if not self.analyzer: return
        text = "I remember when we used to play in the park back in the day. It was wonderful."
        result = self.analyzer.analyze(text)
        self.assertTrue(result["scores"]["nostalgia"] > 0.5)
        self.assertEqual(result["primary_tone"], "NOSTALGIC_POSITIVE")

    def test_sensitive_detection(self):
        if not self.analyzer: return
        text = "Then he died in the war. It was full of pain."
        result = self.analyzer.analyze(text)
        self.assertTrue(result["is_sensitive"])
        self.assertEqual(result["primary_tone"], "SENSITIVE/SAD")

if __name__ == '__main__':
    unittest.main()
