# Memory Keeper - Technical Documentation

## API Reference (v1)

### Authentication

- **POST /api/v1/login**: OAuth2 compliant login.
- **POST /api/v1/register**: Create new family account.

### Conversation

- **POST /api/v1/chat/send**: Send text message (JSON).
- **POST /api/v1/chat/audio**: Upload audio blob (Multipart).
  - Returns: `{ "transcription": "...", "ai_response": "..." }`

### Data Models

See `docs/schema_design.md` for full ERD.

## Deployment Guide (Prompt 6.1)

1. **Build Containers**:
   ```bash
   docker-compose build
   ```
2. **Run Services**:
   ```bash
   docker-compose up -d
   ```
3. **Access**:
   - Frontend: `http://localhost:5173`
   - Backend API: `http://localhost:8000`

## NLP Pipeline Details

- **Preprocessing**: `app/services/nlp/preprocessing.py` (Rule-based cleaning).
- **Topic Modeling**: LDA implementation in `app/services/nlp/topics.py`.
- **Classification**: LogisticRegression model in `app/services/nlp/classification.py`.
