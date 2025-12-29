# Constitution: Phase II – Intermediate Level
## Todo Full-Stack Web Application

### Baseline
- Phase II Basic CRUD + Auth is COMPLETE and STABLE
- This phase EXTENDS functionality without breaking existing behavior

### Core Rules
- Application remains a FULL-STACK WEB APPLICATION
- Monorepo structure is mandatory
- Spec-Kit Plus workflow is mandatory
- Claude Code must reference specs using @specs paths

### Architecture (Unchanged)
- **Frontend**: Next.js 16+ (App Router)
- **Backend**: FastAPI (Python)
- **ORM**: SQLModel
- **Database**: Neon Serverless PostgreSQL
- **Authentication**: Better Auth (Frontend) + JWT (Backend)

### New Feature Scope (Intermediate Level)
- **Task Priorities**: (Low, Medium, High)
- **Task Tags / Categories**: User-defined tags
- **Search**: Multi-field search support
- **Filtering**: By priority, status, and tags
- **Sorting**: By date, priority, and title

### Non-Negotiable Constraints
- All features must be **USER-SCOPED**
- All queries must be filtered by authenticated user
- No role-based access or sharing
- No admin features
- No realtime or websockets

### Security Rules
- JWT authentication remains mandatory
- User isolation must be enforced at query level
- No task may be accessed outside its owner

### Decision Principles
- If ambiguity exists, choose:
  - Simpler UX
  - Safer backend logic
  - Fewer API endpoints over complex ones
