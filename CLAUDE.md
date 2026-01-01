# Todo Full-Stack Web Application - Claude Code Usage

This project was developed using Claude Code, an AI assistant for software engineering tasks.

## Project Overview

The Todo Full-Stack Web Application is a complete application with:
- Next.js 16+ frontend (App Router)
- FastAPI backend with SQLModel ORM
- PostgreSQL database
- JWT-based authentication with Better Auth
- Multi-user support with data isolation
- AI-powered chatbot for task management

## Development Process

The application was built following a structured approach with the following phases:
1. Project setup and monorepo structure
2. Backend: Database models, services, and API endpoints
3. Frontend: Authentication, components, and pages
4. Security: JWT middleware and access control
5. Phase III: AI Chatbot Integration with OpenAI Agents SDK and Gemini
6. Integration and testing

## Code Structure

The project follows a monorepo architecture:
- **backend/**: FastAPI backend with SQLModel
  - **src/models/**: SQLModel data models (User, Task, Conversation, Message)
  - **src/services/**: Business logic (Auth, Task, Conversation, Message, Agent, MCP)
  - **src/api/**: API routes (Auth, Tasks, Chat)
  - **src/middleware/**: JWT authentication
  - **src/database/**: Database configuration
- **frontend/**: Next.js frontend with App Router
  - **src/app/**: App Router pages (login, register, dashboard, chat)
  - **src/components/**: React components (TaskList, TaskForm, ProtectedRoute, ChatKitWrapper)
  - **src/services/**: API and auth services
  - **src/types/**: TypeScript type definitions

## Key Features

- User authentication (register/login/logout)
- Task management (create, read, update, delete, toggle completion)
- Multi-user support with proper data isolation
- JWT-based authentication
- Responsive UI design
- Secure API with access control
- AI-powered chatbot for natural language task management
- Conversation history persistence
- MCP tools for task operations

## Claude Code Commands Used

- `/sp.constitution`: Updated project constitution for full-stack app
- `/sp.specify`: Created detailed feature specification
- `/sp.plan`: Generated implementation plan
- `/sp.tasks`: Generated detailed task breakdown
- `/sp.implement`: Implemented the AI chatbot feature
- Various file operations to create and modify source files
- Test creation and validation

## Quality Assurance

- Backend API endpoints properly secured with JWT authentication
- User data isolation enforced at the API level
- Frontend components properly handle authentication state
- Responsive UI design for multiple device sizes
- Clean, documented code with proper type hints
- AI integration follows stateless architecture principles

## Running the Application

1. Set up environment variables in `.env` (backend) and `.env.local` (frontend)
2. Install dependencies: `cd backend && pip install -r requirements.txt` and `cd frontend && npm install`
3. Start backend: `cd backend && uvicorn src.main:app --reload --port 8000`
4. Start frontend: `cd frontend && npm run dev`
5. Access the application at `http://localhost:3000`, chatbot at `http://localhost:3000/chat`

## Database Setup

1. Ensure PostgreSQL is running
2. Run database migrations: `alembic upgrade head`

## Testing

Backend tests: `python -m pytest`
Frontend tests: `npm test`