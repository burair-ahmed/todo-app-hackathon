---
description: "Task list for Todo AI Chatbot feature implementation"
---

# Tasks: Todo AI Chatbot

**Input**: Design documents from `/specs/1-ai-chatbot/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: The examples below include test tasks. Tests are OPTIONAL - only include them if explicitly requested in the feature specification.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Single project**: `src/`, `tests/` at repository root
- **Web app**: `backend/src/`, `frontend/src/`
- **Mobile**: `api/src/`, `ios/src/` or `android/src/`
- Paths shown below assume single project - adjust based on plan.md structure

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [X] T001 Create project structure per implementation plan in backend/src/ and frontend/src/
- [X] T002 Initialize Python project with FastAPI, SQLModel, OpenAI Agents SDK dependencies in backend/requirements.txt
- [X] T003 [P] Configure linting and formatting tools for Python and TypeScript
- [X] T004 Initialize TypeScript project with ChatKit dependencies in frontend/package.json
- [X] T005 [P] Create environment configuration for backend and frontend

---
## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [X] T006 Setup database schema and migrations framework in backend/src/database/
- [X] T007 [P] Implement JWT authentication framework in backend/src/middleware/jwt_auth.py
- [X] T008 [P] Setup API routing and middleware structure in backend/src/main.py
- [X] T009 Create Conversation SQLModel in backend/src/models/conversation.py
- [X] T010 Create Message SQLModel in backend/src/models/message.py
- [X] T011 Create migration scripts for Conversation and Message models
- [X] T012 Configure error handling and logging infrastructure
- [X] T013 Initialize MCP server framework in backend/src/services/mcp_server.py
- [X] T014 Setup conversation and message service layers in backend/src/services/

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Chat with AI Assistant for Task Management (Priority: P1) 🎯 MVP

**Goal**: Allow users to interact with an AI assistant to manage tasks through natural language commands

**Independent Test**: User can send natural language commands to the chatbot and verify that tasks are created, updated, or deleted appropriately

### Implementation for User Story 1

- [X] T015 [P] [US1] Initialize OpenAI Agents SDK configuration in backend/src/services/agent_service.py
- [X] T016 [P] [US1] Integrate Gemini model adapter in backend/src/services/agent_service.py
- [X] T017 [US1] Register MCP tools with the agent in backend/src/services/agent_service.py
- [X] T018 [US1] Define agent instructions for task management in backend/src/services/agent_service.py
- [X] T018.1 [US1] Implement tool call detection and execution in backend/src/services/agent_service.py
- [X] T019 [P] [US1] Implement add_task MCP tool in backend/src/services/mcp_server.py
- [X] T020 [P] [US1] Implement list_tasks MCP tool in backend/src/services/mcp_server.py
- [X] T021 [P] [US1] Implement update_task MCP tool in backend/src/services/mcp_server.py
- [X] T022 [P] [US1] Implement complete_task MCP tool in backend/src/services/mcp_server.py
- [X] T023 [P] [US1] Implement delete_task MCP tool in backend/src/services/mcp_server.py
- [X] T023.1 [US1] Integrate MCP tools with existing task service in backend/src/services/mcp_server.py
- [X] T024 [US1] Implement chat endpoint POST /api/{user_id}/chat in backend/src/api/chat_api.py
- [X] T025 [US1] Add conversation history loading to chat endpoint in backend/src/api/chat_api.py
- [X] T026 [US1] Add message persistence to chat endpoint in backend/src/api/chat_api.py
- [X] T027 [US1] Handle tool call results in chat endpoint in backend/src/api/chat_api.py
- [X] T028 [US1] Add error handling to chat endpoint in backend/src/api/chat_api.py
- [X] T029 [P] [US1] Integrate ChatKit UI in frontend/src/components/ChatKitWrapper/
- [X] T029.1 [P] [US1] Implement tool call handling in frontend/src/components/ChatKitWrapper/
- [X] T030 [P] [US1] Create chat API service in frontend/src/services/api.ts
- [X] T030.1 [P] [US1] Update chat API service for tool call handling in frontend/src/services/api.ts
- [X] T031 [US1] Implement secure JWT usage in frontend/src/services/auth.ts
- [X] T031.1 [US1] Update auth service for Better Auth integration in frontend/src/services/auth.ts
- [X] T032 [US1] Connect frontend to backend chat API in frontend/src/app/chat/page.tsx

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - Persistent Conversation History (Priority: P2)

**Goal**: Allow users to continue conversations across sessions with all conversation history preserved and associated with their account

**Independent Test**: User can start a conversation, close the interface, and then resume the conversation with a new message that references previous context

### Implementation for User Story 2

- [X] T033 [P] [US2] Enhance conversation service with history retrieval in backend/src/services/conversation_service.py
- [X] T034 [P] [US2] Enhance message service with pagination in backend/src/services/message_service.py
- [X] T035 [US2] Add conversation resume support to frontend in frontend/src/app/chat/page.tsx
- [X] T036 [US2] Implement conversation history display in frontend/src/components/ChatKitWrapper/

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - Secure User Isolation (Priority: P3)

**Goal**: Ensure each user can only access their own conversations and tasks with proper authentication and authorization enforced at all levels

**Independent Test**: Attempt to access another user's conversations and verify access is denied

### Implementation for User Story 3

- [X] T037 [P] [US3] Enhance JWT middleware to enforce user ownership in backend/src/middleware/jwt_auth.py
- [X] T038 [P] [US3] Add user ownership checks to conversation service in backend/src/services/conversation_service.py
- [X] T039 [P] [US3] Add user ownership checks to message service in backend/src/services/message_service.py
- [X] T040 [US3] Add user ownership validation to MCP tools in backend/src/services/mcp_server.py

**Checkpoint**: All user stories should now be independently functional

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [X] T041 [P] Documentation updates in README.md
- [X] T042 [P] Update CLAUDE.md with AI chatbot information
- [X] T043 Update specs history documentation
- [X] T044 Code cleanup and refactoring across all components
- [X] T045 Performance optimization for chat responses
- [X] T046 Security hardening for all endpoints
- [X] T047 Run quickstart.md validation
- [X] T047.1 Update frontend dependencies (jwt-decode) in package.json
- [X] T047.2 Update backend dependencies (AI packages) in requirements.txt

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3+)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P2 → P3)
- **Polish (Final Phase)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P2)**: Can start after Foundational (Phase 2) - May integrate with US1 but should be independently testable
- **User Story 3 (P3)**: Can start after Foundational (Phase 2) - May integrate with US1/US2 but should be independently testable

### Within Each User Story

- Models before services
- Services before endpoints
- Core implementation before integration
- Story complete before moving to next priority

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel
- All Foundational tasks marked [P] can run in parallel (within Phase 2)
- Once Foundational phase completes, all user stories can start in parallel (if team capacity allows)
- All tests for a user story marked [P] can run in parallel
- Models within a story marked [P] can run in parallel
- Different user stories can be worked on in parallel by different team members

---

## Parallel Example: User Story 1

```bash
# Launch all parallelizable tasks for User Story 1 together:
Task: "Initialize OpenAI Agents SDK configuration in backend/src/services/agent_service.py"
Task: "Integrate Gemini model adapter in backend/src/services/agent_service.py"
Task: "Implement add_task MCP tool in backend/src/services/mcp_server.py"
Task: "Implement list_tasks MCP tool in backend/src/services/mcp_server.py"
Task: "Implement update_task MCP tool in backend/src/services/mcp_server.py"
Task: "Integrate ChatKit UI in frontend/src/components/ChatKitWrapper/"
Task: "Create chat API service in frontend/src/services/api.js"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1
4. **STOP and VALIDATE**: Test User Story 1 independently
5. Deploy/demo if ready

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → Deploy/Demo (MVP!)
3. Add User Story 2 → Test independently → Deploy/Demo
4. Add User Story 3 → Test independently → Deploy/Demo
5. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1
   - Developer B: User Story 2
   - Developer C: User Story 3
3. Stories complete and integrate independently

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Verify tests fail before implementing
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence