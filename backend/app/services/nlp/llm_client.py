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
                                 user_response_length: str = "medium") -> str:
        """
        Generates a context-aware follow-up question.
        
        Args:
            history: List of {"role": "user/ai", "content": "..."}
            current_topic: Current active topic (e.g. "childhood")
            user_response_length: 'short', 'medium', 'long' (derived from context)
        """
        last_user_msg = history[-1]['content'] if history and history[-1]['role'] == 'user' else ""
        
        # 1. Check for specific confusion markers or requests to stop
        if "stop" in last_user_msg.lower() or "tired" in last_user_msg.lower():
            return "We can take a break whenever you like. Should we stop for now?"
            
        # 2. Adaptation logic (Prompt 3.1 requirement: adapt to user state)
        # If user gives short answers, ask simpler, more specific questions.
        # If user gives long answers, ask broader, open-ended questions.
        
        # Mocking LLM Call:
        # prompt = f"You are an empathetic interviewer. User said: {last_user_msg}. Topic: {current_topic}..."
        # response = openai.ChatCompletion.create(...)
        
        # Heuristic implementation for prototype:
        questions = self.templates.get(current_topic, self.templates["general"])
        selected_question = random.choice(questions)
        
        if user_response_length == "short":
             return f"That's interesting. {selected_question} Was it a happy time?" # Append simple yes/no hook
             
        return selected_question

    def personalize_prompt(self, base_question: str, user_name: str) -> str:
        """
        Injects user name for personalization.
        """
        return f"{user_name}, {base_question}"
