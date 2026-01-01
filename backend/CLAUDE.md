# CLAUDE.md (Backend)

## Build and Development
- **Virtual Environment**: `python -m venv venv`
- **Install Dependencies**: `pip install -r requirements.txt`
- **Run Server**: `uvicorn src.main:app --reload`
- **Migrations**:
  - `alembic upgrade head`
  - `alembic revision --autogenerate -m "description"`

## Project Structure
- `src/api`: FastAPI route definitions and routers.
- `src/models`: SQLModel/Pydantic schemas and database models.
- `src/services`: Business logic and database operations.
- `src/middleware`: Custom auth verification and logging.
- `src/database`: Connection and session management.

## New Models and Services (Phase III: AI Chatbot)
- `src/models/conversation.py`: Conversation entity for chat history
- `src/models/message.py`: Message entity for chat messages
- `src/services/conversation_service.py`: Conversation management
- `src/services/message_service.py`: Message handling
- `src/services/agent_service.py`: AI agent integration with OpenAI Agents SDK
- `src/services/mcp_server.py`: MCP tools for task operations (add_task, list_tasks, update_task, complete_task, delete_task)
- `src/api/chat_api.py`: Chat endpoint at `/api/{user_id}/chat`

## Coding Style
- **Framework**: FastAPI with SQLModel (Active Record pattern).
- **Type Hints**: Mandatory for all function signatures and properties.
- **Enums**: Use lowercase values for database compatibility.
- **Security**: JWT-based authentication using `sub` claim for ownership filtering.
- **Naming**: snake_case for functions/variables, PascalCase for classes.
- **Routing**: Explicit prefixes in `APIRouter` with empty-string root paths.
- **AI Integration**: Follow stateless architecture with conversation persistence.
