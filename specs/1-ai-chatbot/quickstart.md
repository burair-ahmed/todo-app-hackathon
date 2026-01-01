# Quickstart: Todo AI Chatbot

## Prerequisites

- Python 3.11+ (backend)
- Node.js 18+ (frontend)
- PostgreSQL database (Neon Serverless recommended)
- Gemini API key
- Better Auth configured

## Setup

### Backend Setup

1. **Install dependencies**:
   ```bash
   cd backend
   pip install fastapi openai uvicorn sqlmodel python-multipart
   pip install google-generativeai
   # Install MCP SDK
   pip install mcp
   ```

2. **Environment variables**:
   ```bash
   # backend/.env
   DATABASE_URL=postgresql://user:password@localhost/dbname
   GEMINI_API_KEY=your-gemini-api-key
   JWT_SECRET=your-jwt-secret
   ```

3. **Database setup**:
   ```bash
   # Create tables for conversations and messages
   python -c "from src.database import create_db_and_tables; create_db_and_tables()"
   ```

4. **Run backend**:
   ```bash
   cd backend
   uvicorn src.main:app --reload --port 8000
   ```

### Frontend Setup

1. **Install dependencies**:
   ```bash
   cd frontend
   npm install @openai/chatkit
   # Other dependencies as needed
   ```

2. **Environment variables**:
   ```bash
   # frontend/.env.local
   NEXT_PUBLIC_API_URL=http://localhost:8000
   NEXT_PUBLIC_CHATKIT_API_KEY=your-chatkit-key
   ```

3. **Run frontend**:
   ```bash
   cd frontend
   npm run dev
   ```

## Architecture Overview

### Backend Components

1. **MCP Server**: Handles tool calls for task operations (add, list, update, delete, complete)
2. **Agent Service**: Integrates OpenAI Agents SDK with Gemini backend
3. **Chat API**: Stateless endpoint at `/api/{user_id}/chat` that manages conversation flow
4. **Authentication**: JWT middleware to verify user identity and enforce data isolation

### Frontend Components

1. **ChatKit Integration**: Provides the chat interface
2. **API Service**: Handles communication with backend chat API
3. **Authentication Service**: Manages user authentication state

## API Usage

### Chat Endpoint

```bash
POST /api/{user_id}/chat
Authorization: Bearer {jwt_token}

{
  "conversation_id": 123,  // optional
  "message": "Add a task to buy groceries"
}
```

Response:
```json
{
  "conversation_id": 123,
  "response": "I've added the task 'buy groceries' to your list.",
  "tool_calls": [
    {
      "name": "add_task",
      "arguments": {
        "title": "buy groceries",
        "description": ""
      }
    }
  ]
}
```

## Running Tests

Backend tests:
```bash
cd backend
python -m pytest
```

Frontend tests:
```bash
cd frontend
npm test
```