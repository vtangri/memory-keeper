from typing import List, Dict, Optional
from datetime import datetime
import uuid
from app.services.nlp.llm_client import LLMClient
from app.services.nlp.sentiment import SentimentAnalyzer

class ConversationContext:
    """
    Maintains the state of a single conversation session.
    """
    def __init__(self, user_id: str, session_id: str = None):
        self.session_id = session_id or str(uuid.uuid4())
        self.user_id = user_id
        self.history: List[Dict[str, str]] = [] # list of {role, content, timestamp}
        self.current_topic: str = "general"
        self.exhausted_topics: List[str] = []
        self.used_questions: set = set() # Track asked questions to prevent repeats
        self.start_time = datetime.now()
        self.start_time = datetime.now()
        self.turn_count = 0
        self.state = "ACTIVE" # ACTIVE, PAUSED, ENDED

class ContextManager:
    """
    Orchestrates the conversation flow (Prompt 3.2).
    Integrates NLP, queues questions, manages state.
    """
    def __init__(self):
        self.active_sessions: Dict[str, ConversationContext] = {}
        self.llm_client = LLMClient()
        self.sentiment_analyzer = SentimentAnalyzer()

    def create_session(self, user_id: str) -> str:
        ctx = ConversationContext(user_id)
        self.active_sessions[ctx.session_id] = ctx
        return ctx.session_id

    def get_session(self, session_id: str) -> Optional[ConversationContext]:
        return self.active_sessions.get(session_id)

    async def process_user_input(self, session_id: str, text: str) -> str:
        """
        Main pipeline entry point for a chat turn.
        """
        ctx = self.get_session(session_id)
        if not ctx:
            return "Session expired or invalid."

        # 1. Update History
        ctx.history.append({
            "role": "user",
            "content": text,
            "timestamp": datetime.now().isoformat()
        })
        ctx.turn_count += 1
        
        # 2. Analyze Input
        sentiment = self.sentiment_analyzer.analyze(text)
        length_category = "long" if len(text.split()) > 20 else "short"
        
        # 3. Check Logic (Confusion, Topic Exhaustion)
        # If user says "I don't know" or "No idea", maybe switch topic
        if length_category == "short" and ("no" in text.lower() or "don't know" in text.lower()):
            # Fallback or switch topic strategy could go here
            pass
            
        # 4. Generate Response
        response_text = await self.llm_client.generate_follow_up(
            history=ctx.history,
            current_topic=ctx.current_topic,
            user_response_length=length_category,
            exclude_questions=list(ctx.used_questions)
        )
        ctx.used_questions.add(response_text)
        
        # 5. Update History with AI response
        ctx.history.append({
            "role": "ai",
            "content": response_text,
            "timestamp": datetime.now().isoformat()
        })
        
        return response_text

    def change_topic(self, session_id: str, new_topic: str):
        ctx = self.get_session(session_id)
        if ctx:
            if ctx.current_topic != "general":
                ctx.exhausted_topics.append(ctx.current_topic)
            ctx.current_topic = new_topic
            return True
        return False

    def reset_session(self, session_id: str):
        """
        Resets the session state (clears history, resets topic) for a fresh start.
        """
        ctx = self.get_session(session_id)
        if ctx:
            ctx.history = []
            ctx.current_topic = "general"
            ctx.turn_count = 0
            ctx.used_questions = set()
            ctx.start_time = datetime.now()
            return True
        return False
