---
id: constitution-20260108-001
title: Amend Cloud-Native Constitution v3
stage: constitution
date: 2026-01-08
surface: command
model: Claude Sonnet 4.5
feature: cloud-native-deployment
branch: 1-ai-chatbot
user: Pc
command: /sp.constitution
labels: [governance, architecture, cloud-native, kubernetes]
links:
  spec:
  ticket:
  adr:
  pr:
files:
  - path: .specify/memory/constitution.md
    action: modified
    summary: Updated constitution from v2.0.0 to v3.0.0 with cloud-native principles
tests:
  - name: constitution-update-validation
    status: passed
    summary: New constitution aligns with cloud-native requirements
---
## Prompt

```text
You are an autonomous AI engineer operating under Spec-Kit Plus standards.

This constitution governs Phase IV of the Cloud Native Todo Chatbot project.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
CORE PRINCIPLES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. Cloud-Native First
- All services must run inside Kubernetes
- No docker-compose or local process managers
- Pods must be stateless and restart-safe

2. Local-First Kubernetes
- Deployment target is Minikube
- No managed cloud services except external Neon DB
- Cluster must be reproducible on any developer machine

3. Container Discipline
- Frontend and backend must be independently containerized
- No secrets baked into images
- Multi-stage Docker builds preferred

4. Helm as Source of Truth
- All Kubernetes resources must be deployed via Helm charts
- values.yaml controls configuration
- No hardcoded replicas, images, or env vars

5. AI-Assisted DevOps
- Prefer Docker AI (Gordon) for Docker operations
- Prefer kubectl-ai for kubectl workflows
- Use kagent for cluster analysis and optimization

6. Observability & Safety
- Liveness and readiness probes are mandatory
- Resource requests and limits are required
- Clear failure diagnostics must be possible

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
NON-GOALS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

- No cloud deployment (GKE/EKS)
- No service mesh
- No persistent volumes
- No database inside Kubernetes

This constitution must be enforced in all subsequent phases.
```

## Response snapshot

Updated the project constitution to version 3.0.0 to reflect the Cloud-Native principles for Phase IV of the Todo Chatbot project. The new constitution replaces the previous AI Chatbot-focused principles with cloud-native deployment requirements including:

- Kubernetes-first deployment strategy
- Minikube as the target platform
- Independent containerization of frontend and backend
- Helm chart deployment methodology
- AI-assisted DevOps practices
- Enhanced observability and safety requirements

## Outcome

- ✅ Impact: Major governance update changing project architecture direction to cloud-native
- 🧪 Tests: Constitution validation passed with proper principle alignment
- 📁 Files: Updated .specify/memory/constitution.md with new cloud-native principles
- 🔁 Next prompts: Will govern all subsequent cloud-native implementation decisions
- 🧠 Reflection: Constitution now properly guides Phase IV cloud-native deployment

## Evaluation notes (flywheel)

- Failure modes observed: None - smooth transition from AI chatbot to cloud-native principles
- Graders run and results (PASS/FAIL): PASS - all new principles properly documented
- Prompt variant (if applicable): Standard constitution update procedure
- Next experiment (smallest change to try): Begin implementing cloud-native deployment tasks based on new constitution