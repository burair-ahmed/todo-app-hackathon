# Horizon: AI-Native Task Orchestration System

[![Spec-Driven](https://img.shields.io/badge/Architecture-Spec--Driven-blueviolet)](/specs/)
[![AI-Powered](https://img.shields.io/badge/AI-Powered%20(Gemini%20%2B%20MCP)-orange)](#-ai-native-architecture)
[![Cloud-Native](https://img.shields.io/badge/Cloud--Native-Kubernetes%20Ready-blue)](#-cloud-native--infrastructure)

Horizon is not just a todo app; it is a **Spec-Driven, AI-Native Task Orchestration System** built across a multi-phase development evolution. It combines a robust FastAPI/Next.js core with an advanced AI Resident Agent that manages your life through the Model Context Protocol (MCP).

---

## 🏛️ The Three Pillars

### 1. Spec-Driven Development (SDD)
Every feature in Horizon was developed using a "Specs First" approach. We maintain a strict source of truth in the `specs/` directory, ensuring that the implementation never drifts from the architectural intent.
- **SDD First**: Logic verified against Specification Documents before a single line of UI was written.
- **Traceable History**: Centralized evolution of requirements from Phase I (Console) to Phase III (AI).

### 2. AI-Native Architecture
Horizon features a deeply integrated AI agent powered by **OpenAI Agents SDK** and **Gemini 2.0 Flash**.
- **MCP Protocol**: The agent interacts with the system via Model Context Protocol (MCP), providing a stateless, tool-driven interface for task manipulation.
- **Multi-Step Reasoning**: Capable of complex task chaining, priority inference, and natural language scheduling.
- **Real-time Synchronization**: Seamless handoff between the AI Chat interface and the Next.js visual dashboard.

### 3. Cloud-Native & Scalable
Designed for the modern cloud, Horizon is ready for production deployment at any scale.
- **Neon Serverless PostgreSQL**: High-performance, autoscaling database storage with instant branching.
- **Containerized Excellence**: Docker-ready with optimized multi-stage builds.
- **Kubernetes Optimized**: Includes production-grade Helm charts for zero-downtime deployments found in `charts/todo-chatbot`.

---

## 🚀 Evolution Roadmap

Horizon was built in three distinct phases, each layering complexity onto a solid foundation:

| Phase | Focus | Key Deliverables |
| :--- | :--- | :--- |
| **Phase I** | **Core Logic** | Python Console App, In-Memory Storage, Core Task Service. |
| **Phase II** | **Full-Stack** | Next.js Frontend, FastAPI Backend, Neon DB, JWT Auth (Better Auth). |
| **Phase III** | **Intelligence** | Gemini-powered Chat Agent, MCP Tooling, ChatKit Integration. |

---

## 🏗️ Architecture

```mermaid
graph TD
    User([User]) <--> Web[Next.js Frontend]
    User <--> Agent[AI Chat Agent]
    
    subgraph "Backend Core"
        API[FastAPI REST Layer]
        ChatAPI[Chat API Endpoint]
        Services[Task & User Services]
        MCP[MCP Server]
    end

    Web <--> API
    Agent <--> ChatAPI
    ChatAPI <--> MCP
    MCP <--> Services
    API <--> Services
    
    Services <--> DB[(Neon PostgreSQL)]
    Services <--> Auth{Better Auth / JWT}
```

---

## 🛠️ Tech Stack

- **Frontend**: Next.js 15 (App Router), Tailwind CSS, Framer Motion, Axios.
- **Backend Core**: FastAPI (Asynchronous), SQLModel (Pydantic + SQLAlchemy).
- **AI Engine**: OpenAI Agents SDK, Google Gemini 2.0 Flash, FastMCP.
- **Database**: Neon Serverless PostgreSQL.
- **DevOps**: Docker, Helm Charts, GitHub Actions.

---

## ⚙️ Project Configuration & Setup

### 1. Environment Variables (`.env`)

#### Backend Setup (`backend/.env`)
Create a `.env` file in the `backend/` directory with the following structure:
```env
# Database
DATABASE_URL=postgresql://user:password@hostname:5432/neondb?sslmode=require

# Security
JWT_SECRET=your_super_secret_key_here
JWT_ALGORITHM=HS256
JWT_EXPIRATION_HOURS=24

# AI Integration
GEMINI_API_KEY=your_gemini_api_key
OPENAI_API_KEY=your_openai_api_key (optional, for compatibility)
```

#### Frontend Setup (`frontend/.env.local`)
Create a `.env.local` file in the `frontend/` directory:
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_BETTER_AUTH_URL=http://localhost:8000

# ChatKit Integration
NEXT_PUBLIC_CHATKIT_API_KEY=your_chatkit_key
NEXT_PUBLIC_CHATKIT_WORKFLOW_ID=your_workflow_id
```

---

### 2. Phase I: Console Application
Before the web UI, Horizon began as a pure Python console application. You can still run it for a lightweight experience.

**Run Command**:
```bash
# From the project root
python -m src.main
```

**Features**:
- Interactive CLI Menu.
- In-memory task management.
- Zero-dependency runtime (uses standard lib).

---

### 3. Launching the Web System

**Backend**:
```bash
cd backend
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
uvicorn src.main:app --reload
```

**Frontend**:
```bash
cd frontend
npm install
npm run dev
```

---

## 🧪 Testing & Quality Assurance

Horizon maintains high code quality through comprehensive testing:
- **Backend Verification**: `pytest` for service logic and API integrity.
- **Frontend Verification**: `Jest` and `React Testing Library`.
- **E2E Stability**: Critical paths verified via automated browser testing.

---

## 📜 License & Acknowledgments
Built for the **Todo App Hackathon**. Horizon follows the 2025 AI-Native Application Standards.
