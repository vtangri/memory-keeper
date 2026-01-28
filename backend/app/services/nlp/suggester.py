from typing import List, Dict
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TopicSuggester:
    """
    Analyzes conversation history and topic coverage to suggest new topics.
    """
    
    def __init__(self):
        self.all_topics = ["Childhood", "Education", "Career", "Marriage", "Parenthood", "Travel", "Hobbies", "Wartime"]
        
    def suggest_next_topics(self, covered_topics: List[str]) -> List[Dict[str, str]]:
        """
        Identify gaps in coverage and return prioritized suggestions.
        """
        covered_set = set(t.capitalize() for t in covered_topics)
        suggestions = []
        
        for topic in self.all_topics:
            if topic not in covered_set:
                suggestions.append({
                    "topic": topic,
                    "reason": "You haven't discussed this yet.",
                    "prompt": f"Tell me about your experiences with {topic}."
                })
                
        # Simple prioritization approach: Early life first
        # In a real system, we'd use RL or graph traversal
        return suggestions[:3]

    def generate_daily_prompt(self, user_name: str, context: Dict) -> str:
        """
        Generate a notification-style prompt for re-engagement.
        """
        return f"Hi {user_name}, do you have a moment to share a story about your first car?"

if __name__ == "__main__":
    suggester = TopicSuggester()
    print(suggester.suggest_next_topics(["Childhood", "Education"]))
