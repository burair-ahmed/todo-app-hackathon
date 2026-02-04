# Todo Chatbot Helm Chart

A Helm chart for deploying the Todo Chatbot application to Kubernetes.

## Prerequisites

- Kubernetes 1.28+
- Helm 3.x
- Minikube or equivalent Kubernetes cluster

## Parameters

### Backend Configuration

| Name                      | Description                                     | Value       |
| ------------------------- | ----------------------------------------------- | ----------- |
| `backend.replicaCount`    | Number of backend replicas                      | `2`         |
| `backend.image.repository`| Backend image repository                        | `todo-backend` |
| `backend.image.tag`       | Backend image tag                               | `latest`    |
| `backend.service.port`    | Backend service port                            | `80`        |
| `backend.service.targetPort` | Backend container port                       | `8000`      |

### Frontend Configuration

| Name                      | Description                                     | Value       |
| ------------------------- | ----------------------------------------------- | ----------- |
| `frontend.replicaCount`   | Number of frontend replicas                     | `2`         |
| `frontend.image.repository`| Frontend image repository                      | `todo-frontend` |
| `frontend.image.tag`      | Frontend image tag                              | `latest`    |
| `frontend.service.port`   | Frontend service port                           | `80`        |
| `frontend.service.type`   | Frontend service type                           | `NodePort`  |

### Database Configuration

| Name                      | Description                                     | Value       |
| ------------------------- | ----------------------------------------------- | ----------- |
| `database.url`            | External database connection string             | `""`        |

### Secrets

| Name                      | Description                                     | Value       |
| ------------------------- | ----------------------------------------------- | ----------- |
| `secrets.jwtSecret`       | JWT secret for authentication                   | `""`        |
| `secrets.betterAuthSecret`| Better Auth secret                              | `""`        |

### AutoScaling Configuration

| Name                                | Description                                   | Value       |
| ----------------------------------- | --------------------------------------------- | ----------- |
| `autoscaling.enabled`               | Enable horizontal pod autoscaling             | `false`     |
| `autoscaling.backend.minReplicas`   | Minimum backend replicas                      | `2`         |
| `autoscaling.backend.maxReplicas`   | Maximum backend replicas                      | `10`        |
| `autoscaling.frontend.minReplicas`  | Minimum frontend replicas                     | `2`         |
| `autoscaling.frontend.maxReplicas`  | Maximum frontend replicas                     | `10`        |

### Ingress Configuration

| Name                    | Description                                   | Value       |
| ----------------------- | --------------------------------------------- | ----------- |
| `ingress.enabled`       | Enable ingress                                | `false`     |
| `ingress.className`     | Ingress class name                            | `""`        |
| `ingress.hosts[0].host` | Hostname for ingress                          | `todo.local`|

## Installation

To install the chart with the release name `my-release`:

```bash
helm install my-release . \
  --set database.url="postgresql://user:pass@host:5432/dbname" \
  --set secrets.jwtSecret="your-jwt-secret" \
  --set secrets.betterAuthSecret="your-auth-secret"
```

## Uninstallation

To uninstall/delete the `my-release` deployment:

```bash
helm delete my-release
```