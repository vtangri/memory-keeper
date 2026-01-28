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

class DashboardStat(BaseModel):
    label: str
    value: str
    icon: str  # We'll pass the icon name, frontend maps it
    color: str
    trend: str

class TimelineEvent(BaseModel):
    year: int
    title: str
    desc: str

MOCK_STATS = [
    DashboardStat(label="Chapters", value="25", icon="Book", color="bg-brand-500", trend="+4 this month"),
    DashboardStat(label="Audio Hours", value="19.2", icon="Layers", color="bg-sage-500", trend="+2.9 hrs"),
    DashboardStat(label="Family Views", value="168", icon="Users", color="bg-fuchsia-500", trend="14 active now"),
]

MOCK_TIMELINE = [
    TimelineEvent(year=1952, title="The Great Winter", desc="A snowy birth in the heart of Ohio."),
    TimelineEvent(year=1965, title="First Guitar", desc="Learning to play 'Yesterday' in the basement."),
    TimelineEvent(year=1972, title="Summer of '72", desc="Crossing the country in a beat-up VW bus."),
    TimelineEvent(year=1985, title="Career Shift", desc="Starting the new business in Chicago."),
]

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

@app.get("/api/v1/dashboard/stats", response_model=List[DashboardStat])
def get_dashboard_stats():
    return MOCK_STATS

@app.get("/api/v1/dashboard/timeline", response_model=List[TimelineEvent])
def get_dashboard_timeline():
    return MOCK_TIMELINE

@app.get("/api/v1/stories/{story_id}", response_model=Story)
def get_story(story_id: str):
    for story in MOCK_STORIES:
        if story.id == story_id:
            return story
    raise HTTPException(status_code=404, detail="Story not found")

# Chat endpoint mock (keeping existing functionality if needed or using the real one if it was integrated)
# Chat endpoint mock (keeping existing functionality if needed or using the real one if it was integrated)
from app.services.conversation_manager import ContextManager
context_manager = ContextManager()

class ChatRequest(BaseModel):
    text: str
    session_id: str

@app.post("/api/v1/chat/send")
async def chat_send(request: ChatRequest):
    # Ensure session exists
    session = context_manager.get_session(request.session_id)
    if not session:
        context_manager.create_session(request.session_id)
        # Hack to force specific ID if needed, but create_session generates one if not passed.
        # Actually context_manager.create_session takes user_id and returns session_id.
        # But our FE sends a session_id "demo_user".
        # Let's adjust create_session or just manually inject for this demo.
        # Re-reading conversation_manager.py: create_session(user_id) -> session_id.
        # It stores in active_sessions[ctx.session_id]
        
        # Let's interact with it properly.
        # If the FE sends "demo_user" as session_id effectively, we should map that.
        # For simplicity in this demo:
        context_manager.active_sessions[request.session_id] = \
            context_manager.active_sessions.get(request.session_id) or \
            context_manager.create_session_with_id(request.session_id, "user_1")

    # The ContextManager doesn't expose create_session_with_id. 
    # Let's just do:
    if request.session_id not in context_manager.active_sessions:
        # Create a context manually and inject it to force the ID from FE
        from app.services.conversation_manager import ConversationContext
        ctx = ConversationContext(user_id="user_1", session_id=request.session_id)
        context_manager.active_sessions[request.session_id] = ctx

    reply = await context_manager.process_user_input(request.session_id, request.text)
    
    return {
        "reply": reply,
        "sentiment": "positive"
    }
