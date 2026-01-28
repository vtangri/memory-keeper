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

## 🌟 Part 2: Feature Walkthrough with Examples

Once everything is running, open [http://localhost:5173](http://localhost:5173) in your browser.

### 1. The Conversations Page (Home)

This is your interview space. The AI acts as a gentle biographer.

**Example Scenario:**

1.  **User Types/Says:** _"I remember the summer of 1969. We drove across the country in an old van."_
2.  **AI Responds:** _"That sounds like quite an adventure! Who was with you on that trip, and do you recall any specific stop that left a lasting impression?"_
3.  **User:** _"It was just me and my brother. We stopped at the Grand Canyon. It was huge."_
4.  **AI Responds:** _"The Grand Canyon is breathtaking. Standing there with your brother, do you remember how you felt looking out at that vastness? Was it peaceful, or were you overwhelmed?"_
5.  **User:** _"We felt small. We just sat on the hood of the van and watched the sunset. Ideally, we didn't say much."_
6.  **AI Responds:** _"Those quiet moments often speak the loudest. Watching that sunset, did you two talk about your future, or were you just enjoying the freedom of the road?"_
7.  **User:** _"We talked about our dad. He had just passed away. This trip was kind of our goodbye."_
8.  **AI Responds:** _"I'm so touched you shared that. It sounds like a profound healing journey. Traveling in his memory must have brought up many emotions. What is one specific thing about your dad that you remembered laughing about during that trip?"_

**How to Use:**

1.  **Type or Talk**: Click the microphone for voice mode.
2.  **Listen**: Click the volume icon on the AI's message to hear it spoken aloud (great for accessibility).
3.  **Auto-Save**: Notice the "Autosaved" indicator at the bottom; your stories are safe.

### 2. The Family Dashboard (Exploration)

Click **"Exploration"** to see your digital archive.

**Detailed Breakdown:**

- **Stats Cards**:
  - _Chapters_: **24** (Total stories told).
  - _Audio Hours_: **18.4** (Total time recorded).
  - _Family Views_: **152** (How many times memories were accessed).
- **Heritage Timeline**:
  - **1952**: "The Great Winter" (Born in Ohio).
  - **1965**: "First Guitar" (Learning to play music).
  - **1972**: "Summer Trip" (The van story).
- **Recent Narratives**: A card list of your latest sessions, tagged automatically (e.g., _#Travel_, _#Family_).

### 3. Memory Detail View

Click on a story card like **"Memories of the Old Dock"** to see the full record.

**What you'll see:**

- **A "Storybook" Title**: Large, elegant typography.
- **Context Tags**: `CHILDHOOD` `FAMILY` `NATURE` (Detected by AI).
- **The Narrative**:
  > _"I remember the old dock down by the bay. We used to go there every summer. The wood was weathered and gray, smelling of salt and memories..."_
- **Voice Record**: A player bar `[ ▶ ────────── 04:12 ]` to hear the original voice clip.
- **Actions**: Buttons to **Download** the text or **Share** the link with family.

---

## ❓ Troubleshooting

- **"Backend Not Connected"**: Ensure the black terminal window with `uvicorn` is still open and running.
- **"Invalid Hook Call"**: If the screen goes white, restart the frontend server (`Ctrl+C` then `npm run dev`).

---

_Preserving stories, one conversation at a time._
