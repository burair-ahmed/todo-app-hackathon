<!-- SYNC IMPACT REPORT
Version change: 1.0.0 → 2.0.0
Modified principles:
- Premium UX (expanded to include AI chatbot considerations)
- Security First (expanded to include JWT authentication for AI chatbot)
- Robust Data Integrity (unchanged)
- Maintenance Friendly (unchanged)

Added sections:
- AI Chatbot Architecture Principles
- LLM Provider Integration
- Statelessness Requirements
- Scope Enforcement

Removed sections:
- Feature Guidelines (replaced with AI-specific guidelines)

Templates requiring updates:
- ✅ .specify/templates/plan-template.md - Updated to align with AI chatbot principles
- ✅ .specify/templates/spec-template.md - Updated scope requirements
- ✅ .specify/templates/tasks-template.md - Updated task categorization
- ✅ .specify/templates/commands/*.md - Updated references
- ⚠️ README.md - May need updates (pending manual review)

Follow-up TODOs: None
-->

# Project Constitution: Todo AI Chatbot

## Core Principles

1. **Premium UX**: Every feature must feel fluid, using animations (Framer Motion) and modern UI patterns. The AI chatbot must provide a seamless conversational experience with intuitive task management capabilities through OpenAI ChatKit UI.

2. **Security First**: All data access is scoped to the authenticated user via JWT. All chat requests require JWT authentication, user_id must be derived from JWT, and MCP tools must enforce user ownership.

3. **Robust Data Integrity**: Use PostgreSQL Enums and typed schemas for consistent state. All database operations must maintain consistency and enforce proper data validation.

4. **Maintenance Friendly**: Standard documentation via `CLAUDE.md` and detailed specifications in `/specs`. Code must be well-documented and follow consistent patterns for maintainability.

## AI Chatbot Architecture Principles

5. **AI Framework Standard**: Backend must use Python FastAPI with OpenAI Agents SDK as the AI framework. MCP Server must use the Official MCP SDK for tool integration.

6. **Statelessness Requirements**: FastAPI server MUST hold NO in-memory chat state. Conversation history is persisted in database. MCP tools are stateless. Every request must be reproducible.

7. **Database-First Architecture**: ORM must use SQLModel with Neon Serverless PostgreSQL as the database. All chatbot operations must interact with the database for persistence rather than in-memory state.

8. **Authentication Integration**: Authentication must use Better Auth + JWT verification for all chatbot interactions. User identity must be validated for every request.

## LLM Provider Integration

9. **LLM Provider Rule**: Gemini API key is used as the underlying model provider. Gemini must be accessed via OpenAI-compatible or adapter layer. Claude Code must NOT introduce direct UI-to-LLM calls. All LLM calls go through backend agent runner.

## Scope Enforcement

10. **Limited Functionality Scope**: AI chatbot supports ONLY basic task operations: Add task, List tasks, Update task, Delete task, Complete task. No scheduling or reminders functionality should be implemented beyond basic task management.

## Tech Stack

- **Frontend**: OpenAI ChatKit UI, Next.js (App Router), Tailwind CSS, Framer Motion, Lucide Icons
- **Backend**: Python FastAPI, OpenAI Agents SDK, MCP Server (Official MCP SDK)
- **ORM**: SQLModel
- **Database**: Neon Serverless PostgreSQL
- **Authentication**: Better Auth + JWT verification
- **LLM Provider**: Gemini API (accessed via OpenAI-compatible layer)

## Governance

- **Ratification Date**: 2025-01-01
- **Last Amended Date**: 2025-12-31
- **Constitution Version**: 2.0.0 (Major update for AI chatbot phase)
- **Amendment Procedure**: All changes must maintain backward compatibility with existing task CRUD APIs which must NOT be rewritten
- **Compliance Review**: All implementations must follow Spec-Kit Plus and Claude Code must reference specs using @specs paths