# Todo Full-Stack Web Application - Claude Code Usage

This project was developed using Claude Code, an AI assistant for software engineering tasks.

## Project Overview

The Todo Full-Stack Web Application is a complete application with:
- Next.js 16+ frontend (App Router)
- FastAPI backend with SQLModel ORM
- PostgreSQL database
- JWT-based authentication with Better Auth
- Multi-user support with data isolation

## Development Process

The application was built following a structured approach with the following phases:
1. Project setup and monorepo structure
2. Backend: Database models, services, and API endpoints
3. Frontend: Authentication, components, and pages
4. Security: JWT middleware and access control
5. Integration and testing

## Code Structure

The project follows a monorepo architecture:
- **backend/**: FastAPI backend with SQLModel
  - **src/models/**: SQLModel data models (User, Task)
  - **src/services/**: Business logic (Auth, Task service)
  - **src/api/**: API routes (Auth, Tasks)
  - **src/middleware/**: JWT authentication
  - **src/database/**: Database configuration
- **frontend/**: Next.js frontend with App Router
  - **src/app/**: App Router pages (login, register, dashboard)
  - **src/components/**: React components (TaskList, TaskForm, ProtectedRoute)
  - **src/services/**: API and auth services
  - **src/types/**: TypeScript type definitions

## Key Features

- User authentication (register/login/logout)
- Task management (create, read, update, delete, toggle completion)
- Multi-user support with proper data isolation
- JWT-based authentication
- Responsive UI design
- Secure API with access control

## Claude Code Commands Used

- `/sp.constitution`: Updated project constitution for full-stack app
- `/sp.specify`: Created detailed feature specification
- `/sp.plan`: Generated implementation plan
- `/sp.tasks`: Generated detailed task breakdown
- Various file operations to create and modify source files
- Test creation and validation

## Quality Assurance

- Backend API endpoints properly secured with JWT authentication
- User data isolation enforced at the API level
- Frontend components properly handle authentication state
- Responsive UI design for multiple device sizes
- Clean, documented code with proper type hints

## Running the Application

1. Set up environment variables in `.env` (backend) and `.env.local` (frontend)
2. Start backend: `cd backend && uvicorn src.main:app --reload --port 8000`
3. Start frontend: `cd frontend && npm run dev`
4. Access the application at `http://localhost:3000`

## Database Setup

1. Ensure PostgreSQL is running
2. Run database migrations: `alembic upgrade head`

## Testing

Backend tests: `python -m pytest`
Frontend tests: `npm test`