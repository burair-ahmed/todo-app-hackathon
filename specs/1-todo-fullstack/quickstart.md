# Quickstart Guide: Todo Full-Stack Web Application

## Prerequisites

- Node.js 18+ for frontend development
- Python 3.11+ for backend development
- PostgreSQL (or access to Neon Serverless PostgreSQL)
- Git
- Package managers: npm/pnpm/yarn for frontend, pip for backend

## Environment Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd <repository-name>
   ```

2. **Backend Setup**
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Frontend Setup**
   ```bash
   cd frontend
   npm install
   ```

4. **Environment Variables**
   Create `.env` files in both backend and frontend directories based on `.env.example`:

   Backend `.env`:
   ```
   DATABASE_URL=postgresql://user:password@localhost:5432/todo_app
   JWT_SECRET=your-super-secret-jwt-key-here
   JWT_ALGORITHM=HS256
   JWT_EXPIRATION_HOURS=24
   ```

   Frontend `.env.local`:
   ```
   NEXT_PUBLIC_API_URL=http://localhost:8000
   NEXT_PUBLIC_BETTER_AUTH_URL=http://localhost:8000
   ```

## Running the Application

### Development Mode

**Backend (FastAPI server)**:
```bash
cd backend
source venv/bin/activate  # On Windows: venv\Scripts\activate
uvicorn src.main:app --reload --port 8000
```

**Frontend (Next.js development server)**:
```bash
cd frontend
npm run dev
```

The application will be available at `http://localhost:3000`

### Database Setup

1. Ensure PostgreSQL is running
2. Run database migrations:
```bash
cd backend
alembic upgrade head
```

### Better Auth Setup

1. Better Auth will be configured automatically when the Next.js app starts
2. The authentication endpoints will be available at `/api/auth/*`

## API Documentation

The backend API documentation is available at:
- Interactive docs: `http://localhost:8000/docs`
- Alternative docs: `http://localhost:8000/redoc`

## Testing

**Backend tests**:
```bash
cd backend
python -m pytest
```

**Frontend tests**:
```bash
cd frontend
npm test
```

## Deployment

### Backend Deployment
1. Set production environment variables
2. Run migrations in production
3. Start the server with a production WSGI server like Gunicorn

### Frontend Deployment
1. Build the application: `npm run build`
2. Deploy the build output to a static hosting service
3. Ensure API endpoints are correctly configured for the deployment environment

## Troubleshooting

**Common Issues**:
- Database connection errors: Verify PostgreSQL is running and credentials are correct
- Authentication not working: Check JWT secret is consistent between frontend and backend
- API calls failing: Verify NEXT_PUBLIC_API_URL points to the correct backend URL
- CORS errors: Ensure backend allows requests from frontend origin