# Data Model: Cloud Native Todo Chatbot Deployment

## Kubernetes Resources

### Backend Deployment
**Entity**: BackendDeployment
- **kind**: Deployment
- **apiVersion**: apps/v1
- **metadata**:
  - name: todo-backend
  - namespace: default
- **spec**:
  - replicas: 2 (scalable)
  - selector: matchLabels: app=todo-backend
  - template: Pod template with labels app=todo-backend
  - containers:
    - name: backend
    - image: todo-backend:latest
    - ports: [{containerPort: 8000, name: http}]
    - envFrom: [{configMapRef: {name: backend-config}}, {secretRef: {name: backend-secrets}}]
    - resources: {requests: {memory: "256Mi", cpu: "250m"}, limits: {memory: "512Mi", cpu: "500m}}
    - livenessProbe: {httpGet: {path: /health, port: 8000}, initialDelaySeconds: 30, periodSeconds: 10}
    - readinessProbe: {httpGet: {path: /ready, port: 8000}, initialDelaySeconds: 5, periodSeconds: 5}

### Backend Service
**Entity**: BackendService
- **kind**: Service
- **apiVersion**: v1
- **metadata**:
  - name: todo-backend-svc
  - namespace: default
- **spec**:
  - selector: app=todo-backend
  - ports: [{protocol: TCP, port: 80, targetPort: 8000, name: http}]
  - type: ClusterIP

### Frontend Deployment
**Entity**: FrontendDeployment
- **kind**: Deployment
- **apiVersion**: apps/v1
- **metadata**:
  - name: todo-frontend
  - namespace: default
- **spec**:
  - replicas: 2 (scalable)
  - selector: matchLabels: app=todo-frontend
  - template: Pod template with labels app=todo-frontend
  - containers:
    - name: frontend
    - image: todo-frontend:latest
    - ports: [{containerPort: 3000, name: http}]
    - env: [{name: BACKEND_URL, value: http://todo-backend-svc:80}]
    - resources: {requests: {memory: "128Mi", cpu: "100m"}, limits: {memory: "256Mi", cpu: "200m}}
    - livenessProbe: {httpGet: {path: /health, port: 3000}, initialDelaySeconds: 30, periodSeconds: 10}
    - readinessProbe: {httpGet: {path: /, port: 3000}, initialDelaySeconds: 5, periodSeconds: 5}

### Frontend Service
**Entity**: FrontendService
- **kind**: Service
- **apiVersion**: v1
- **metadata**:
  - name: todo-frontend-svc
  - namespace: default
- **spec**:
  - selector: app=todo-frontend
  - ports: [{protocol: TCP, port: 80, targetPort: 3000, name: http}]
  - type: NodePort (for external access)

### ConfigMap
**Entity**: AppConfigMap
- **kind**: ConfigMap
- **apiVersion**: v1
- **metadata**:
  - name: todo-app-config
  - namespace: default
- **data**:
  - BACKEND_SERVICE_HOST: todo-backend-svc
  - BACKEND_SERVICE_PORT: "80"
  - NODE_ENV: production
  - LOG_LEVEL: info

### Secrets
**Entity**: AppSecrets
- **kind**: Secret
- **apiVersion**: v1
- **metadata**:
  - name: todo-app-secrets
  - namespace: default
- **type**: Opaque
- **data**:
  - DATABASE_URL: (base64 encoded)
  - JWT_SECRET: (base64 encoded)
  - BETTER_AUTH_SECRET: (base64 encoded)

### Ingress (Optional)
**Entity**: AppIngress
- **kind**: Ingress
- **apiVersion**: networking.k8s.io/v1
- **metadata**:
  - name: todo-app-ingress
  - namespace: default
  - annotations: {kubernetes.io/ingress.class: nginx, nginx.ingress.kubernetes.io/rewrite-target: /}
- **spec**:
  - rules:
    - host: todo.local
      http:
        paths:
          - path: /
            pathType: Prefix
            backend: {service: {name: todo-frontend-svc, port: {number: 80}}}
          - path: /api
            pathType: Prefix
            backend: {service: {name: todo-backend-svc, port: {number: 80}}}

### Horizontal Pod Autoscaler (Future)
**Entity**: HPA
- **kind**: HorizontalPodAutoscaler
- **apiVersion**: autoscaling/v2
- **metadata**:
  - name: todo-backend-hpa
- **spec**:
  - scaleTargetRef: {apiVersion: apps/v1, kind: Deployment, name: todo-backend}
  - minReplicas: 2
  - maxReplicas: 10
  - metrics: [{type: Resource, resource: {name: cpu, target: {type: Utilization, averageUtilization: 70}}}]

## Relationships

- Frontend Deployment → Backend Service (via service discovery)
- Deployments → Services (via selectors)
- Deployments → ConfigMap/Secrets (via volume mounts/envFrom)
- Ingress → Services (via backend references)

## Validation Rules

### Deployment Validation
- All deployments must have replica count >= 1
- All deployments must have resource requests and limits defined
- All deployments must have health checks configured
- ImagePullPolicy should be set appropriately

### Service Validation
- Services must have matching selectors for deployments
- Port configurations must match container ports
- Service types must be appropriate for intended access

### Security Validation
- Secrets must not be stored in ConfigMaps
- Container images must come from trusted registries
- Privileged containers must be justified

## State Transitions

### Deployment Lifecycle
- Pending → ContainerCreating → Running → Terminating (based on Kubernetes pod lifecycle)
- Healthy → Unhealthy → Recovering → Healthy (based on health probe status)

### Scaling Events
- Normal Load → High Load → Scale Up → Stable High Load → Low Load → Scale Down → Normal Load