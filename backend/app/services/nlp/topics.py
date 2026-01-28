try:
    import gensim
    from gensim import corpora
    from gensim.models import LdaModel, CoherenceModel
except ImportError:
    gensim = None
from typing import List, Dict, Any, Tuple
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TopicModeler:
    """
    Implements LDA Topic Modeling to discover themes in family stories.
    Manages a dictionary and corpus for the family's specific vocabulary.
    """

    def __init__(self, num_topics=5):
        self.num_topics = num_topics
        self.dictionary = None
        self.lda_model = None
        
        # Predefined mapping attempting to label discovered topics
        self.topic_labels = {
            "childhood": ["school", "play", "mother", "father", "young", "kid", "born"],
            "career": ["work", "job", "office", "money", "business", "company", "retired"],
            "wartime": ["war", "army", "soldier", "fight", "peace", "country"],
            "family": ["marriage", "wedding", "husband", "wife", "children", "son", "daughter"]
        }

    def train(self, tokenized_docs: List[List[str]]):
        """
        Train the LDA model on a collection of stories (list of token lists).
        """
        if not gensim:
            logger.warning("Gensim not installed. Topic modeling disabled.")
            return

        if not tokenized_docs:
            logger.warning("No documents provided for training.")
            return

        # Create dictionary
        self.dictionary = corpora.Dictionary(tokenized_docs)
        # Filter extremes: remove words in <3 docs or >80% of docs
        # (Be careful with small datasets: adjusting min_no below)
        if len(tokenized_docs) > 5:
            self.dictionary.filter_extremes(no_below=2, no_above=0.8)

        # Create Corpus (BoW)
        corpus = [self.dictionary.doc2bow(text) for text in tokenized_docs]
        
        # Train LDA
        self.lda_model = LdaModel(
            corpus=corpus,
            id2word=self.dictionary,
            num_topics=self.num_topics,
            random_state=42,
            update_every=1,
            chunksize=10,
            passes=10,
            alpha='auto',
            per_word_topics=True
        )
        logger.info("LDA Model trained successfully.")

    def get_topic_for_document(self, tokens: List[str]) -> List[Tuple[str, float]]:
        """
        Infers the topic distribution for a new document.
        Returns list of (TopicName, Probability).
        """
        if not self.lda_model or not self.dictionary or not gensim:
            return [("Uncategorized", 1.0)]

        bow = self.dictionary.doc2bow(tokens)
        topic_dist = self.lda_model.get_document_topics(bow)
        
        # Map ID to human-readable label if possible
        results = []
        for topic_id, prob in topic_dist:
            label = self._label_topic(topic_id)
            results.append((label, float(prob)))
            
        return sorted(results, key=lambda x: x[1], reverse=True)

    def _label_topic(self, topic_id: int) -> str:
        """
        Attempt to label a topic by comparing its top words to predefined categories.
        """
        top_words = [word for word, _ in self.lda_model.show_topic(topic_id, topn=10)]
        
        best_label = f"Topic {topic_id}"
        max_overlap = 0
        
        for label, keywords in self.topic_labels.items():
            # intersection of top_words and keywords
            overlap = len(set(top_words) & set(keywords))
            if overlap > max_overlap:
                max_overlap = overlap
                best_label = label.capitalize()
                
        return best_label

    def get_topics_display(self) -> List[Dict[str, Any]]:
        """
        Returns all topics and their top words for visualization.
        """
        if not self.lda_model:
            return []
            
        output = []
        for i in range(self.num_topics):
            words = self.lda_model.show_topic(i, topn=10)
            output.append({
                "id": i,
                "label": self._label_topic(i),
                "words": [w[0] for w in words]
            })
        return output

if __name__ == "__main__":
    # Tiny dataset simulation
    docs = [
        ["school", "teacher", "class", "study", "exam"],
        ["work", "job", "money", "office", "boss"],
        ["school", "friend", "play", "playground"],
        ["war", "army", "gun", "fight", "soldier"],
        ["job", "career", "salary", "bonus"]
    ]
    
    modeler = TopicModeler(num_topics=3)
    modeler.train(docs)
    
    new_doc = ["teacher", "study", "books"]
    print("New Doc Topics:", modeler.get_topic_for_document(new_doc))
    print("All Topics:", modeler.get_topics_display())
