# Database Schema Design

**Response to Prompt 1.2**

## 1. Entity-Relationship Diagram (ERD)

```mermaid
erDiagram
    users ||--o{ families_users : "belongs to"
    families ||--o{ families_users : "has members"
    users ||--o{ conversations : "participates in"
    conversations ||--o{ messages : "contains"
    conversations ||--o{ audio_recordings : "has"
    users ||--o{ stories : "narrates"
    stories }|--|{ topics : "covers"
    stories ||--o{ timeline_events : "generates"
    users ||--o{ relationships : "source"
    users ||--o{ relationships : "target"

    users {
        uuid id PK
        string email
        string password_hash
        string full_name
        string role "ELDERLY | FAMILY | ADMIN"
        jsonb preferences
        timestamp created_at
    }

    families {
        uuid id PK
        string name
        timestamp created_at
    }

    conversations {
        uuid id PK
        uuid user_id FK
        timestamp start_time
        timestamp end_time
        string status "ACTIVE | COMPLETED | ARCHIVED"
        jsonb context_state
    }

    messages {
        uuid id PK
        uuid conversation_id FK
        string sender "USER | AI"
        text content
        timestamp timestamp
        uuid audio_id FK "nullable"
        float sentiment_score
    }

    stories {
        uuid id PK
        uuid user_id FK
        uuid conversation_source_id FK
        string title
        text content_markdown
        string category "CHILDHOOD | CAREER | WARTIME | ETC"
        string emotional_tone
        timestamp created_at
    }

    timeline_events {
        uuid id PK
        uuid story_id FK
        date event_date
        string title
        string description
        string location
    }

    audio_recordings {
        uuid id PK
        uuid conversation_id FK
        string s3_key
        int duration_seconds
        string status "PROCESSING | COMPLETED"
        string transcript_path
    }

    relationships {
        uuid id PK
        uuid from_user_id FK
        uuid to_user_id FK
        string relation_type "PARENT | CHILD | SIBLING | SPOUSE"
    }
```

## 2. Table Definitions & Strategies

### Core Tables

**1. Users**

- **Purpose**: Stores authentication and profile info.
- **Indexing**: `email` (Unique), `role` (B-tree for filtering).

**2. Conversations**

- **Purpose**: Tracks chat sessions.
- **Indexing**: `user_id` + `start_time` (Composite index for "My History").

**3. Stories (The Core Asset)**

- **Purpose**: Refined narratives extracted from raw chat.
- **Data Types**: `content_markdown` (Text), `category` (Enum).
- **Indexing**: `user_id`, `category` (Bitmap scan capable).

**4. Audio Recordings**

- **Purpose**: links to raw audio in Object Storage.
- **Optimization**: Store metadata here. actual binary data in S3/MinIO.

### Semantic & Analysis Tables

**5. Topics**

- **Purpose**: Tracks coverage of different life areas.
- **Structure**: `id`, `name`, `description`, `parent_topic_id`.

**6. Timeline Events**

- **Purpose**: Structured data for the Timeline Visualization features.
- **Data Types**: `event_date` (Date, allowing fuzzy dates if needed via separate fields).

### Scalability & Performance

1.  **JSONB for Flexibility**:
    - The `context_state` in `conversations` is JSONB. This allows the NLP engine to store arbitrary state (current mood, last discussed entity, exhausted topics) without schema migrations.
2.  **Vector Embeddings (Extension)**:
    - Future-proofing: A `embeddings` table linked to `stories` using `pgvector` will allow semantic search ("Show me stories about resilience").
3.  **Partitioning**:
    - `messages` table will grow effectively infinite. Partitioning by `created_at` (Monthly) is recommended for long-term retention.
