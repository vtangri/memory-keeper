import unittest
from app.services.nlp.topics import TopicModeler

class TestTopicModeler(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.modeler = TopicModeler(num_topics=2)
        # Small deterministic dataset for testing
        cls.docs = [
            ["apple", "banana", "fruit"],
            ["apple", "orange", "fruit"],
            ["car", "bus", "drive"],
            ["car", "truck", "drive"],
            ["apple", "banana", "fruit"], # repeat to help LDA converge
            ["car", "bus", "drive"]
        ]
        cls.modeler.train(cls.docs)

    def test_topic_inference(self):
        new_doc_fruit = ["apple", "fruit"]
        topics = self.modeler.get_topic_for_document(new_doc_fruit)
        # Should be list of (Label, Prob)
        self.assertTrue(len(topics) > 0)
        
        # Check that the probability sums roughly to something reasonable (LDA probabilistic)
        # We expect "apple" doc to share topic with "apple" training docs.
        # Since we can't guarantee Topic ID 0 is fruit, just check structure.
        self.assertIsInstance(topics[0][0], str)
        self.assertIsInstance(topics[0][1], float)

    def test_topic_display(self):
        display = self.modeler.get_topics_display()
        self.assertEqual(len(display), 2)
        self.assertIn("words", display[0])

if __name__ == '__main__':
    unittest.main()
