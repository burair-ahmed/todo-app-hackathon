<!--
Sync Impact Report:
Version change: 1.0.0 → 2.0.0
Added sections:
- Full-Stack Web Application: This is a FULL-STACK WEB APPLICATION with both frontend and backend components in a monorepo structure
- Monorepo Architecture: Must use MONOREPO structure with frontend and backend in a single repository following Spec-Kit Plus conventions
- Frontend Technology: Frontend must use Next.js 16+ with App Router
- Backend Technology: Backend must use Python FastAPI with SQLModel ORM
- Database Requirement: Must use Neon Serverless PostgreSQL for persistent storage
- Authentication System: Must implement Better Auth for frontend and JWT verification for backend
- Multi-User Support: Application must support multiple users with data isolation
- Security Requirements: Every API request MUST include valid JWT token; backend must verify JWT signature; user ID from JWT must match route user_id
- Scope Adherence (NON-NEGOTIABLE): Scope is STRICTLY limited to basic Todo functionality: Add Task, View Tasks, Update Task, Delete Task, Mark Complete/Incomplete; No feature creep allowed
- Clean Code Practices: Follow clean code principles and modern web development best practices
- Simple Implementation: Avoid over-engineering; keep logic simple and explicit; Choose the simplest secure implementation that satisfies the requirements
- Feature Completeness: Must implement all Non-Negotiable Features with proper authentication and data isolation

Modified principles: All principles updated from console application to full-stack web application
Removed sections: Command-Line Interface Focus, In-Memory Storage (replaced with new principles)
Templates requiring updates:
- .specify/templates/plan-template.md ✅ updated - Constitution Check section updated to reference new principles
- .specify/templates/spec-template.md ✅ updated - Aligned with new scope constraints and requirements
- .specify/templates/tasks-template.md ✅ updated - Aligned with new implementation guidelines

Follow-up TODOs: None
-->

# Todo Full-Stack Web Application Constitution

## Core Principles

### Full-Stack Web Application
This is a FULL-STACK WEB APPLICATION with both frontend and backend components; no console-only or single-tier assumptions.

### Monorepo Architecture
Must use MONOREPO structure with frontend and backend in a single repository; All development must follow Spec-Kit Plus conventions; Claude Code must always reference specs using @specs paths; Phase I console-only assumptions are no longer valid.

### Frontend Technology
Frontend must use Next.js 16+ (App Router); Must implement responsive design and modern UI/UX patterns.

### Backend Technology
Backend must use Python FastAPI; Must follow RESTful API design principles; All API endpoints must be properly documented.

### ORM and Database Requirement
Must use SQLModel ORM with Neon Serverless PostgreSQL for persistent storage; All data must be properly structured with appropriate relationships and constraints.

### Authentication System
Must implement Better Auth (Frontend) + JWT (Backend verification); Authentication must be secure and properly validated at all levels.

### Multi-User Support
Application must support multiple users with proper data isolation enforced at the API level; User data must never be accessible to other users.

### Security Requirements
Every API request MUST include a valid JWT token; Backend must verify JWT signature using shared secret; User ID from JWT must match user_id in route; Unauthorized access must return HTTP 401.

### Scope Adherence (NON-NEGOTIABLE)
Scope is STRICTLY limited to basic Todo functionality: Add Task, View Tasks, Update Task, Delete Task, Mark Complete/Incomplete; No feature creep (no priorities, tags, due dates, sharing, admin roles).

## Development Standards

Use spec-driven development with Spec-Kit Plus and Claude Code; Project must follow a clean and professional full-stack folder structure; Code must be readable, modular, and maintainable across both frontend and backend.

## Implementation Guidelines

If any ambiguity exists, choose the simplest secure implementation that satisfies the requirements; Prioritize security and data isolation over feature richness.

## Governance

Constitution supersedes all other practices; Amendments require documentation and approval; All implementations must verify compliance with these principles and security requirements.

**Version**: 2.0.0 | **Ratified**: 2025-12-24 | **Last Amended**: 2025-12-26
