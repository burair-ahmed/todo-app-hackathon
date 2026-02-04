# Data Model: Todo AI Chatbot

## Entity: Conversation

**Description**: Represents a single conversation thread between a user and the AI assistant

**Fields**:
- `id` (integer, primary key, auto-generated): Unique identifier for the conversation
- `user_id` (integer/string): Foreign key reference to the authenticated user
- `created_at` (timestamp): When the conversation was created
- `updated_at` (timestamp): When the conversation was last updated

**Validation Rules**:
- `user_id` must exist in the users table
- `created_at` is set on creation
- `updated_at` is updated on any modification

**State Transitions**: N/A (immutable after creation)

## Entity: Message

**Description**: Represents an individual message in a conversation

**Fields**:
- `id` (integer, primary key, auto-generated): Unique identifier for the message
- `user_id` (integer/string): Foreign key reference to the authenticated user
- `conversation_id` (integer): Foreign key reference to the conversation
- `role` (string, enum: "user" | "assistant"): The role of the message sender
- `content` (text): The content of the message
- `created_at` (timestamp): When the message was created

**Validation Rules**:
- `user_id` must match the conversation owner
- `conversation_id` must exist in the conversations table
- `role` must be either "user" or "assistant"
- `content` must not be empty
- `created_at` is set on creation

**State Transitions**: N/A (immutable after creation)

## Entity: User (existing)

**Description**: Represents an authenticated user (reference to existing user model)

**Fields**:
- `id` (integer/string, primary key): Unique identifier for the user
- Other fields from existing user model

**Relationships**:
- One user can have many conversations
- One user can have many messages
- One conversation can have many messages

## Database Constraints

1. **Foreign Key Constraints**:
   - `messages.user_id` references `users.id`
   - `messages.conversation_id` references `conversations.id`
   - `conversations.user_id` references `users.id`

2. **Data Integrity**:
   - All messages must belong to a valid conversation
   - All messages must belong to a valid user
   - All conversations must belong to a valid user
   - User ownership is enforced at the application level

3. **Indexes**:
   - Index on `conversations.user_id` for efficient user conversation queries
   - Index on `messages.conversation_id` for efficient conversation message queries
   - Index on `messages.user_id` for efficient user message queries