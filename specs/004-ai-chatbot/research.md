# Research: Todo AI Chatbot Implementation

## Decision: Database Schema Design
**Rationale**: Need to define the conversation and message models that align with the requirements while ensuring data integrity and proper relationships.
**Alternatives considered**:
- Single table approach (combined conversation/message data)
- Separate tables with foreign key relationships (chosen)
- Document-based storage in JSON fields

## Decision: MCP Server Integration Pattern
**Rationale**: The MCP SDK needs to be integrated with the agent system to provide task operations. The official MCP SDK provides the standard interface for tool integration.
**Alternatives considered**:
- Direct function calls instead of MCP tools
- Custom tool registration system
- MCP server with official SDK (chosen for standardization)

## Decision: JWT Authentication Implementation
**Rationale**: Must extract user context from JWT tokens to ensure proper user isolation and security as required by the constitution.
**Alternatives considered**:
- Session-based authentication
- API keys per user
- JWT with custom middleware (chosen for consistency with existing auth)

## Decision: OpenAI Agents SDK with Gemini Backend
**Rationale**: The constitution requires using OpenAI Agents SDK but with Gemini as the underlying provider, necessitating an adapter layer.
**Alternatives considered**:
- Direct Gemini API calls
- OpenAI-compatible proxy layer (chosen)
- Custom agent implementation

## Decision: Frontend ChatKit Integration
**Rationale**: The constitution specifies OpenAI ChatKit UI, which needs to be properly integrated with the backend authentication and API.
**Alternatives considered**:
- Custom chat UI implementation
- Third-party chat library
- OpenAI ChatKit with custom wrapper (chosen for compliance)

## Decision: Stateless Architecture Implementation
**Rationale**: The system must be stateless as required by the constitution, with all conversation state persisted to the database.
**Alternatives considered**:
- In-memory session storage
- Redis caching
- Database-only persistence (chosen for compliance)

## Decision: Task Tool Contracts Design
**Rationale**: MCP tools must implement the required task operations (add, list, update, delete, complete) with proper user ownership enforcement.
**Alternatives considered**:
- Generic task operation
- Separate tools for each operation (chosen for clarity)
- Batch operations vs individual tools