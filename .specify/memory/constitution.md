<!-- SYNC IMPACT REPORT
Version change: 2.0.0 → 3.0.0
Modified principles:
- Premium UX (removed - not relevant to cloud-native phase)
- Security First (removed - not relevant to cloud-native phase)
- Robust Data Integrity (removed - not relevant to cloud-native phase)
- Maintenance Friendly (removed - not relevant to cloud-native phase)
- AI Chatbot Architecture Principles (removed - not relevant to cloud-native phase)
- LLM Provider Integration (removed - not relevant to cloud-native phase)
- Scope Enforcement (removed - not relevant to cloud-native phase)

Added sections:
- Cloud-Native First: All services must run inside Kubernetes
- Local-First Kubernetes: Deployment target is Minikube
- Container Discipline: Frontend and backend must be independently containerized
- Helm as Source of Truth: All Kubernetes resources must be deployed via Helm charts
- AI-Assisted DevOps: Prefer Docker AI (Gordon) for Docker operations
- Observability & Safety: Liveness and readiness probes are mandatory

Templates requiring updates:
- ✅ .specify/templates/plan-template.md - Updated to align with cloud-native principles
- ✅ .specify/templates/spec-template.md - Updated scope requirements
- ✅ .specify/templates/tasks-template.md - Updated task categorization
- ✅ .specify/templates/commands/*.md - Updated references
- ⚠️ README.md - May need updates for cloud-native deployment (pending manual review)

Follow-up TODOs:
- TODO(DEPLOYMENT_GUIDE): Add detailed Minikube deployment guide
-->

# Project Constitution: Todo Cloud-Native Chatbot

## Core Principles

1. **Cloud-Native First**: All services must run inside Kubernetes. No docker-compose or local process managers. Pods must be stateless and restart-safe.

2. **Local-First Kubernetes**: Deployment target is Minikube. No managed cloud services except external Neon DB. Cluster must be reproducible on any developer machine.

3. **Container Discipline**: Frontend and backend must be independently containerized. No secrets baked into images. Multi-stage Docker builds preferred.

4. **Helm as Source of Truth**: All Kubernetes resources must be deployed via Helm charts. values.yaml controls configuration. No hardcoded replicas, images, or env vars.

5. **AI-Assisted DevOps**: Prefer Docker AI (Gordon) for Docker operations. Prefer kubectl-ai for kubectl workflows. Use kagent for cluster analysis and optimization.

6. **Observability & Safety**: Liveness and readiness probes are mandatory. Resource requests and limits are required. Clear failure diagnostics must be possible.

## Non-Goals

- No cloud deployment (GKE/EKS)
- No service mesh
- No persistent volumes
- No database inside Kubernetes

## Tech Stack

- **Containerization**: Docker with multi-stage builds
- **Orchestration**: Kubernetes via Minikube
- **Packaging**: Helm charts for deployment
- **Database**: External Neon Serverless PostgreSQL (not inside Kubernetes)
- **DevOps Tools**: Docker AI (Gordon), kubectl-ai, kagent

## Governance

- **Ratification Date**: 2026-01-08
- **Last Amended Date**: 2026-01-08
- **Constitution Version**: 3.0.0 (Major update for cloud-native phase)
- **Amendment Procedure**: All changes must maintain backward compatibility with existing Kubernetes deployment patterns
- **Compliance Review**: All implementations must follow Spec-Kit Plus and ensure cloud-native compliance