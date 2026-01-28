# 📖 Memory Keeper: Complete User Manual

Welcome to **Memory Keeper**, your personal legacy engine. This guide covers everything from setting up the project on your machine to recording your first family story.

---

## 🛠️ Part 1: Installation & Setup Guide

Since you have the code on GitHub, here is how to set it up on any new machine (Mac/Windows/Linux).

### Prerequisites

- **Git**: To clone the repository.
- **Python (3.9+)**: To run the AI backend.
- **Node.js (18+)**: To run the Majestic UI frontend.

### Step 1: Clone the Repository

Open your terminal and run:

```bash
git clone https://github.com/vtangri/memory-keeper.git
cd memory-keeper
```

### Step 2: Setup the Backend (The Brain)

The backend powers the AI conversation and story analysis.

1. Navigate to the backend folder:
   ```bash
   cd backend
   ```
2. Create and activate a virtual environment (optional but recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Download the necessary Language Model:
   ```bash
   python -m spacy download en_core_web_sm
   ```
5. **Start the Server**:
   ```bash
   # Make sure you are in the 'backend' folder
   export PYTHONPATH=$PYTHONPATH:$(pwd)  # Mac/Linux only
   uvicorn app.main:app --reload
   ```
   _You should see: `Uvicorn running on http://127.0.0.1:8000`_

### Step 3: Setup the Frontend (The Beautiful UI)

1. Open a **new terminal** window/tab.
2. Navigate to the frontend folder:
   ```bash
   cd memory-keeper/frontend
   ```
3. Install dependencies:
   ```bash
   npm install
   ```
4. **Start the Application**:
   ```bash
   npm run dev
   ```
   _You should see a link like: `http://localhost:5173`_

---

## 🌟 Part 2: Feature Walkthrough

Once everything is running, open [http://localhost:5173](http://localhost:5173) in your browser.

### 1. The Conversations Page (Home)

This is where the magic happens.

- **Start Talking**: Type a memory into the input bar (e.g., _"I remember my first bicycle..."_) or click the **Microphone** to simulate voice recording.
- **Interactive AI**: The AI will ask follow-up questions. It's designed to be empathetic and encouraging.
- **Voice Player**: Listen to AI responses by clicking the **Volume** icon on any message bubble.

### 2. The Family Dashboard (Exploration)

Click **"Exploration"** in the top navigation bar.

- **Stats at a Glance**: See how many "Chapters" you've recorded and total "Audio Hours".
- **Recent Narratives**: A list of your latest stories. Each card shows the date, duration, and AI-detected tags (e.g., _Family, Travel_).
- **Heritage Timeline**: On the right, see your life events plotted vertically by year.

### 3. Memory Detail View

Click on any **Story Card** in the dashboard (e.g., _"Memories of the Old Dock"_).

- **Read**: View the full transcript of the story, beautifully formatted.
- **Listen**: Use the built-in audio player to hear the original recording.
- **Download**: Save the story to your device.

---

## ❓ Troubleshooting

- **"Backend Not Connected"**: Ensure the black terminal window with `uvicorn` is still open and running.
- **"Invalid Hook Call"**: If the screen goes white, restart the frontend server (`Ctrl+C` then `npm run dev`).

---

_Preserving stories, one conversation at a time._
