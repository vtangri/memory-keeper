from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional
from pydantic import BaseModel
import datetime

app = FastAPI(title="Memory Keeper API", version="1.0.0")

# Add CORS middleware to allow frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mock Data Storage
class Story(BaseModel):
    id: str
    title: str
    date: str
    duration: str
    topics: List[str]
    content: str  # The full text or summary
    audio_url: Optional[str] = None

MOCK_STORIES = [
    Story(
        id="1",
        title="Memories of the Old Dock",
        date="Mar 24, 2024",
        duration="12 mins",
        topics=["Childhood", "Family", "Travel"],
        content="I remember the old dock down by the bay. We used to go there every summer. The wood was weathered and gray, smelling of salt and memories. My grandfather taught me how to fish there. We would sit for hours, just watching the bobbers dance on the water. It wasn't really about the fish, you know? It was about the silence, the shared peace. I can still hear the creaking of the wood and the gentle lap of the waves.",
        audio_url="mock_audio.mp3"
    ),
    Story(
        id="2",
        title="The First Day of College",
        date="Mar 22, 2024",
        duration="10 mins",
        topics=["Education", "Growth"],
        content="Walking onto campus for the first time felt like stepping into a new world. The buildings were so tall, covered in ivy. I was terrified but also exhilarated. I remember carrying a heavy suitcase up three flights of stairs to my dorm room. My roommate was already there, unpacking a collection of vintage records. That day marked the beginning of my independence.",
        audio_url="mock_audio_2.mp3"
    ),
    Story(
        id="3",
        title="Our Wedding in Vermont",
        date="Mar 20, 2024",
        duration="15 mins",
        topics=["Love", "Milestone", "Family"],
        content="It was a crisp autumn day. The leaves were turning shades of gold and crimson. We chose a small barn in Vermont for the ceremony. I remember the smell of apple cider and woodsmoke in the air. When I saw her walking down the aisle, everything else faded away. We wrote our own vows, promising to be each other's compass. It was the happiest day of my life.",
        audio_url="mock_audio_3.mp3"
    )
]

@app.get("/health")
def health_check():
    return {"status": "healthy"}

@app.get("/api/v1/stories", response_model=List[Story])
def get_stories():
    return MOCK_STORIES

@app.get("/api/v1/stories/{story_id}", response_model=Story)
def get_story(story_id: str):
    for story in MOCK_STORIES:
        if story.id == story_id:
            return story
    raise HTTPException(status_code=404, detail="Story not found")

# Chat endpoint mock (keeping existing functionality if needed or using the real one if it was integrated)
from app.services.conversation_manager import ContextManager
# context_manager = ContextManager() 
# For now, simplistic echo or mock if ContextManager isn't fully wired in this single file view
# In a real app, we'd import the router.

class ChatRequest(BaseModel):
    text: str
    session_id: str

@app.post("/api/v1/chat/send")
async def chat_send(request: ChatRequest):
    # Mock response for now to ensure UI works, or use the ContextManager if instantiated
    return {
        "reply": f"That's a fascinating detail about '{request.text}'. Tell me more about how you felt in that moment?",
        "sentiment": "positive"
    }
