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

## Coding Style
- **Framework**: FastAPI with SQLModel (Active Record pattern).
- **Type Hints**: Mandatory for all function signatures and properties.
- **Enums**: Use lowercase values for database compatibility.
- **Security**: JWT-based authentication using `sub` claim for ownership filtering.
- **Naming**: snake_case for functions/variables, PascalCase for classes.
- **Routing**: Explicit prefixes in `APIRouter` with empty-string root paths.
