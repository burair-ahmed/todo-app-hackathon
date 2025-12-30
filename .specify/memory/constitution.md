# Project Constitution: Todo App Hackathon

## Core Principles
1. **Premium UX**: Every feature must feeel fluid, using animations (Framer Motion) and modern UI patterns.
2. **Security First**: All data access is scoped to the authenticated user via JWT.
3. **Robust Data Integrity**: Use PostgreSQL Enums and typed schemas for consistent state.
4. **Maintenance Friendly**: Standard documentation via `CLAUDE.md` and detailed specifications in `/specs`.

## Feature Guidelines
- **Recurring Tasks**: Logic must handle rescheduling without duplicating history.
- **Due Dates**: Must support timezone-aware timestamps.
- **State Management**: React Query for data fetching; local state for UI transitions.

## Tech Stack
- **Frontend**: Next.js (App Router), Tailwind CSS, Framer Motion, Lucide Icons.
- **Backend**: FastAPI, SQLModel, PostgreSQL (Neon), Alembic.
- **Auth**: Custom JWT-based auth.
