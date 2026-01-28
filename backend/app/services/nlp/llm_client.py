from typing import List, Dict, Any
import logging
import random

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class LLMClient:
    """
    Handles interactions with the LLM (e.g., GPT-4) for generating questions.
    In a real scenario, this would wrap OpenAI or Azure API calls.
    Current implementation uses logic and templates for demonstration.
    """
    
    def __init__(self, api_key: str = None):
        self.api_key = api_key
        # Template library for fallback or structured interviewing
        self.templates = {
            "childhood": [
                "What was your favorite game to play as a child?",
                "Who was your best friend growing up, and what did you do together?",
                "Can you describe the house you grew up in?",
                "What is your earliest memory?"
            ],
            "career": [
                "What was your first job?",
                "Did you have a mentor who influenced your career path?",
                "What was the biggest challenge you faced in your work?",
                "What are you most proud of from your professional life?"
            ],
            "general": [
                "Tell me more about that.",
                "How did that make you feel?",
                "What happened next?",
                "Can you explain that in a bit more detail?"
            ]
        }

    async def generate_follow_up(self, 
                                 history: List[Dict[str, str]], 
                                 current_topic: str,
                                 user_response_length: str = "medium",
                                 exclude_questions: List[str] = None) -> str:
        """
        Generates a context-aware follow-up question.
        
        Args:
            history: List of {"role": "user/ai", "content": "..."}
            current_topic: Current active topic (e.g. "childhood")
            user_response_length: 'short', 'medium', 'long' (derived from context)
            exclude_questions: List of questions already asked in this session.
        """
        last_user_msg = history[-1]['content'] if history and history[-1]['role'] == 'user' else ""
        text_lower = last_user_msg.lower()
        exclude_questions = exclude_questions or []
        
        # 1. Check for specific confusion markers or requests to stop
        if "stop" in last_user_msg.lower() or "tired" in last_user_msg.lower():
            return "We can take a break whenever you like. Should we stop for now?"
            
        # 2. Dynamic topic detection based on keywords
        if any(word in text_lower for word in ["mom", "dad", "brother", "sister", "grandma", "grandpa", "family", "parents"]):
            current_topic = "family"
        elif any(word in text_lower for word in ["job", "work", "office", "boss", "career", "school", "college", "university"]):
            current_topic = "career"
        elif any(word in text_lower for word in ["trip", "travel", "vacation", "road", "visit", "summer", "mountain", "beach"]):
            current_topic = "travel"
        elif any(word in text_lower for word in ["sad", "cry", "miss", "lost", "passed away", "died", "gone", "grief"]):
            current_topic = "emotional"

        # Expanded template library (Prompt 3.1)
        # Dictionary of lists. Each list contains unique questions.
        if current_topic not in self.templates:
            # Initialize rich templates if not present or just extend them
            self.templates["family"] = [
                "Family bonds are so special. What is one tradition you all shared?",
                "How did your relationship with them shape who you are today?",
                "Do you have a favorite photograph of you two together?",
                "What was a typical Sunday dinner like in your house?",
                "Is there a specific lesson they taught you that stuck with you?",
                "When you look back, what makes you smile most about them?"
            ]
            self.templates["travel"] = [
                "Traveling often changes our perspective. Did this trip change how you saw the world?",
                "What was the most unexpected thing that happened on that journey?",
                "If you could go back to that place today, would you?",
                "Who was your favorite travel companion on that trip?",
                "Do you remember the smells or sounds of that place?"
            ]
            self.templates["career"] = [
                "What was the most rewarding project you ever worked on?",
                "Did you have a mentor who guided you early in your career?",
                "How did you balance your work with your personal life back then?",
                "What was the biggest risk you took in your professional life?"
            ]
            self.templates["emotional"] = [
                "I'm so touched you shared that. It sounds like a profound moment. How did you find comfort during that time?",
                "Those memories are heavy but beautiful. What is one thing about them that brings a smile to your face now?",
                "Thank you for trusting me with this. Do you feel that experience made you stronger?",
                "It's okay to feel emotional. Take your time. What do you miss most?"
            ]
            self.templates["childhood"] = [
                "What was your favorite game to play as a child?",
                "Who was your best friend growing up, and what did you do together?",
                "Can you describe the house you grew up in?",
                "What is your earliest memory?",
                "Did you have a favorite toy that went everywhere with you?"
            ]
            self.templates["general"] = [
                "Tell me more about that.",
                "How did that make you feel?",
                "What happened next?",
                "Can you explain that in a bit more detail?",
                "That's fascinating. What else do you remember?",
                "Could you paint a picture of that day for me?"
            ]
        
        # Select questions for the topic
        potential_questions = self.templates.get(current_topic, self.templates["general"])
        
        # Filter out already used questions
        available_questions = [q for q in potential_questions if q not in exclude_questions]
        
        # Fallback if we exhausted all questions for this topic
        if not available_questions:
             available_questions = self.templates["general"] # Fallback to general
             # If even general is exhausted (unlikely), just pick a random one
             if not available_questions:
                 available_questions = potential_questions

        # Pick a random one
        selected_question = random.choice(available_questions)
        
        if user_response_length == "short":
             # Hooks to encourage more detail
             hooks = ["Was it a vivid memory for you?", "Do you remember specific details?", "Why does that stand out?"]
             return f"That's interesting. {selected_question} {random.choice(hooks)}"
             
        return selected_question

    def personalize_prompt(self, base_question: str, user_name: str) -> str:
        """
        Injects user name for personalization.
        """
        return f"{user_name}, {base_question}"
