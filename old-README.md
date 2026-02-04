# Todo Full-Stack Web Application

A full-stack todo application with Next.js 16+ frontend (App Router), FastAPI backend with SQLModel ORM, Neon Serverless PostgreSQL database, and Better Auth/JWT authentication. The application provides secure, multi-user task management with proper data isolation and RESTful API design.

## Features

- User authentication and registration (via Better Auth)
- Create, read, update, and delete tasks
- Task completion tracking
- Multi-user support with data isolation
- JWT-based authentication using Better Auth tokens
- Responsive UI design
- Neon Serverless PostgreSQL for scalable database storage

## Tech Stack

- **Frontend**: Next.js 16+ with App Router
- **Backend**: FastAPI with Python 3.11+
- **Database**: Neon Serverless PostgreSQL with SQLModel ORM
- **Authentication**: Better Auth with JWT
- **Testing**: pytest (backend), Jest/React Testing Library (frontend)

## Prerequisites

- Node.js 18+ for frontend development
- Python 3.11+ for backend development
- Neon Serverless PostgreSQL access (or local PostgreSQL for development)
- Git

## Setup

### Backend Setup

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Copy the environment variables file:
   ```bash
   cp ../.env.example .env
   ```

5. Update the `.env` file with your Neon PostgreSQL configuration and JWT settings.

6. Run the application:
   ```bash
   uvicorn src.main:app --reload --port 8000
   ```

### Frontend Setup

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Copy the environment variables file:
   ```bash
   cp ../.env.example .env.local
   ```

4. Update the `.env.local` file with your configuration.

5. Run the development server:
   ```bash
   npm run dev
   ```

The application will be available at `http://localhost:3000`

## API Documentation

The backend API documentation is available at:
- Interactive docs: `http://localhost:8000/docs`
- Alternative docs: `http://localhost:8000/redoc`

## Environment Variables

### Backend (.env)
- `DATABASE_URL`: Neon Serverless PostgreSQL connection string (format: `postgresql://username:password@ep-dry-recipe-a1234567.us-east-1.aws.neon.tech/dbname?sslmode=require`)
- `JWT_SECRET`: Secret key for JWT token verification
- `JWT_ALGORITHM`: Algorithm used for JWT verification (default: HS256)

### Frontend (.env.local)
- `NEXT_PUBLIC_API_URL`: URL of the backend API
- `NEXT_PUBLIC_BETTER_AUTH_URL`: URL for Better Auth

## Project Structure

```
todo-fullstack/
├── backend/              # FastAPI backend
│   ├── src/
│   │   ├── models/       # SQLModel data models
│   │   ├── services/     # Business logic
│   │   ├── api/          # API routes
│   │   ├── middleware/   # JWT verification middleware
│   │   └── database/     # Database configuration for Neon
│   └── requirements.txt
├── frontend/             # Next.js frontend
│   ├── src/
│   │   ├── app/          # App Router pages
│   │   ├── components/   # React components
│   │   ├── services/     # API and Better Auth services
│   │   └── types/        # TypeScript types
│   └── package.json
├── specs/                # Specification files
└── README.md
```

## Database Setup

1. Ensure you have Neon Serverless PostgreSQL access
2. Run database migrations:
```bash
cd backend
alembic upgrade head
```

## Authentication Flow

1. Better Auth handles registration/login on the frontend
2. Better Auth issues JWT tokens upon successful authentication
3. Frontend includes JWT token in Authorization header for API requests
4. Backend verifies JWT tokens using shared secret
5. Backend enforces user-specific data access

## Testing

### Backend tests:
```bash
cd backend
python -m pytest
```

### Frontend tests:
```bash
cd frontend
npm test
```

## Deployment

### Backend
1. Set production environment variables (especially Neon database URL)
2. Run migrations in production
3. Start the server with a production WSGI server like Gunicorn

### Frontend
1. Build the application: `npm run build`
2. Deploy the build output to a static hosting service
3. Ensure API endpoints and Better Auth are correctly configured for the deployment environment

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## License

[License information to be added]