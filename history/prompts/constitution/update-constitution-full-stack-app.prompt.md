---
id: constitution-001
title: Update Constitution Full-Stack App
stage: constitution
date: 2025-12-26
surface: ""
model: claude-sonnet-4-5-20250929
feature: todo-fullstack-app
branch: main
user: Pc
command: /sp.constitution
labels: [constitution, fullstack, todo-app]
links:
  spec: ""
  ticket: ""
  adr: ""
  pr: ""
files:
  - path: .specify/memory/constitution.md
    action: modify
    description: Update constitution from console app to full-stack web app
tests: {}
---

## Prompt

```text
You are building Phase II: Todo Full-Stack Web Application using spec-driven development.

Core Rules:
- This is a FULL-STACK WEB APPLICATION.
- Must use a MONOREPO structure with frontend and backend in a single repository.
- All development must follow Spec-Kit Plus conventions.
- Claude Code must always reference specs using @specs paths.
- Phase I console-only assumptions are no longer valid.

Mandatory Architecture:
- Frontend: Next.js 16+ (App Router)
- Backend: Python FastAPI
- ORM: SQLModel
- Database: Neon Serverless PostgreSQL
- Authentication: Better Auth (Frontend) + JWT (Backend verification)

Non-Negotiable Requirements:
- Multi-user support
- Persistent storage using PostgreSQL
- RESTful API design
- JWT-based authentication for all API requests
- User data isolation enforced at API level

Security Rules:
- Every API request MUST include a valid JWT token
- Backend must verify JWT signature using shared secret
- User ID from JWT must match user_id in route
- Unauthorized access must return HTTP 401

Scope Enforcement:
- Implement ONLY basic Todo functionality:
  - Add Task
  - View Tasks
  - Update Task
  - Delete Task
  - Mark Complete / Incomplete
- No feature creep (no priorities, tags, due dates, sharing, admin roles)

If ambiguity exists, choose the simplest secure implementation.
```

## Response snapshot

The constitution file (.specify/memory/constitution.md) was successfully updated to reflect the requirements for the full-stack web application. The key changes included:

- Updated version from 1.0.0 to 2.0.0 (major version bump due to architectural changes)
- Changed focus from console application to full-stack web application
- Added requirements for monorepo architecture with frontend and backend
- Specified technology stack (Next.js 16+, FastAPI, SQLModel, Neon PostgreSQL)
- Added authentication requirements (Better Auth + JWT)
- Included security requirements for API authentication and data isolation
- Maintained scope limitations to basic Todo functionality
- Updated development standards for full-stack development

## Outcome

- ✅ Impact: Constitution updated to reflect full-stack web application requirements
- 🧪 Tests: N/A
- 📁 Files: 1 file modified (.specify/memory/constitution.md)
- 🔁 Next prompts: N/A
- 🧠 Reflection: Major version bump was appropriate as this represents a fundamental architectural change from console app to full-stack web app

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): N/A
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): N/A