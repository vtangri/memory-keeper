# 🕯️ Memory Keeper: Preserving Legacies

**Memory Keeper** is a sophisticated, AI-powered storytelling companion designed to help families capture and preserve their stories. By combining a "Majestic Heritage" user interface with a robust NLP pipeline, it transforms casual conversations into a structured digital heirloom.

---

## 🌟 Overview

Memory Keeper isn't just a chatbot; it's a **Legacy Engine**. It uses natural language processing to understand the context, emotion, and historical significance of your stories.

### Key Features

- **Empathetic Conversation**: A high-end chat interface designed for comfort and accessibility.
- **NLP Enrichment**: Automatic topic classification, sentiment analysis, and keyword extraction.
- **Family Dashboard**: A centralized "Exploration" hub to view statistics, recent recordings, and an interactive life timeline.
- **Storybook Generation**: Capability to compile narratives into a printable PDF format.
- **Multimodal Support**: Integrated audio recording and STT (Speech-to-Text) capabilities.

---

## 🛠️ Tech Stack & NLP Methods

### 1. Core Stack

| Layer        | Technology                                               |
| :----------- | :------------------------------------------------------- |
| **Frontend** | React 18, Vite, Tailwind CSS, Framer Motion (Animations) |
| **Backend**  | FastAPI (Python 3.11+), Uvicorn                          |
| **Icons**    | Lucide React                                             |
| **Database** | PostgreSQL (Production) / Mocked Service layer (Local)   |

### 2. NLP Pipeline & Methods

The intelligence of Memory Keeper is powered by a modular NLP service layer designed for high resilience.

- **Entity & Theme Detection**: Powered by **spaCy** (`en_core_web_sm`). It extracts names, dates, and custom heritage themes (e.g., "MILESTONES", "FAMILY_ROLES").
- **Sentiment & Emotion**: Uses **VADER** and **NLTK** to detect nostalgia, sensitive topics, and general emotional valence.
- **Topic Modeling**: Implements **Latent Dirichlet Allocation (LDA)** via **Gensim** to find hidden themes across multiple story sessions.
- **Multi-label Classification**: Uses **Scikit-learn** (TF-IDF + OneVsRest Logistic Regression) to categorize story segments into "Childhood", "Career", "Marriage", etc.
- **Text Preprocessing**: Custom cleaning pipeline for handling speech disfluencies (fillers like "umm", "uhh") and repetitive phrases common in speech-to-text.

---

## 🏗️ Folder Structure

```text
Memory Keeper/
├── backend/                # FastAPI Application
│   ├── app/
│   │   ├── core/           # Security, Caching, Config
│   │   ├── services/       # The Business Logic
│   │   │   ├── nlp/        # Classification, Keywords, Sentiment, Topics
│   │   │   ├── audio/      # STT and TTS services
│   │   │   └── context/    # Historical context scrapers
│   │   └── main.py         # App Entry Point
│   ├── tests/              # Integration and Unit tests
│   └── requirements.txt    # Python Dependencies
├── frontend/               # React Application
│   ├── src/
│   │   ├── features/       # Modular features (Chat, Dashboard)
│   │   ├── components/     # High-reuse UI components
│   │   ├── Layout.jsx      # Majestic Heritage Layout
│   │   └── index.css       # Premium Design System
│   ├── tailwind.config.js  # Custom theme & Glassmorphism
│   └── package.json        # Node Dependencies
└── docker-compose.yml      # Orchestration
```

---

## 🚀 Execution Guide

### Prerequisites

- Python 3.11 or higher
- Node.js 18 or higher
- `pip` and `npm`

### Step 1: Clone and Setup Backend

1. Navigate to the backend directory:
   ```bash
   cd "Memory Keeper/backend"
   ```
2. Install dependencies:
   ```bash
   python3 -m pip install -r requirements.txt
   ```
3. Download the spaCy model:
   ```bash
   python3 -m spacy download en_core_web_sm
   ```
4. Start the FastAPI server:
   ```bash
   export PYTHONPATH=$PYTHONPATH:$(pwd)
   uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
   ```

### Step 2: Setup Frontend

1. Open a new terminal and navigate to the frontend:
   ```bash
   cd "Memory Keeper/frontend"
   ```
2. Install packages:
   ```bash
   npm install
   ```
3. Start the development server:
   ```bash
   npm run dev
   ```

### Step 3: Accessing the App

- **Chat Interface**: [http://localhost:5173](http://localhost:5173)
- **Family Dashboard**: [http://localhost:5173/dashboard](http://localhost:5173/dashboard)
- **API Documentation**: [http://localhost:8000/docs](http://localhost:8000/docs) (Interactive Swagger UI)

---

## 🛡️ Implementation Details

- **Safe-Import Architecture**: The backend is designed with "Safe Imports" for ML libraries. If a library like `gensim` or `sklearn` is missing, the system will log a warning but keep the core API running, degrading functionality gracefully.
- **Glassmorphism UI**: Uses Tailwind custom gradients and backdrop-blur utilities to create a "premium digital heirloom" feel.
- **Async Execution**: Audio processing and PDF generation are designed to run asynchronously to ensure a responsive UI.

---

_Created with ❤️ to preserve the stories that define us._
