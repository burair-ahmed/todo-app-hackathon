# Implementation Plan: Todo AI Chatbot

**Branch**: `1-ai-chatbot` | **Date**: 2025-12-31 | **Spec**: [link](spec.md)
**Input**: Feature specification from `/specs/1-ai-chatbot/spec.md`

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Implementation of an AI-powered chatbot that allows users to manage their tasks through natural language conversations. The system will use OpenAI Agents SDK with a Gemini backend, MCP tools for task operations, and persistent conversation storage with JWT-based authentication.

## Technical Context

**Language/Version**: Python 3.11, TypeScript/JavaScript (Next.js 16+)
**Primary Dependencies**: FastAPI, OpenAI Agents SDK, MCP SDK, SQLModel, Better Auth, OpenAI ChatKit
**Storage**: PostgreSQL (Neon Serverless) with SQLModel ORM
**Testing**: pytest for backend, Jest for frontend
**Target Platform**: Web application (Next.js frontend + FastAPI backend)
**Project Type**: web (determines source structure)
**Performance Goals**: 95% of chat requests respond within 3 seconds, 99.9% uptime for message storage
**Constraints**: <3000ms p95 for chat responses, JWT authentication for all requests, user data isolation
**Scale/Scope**: Multi-user support with proper data isolation, conversation history persistence

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

1. **Premium UX**: Implementation must use OpenAI ChatKit UI for seamless conversational experience
2. **Security First**: All data access scoped to authenticated user via JWT, all chat requests require JWT authentication
3. **Robust Data Integrity**: Use PostgreSQL with SQLModel for consistent state and proper validation
4. **Maintenance Friendly**: Follow existing code patterns and document new components
5. **AI Framework Standard**: Backend must use Python FastAPI with OpenAI Agents SDK, MCP Server must use Official MCP SDK
6. **Statelessness Requirements**: FastAPI server holds no in-memory chat state, conversation history persists in database, MCP tools are stateless
7. **Database-First Architecture**: ORM uses SQLModel with Neon Serverless PostgreSQL
8. **Authentication Integration**: Use Better Auth + JWT verification for all chatbot interactions
9. **LLM Provider Rule**: Use Gemini API via OpenAI-compatible layer, all LLM calls go through backend agent runner
10. **Limited Functionality Scope**: Support only basic task operations (add, list, update, delete, complete), no scheduling/reminders

## Project Structure

### Documentation (this feature)

```text
specs/1-ai-chatbot/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── contracts/           # Phase 1 output (/sp.plan command)
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
backend/
├── src/
│   ├── models/
│   │   ├── conversation.py    # Conversation model
│   │   ├── message.py         # Message model
│   │   └── __init__.py
│   ├── services/
│   │   ├── conversation_service.py    # Conversation management
│   │   ├── message_service.py         # Message handling
│   │   ├── agent_service.py           # AI agent integration
│   │   ├── mcp_server.py              # MCP tools server
│   │   └── __init__.py
│   ├── api/
│   │   ├── chat_api.py        # Chat API endpoints
│   │   └── __init__.py
│   ├── middleware/
│   │   └── jwt_auth.py        # JWT authentication
│   └── main.py                # FastAPI app entry point
└── tests/
    ├── unit/
    ├── integration/
    └── contract/

frontend/
├── src/
│   ├── app/
│   │   └── chat/              # Chatbot page
│   ├── components/
│   │   └── ChatKitWrapper/    # ChatKit UI integration
│   ├── services/
│   │   ├── api.js             # API service
│   │   └── auth.js            # Authentication service
│   └── types/
│       └── chat.d.ts          # Chat-related types
└── tests/
    ├── unit/
    └── integration/
```

**Structure Decision**: Web application structure chosen to separate frontend (Next.js) and backend (FastAPI) concerns, with proper authentication and data isolation.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| Multiple API layers | Need both MCP server and chat API | MCP server handles tool calls, chat API handles user interactions |
| Complex authentication | Required for user data isolation | Basic auth insufficient for multi-user data protection |