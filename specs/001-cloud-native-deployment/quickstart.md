# Quickstart: Cloud Native Todo Chatbot Deployment

## Prerequisites

- Docker Desktop with Kubernetes enabled OR Minikube
- Helm 3.x
- kubectl
- kubectl-ai (optional, for AI-assisted operations)
- kagent (optional, for cluster analysis)

## Setup Instructions

### 1. Environment Preparation

```bash
# Install required tools (using package manager like Chocolatey on Windows)
choco install minikube kubernetes-cli helm

# Or using other package managers
# brew install minikube kubernetes-cli helm  # macOS
# sudo snap install minikube --classic      # Ubuntu

# Start Minikube
minikube start --cpus=4 --memory=8192 --disk-size=20g

# Enable ingress addon (if needed)
minikube addons enable ingress

# Verify Kubernetes cluster
kubectl cluster-info
```

### 2. Clone and Prepare the Repository

```bash
# Clone the repository (if not already done)
git clone <repository-url>
cd <repository-directory>

# Switch to the cloud-native deployment branch
git checkout 001-cloud-native-deployment
```

### 3. Build Docker Images

```bash
# Navigate to backend directory
cd backend/

# Build backend Docker image
docker build -t todo-backend:latest .

# Navigate to frontend directory
cd ../frontend/

# Build frontend Docker image
docker build -t todo-frontend:latest .

# Tag images for local registry if needed
docker tag todo-backend:latest localhost:5000/todo-backend:latest
docker tag todo-frontend:latest localhost:5000/todo-frontend:latest
```

### 4. Configure Database Connection

Create a `.env` file or prepare your Neon PostgreSQL connection:

```bash
# Example .env for local testing (do not commit this file!)
DATABASE_URL="postgresql://username:password@neon-host.region.provider.neon.tech/dbname"
JWT_SECRET="your-jwt-secret"
BETTER_AUTH_SECRET="your-auth-secret"
```

### 5. Deploy Using Helm

```bash
# Navigate to charts directory
cd ../charts/

# Install the Helm chart
helm install todo-chatbot ./todo-chatbot \
  --set backend.image.repository=localhost:5000/todo-backend \
  --set backend.image.tag=latest \
  --set frontend.image.repository=localhost:5000/todo-frontend \
  --set frontend.image.tag=latest \
  --set database.url="postgresql://username:password@neon-host.region.provider.neon.tech/dbname" \
  --set secrets.jwtSecret="your-jwt-secret" \
  --set secrets.authSecret="your-auth-secret"

# Verify deployment
kubectl get pods
kubectl get services
kubectl get ingress  # if using ingress
```

### 6. Access the Application

```bash
# Get the frontend service URL
minikube service todo-frontend-svc --url

# Or if using ingress
minikube tunnel  # in a separate terminal
# Then access via configured hostname
```

## AI-Assisted Operations

### Using kubectl-ai

```bash
# Install kubectl-ai plugin
curl -L https://raw.githubusercontent.com/sozercan/kubectl-ai/main/install.sh | bash

# Example AI-assisted operations
kubectl ai "show me all pods in error state"
kubectl ai "scale frontend deployment to 4 replicas"
kubectl ai "describe why backend pods are not ready"
```

### Using Docker AI (Gordon)

```bash
# Enable Docker AI if available
# Use Docker Desktop interface to enable Gordon AI features
# Use AI to optimize Dockerfiles or troubleshoot container issues
```

## Verification Steps

1. **Check Pod Status**:
   ```bash
   kubectl get pods
   # All pods should show STATUS as Running
   ```

2. **Check Services**:
   ```bash
   kubectl get services
   # Services should show external IPs (if applicable)
   ```

3. **Check Application Health**:
   ```bash
   kubectl port-forward svc/todo-frontend-svc 8080:80
   # Visit http://localhost:8080 in browser
   ```

4. **Test Scaling**:
   ```bash
   kubectl scale deployment todo-frontend --replicas=3
   kubectl get pods  # Should show 3 frontend pods
   ```

## Troubleshooting

### Common Issues

1. **Images Not Found**: Ensure images are built and available in the cluster
   ```bash
   # For Minikube, load images directly
   minikube image load todo-backend:latest
   minikube image load todo-frontend:latest
   ```

2. **Database Connection Errors**: Verify database URL is correctly configured
   ```bash
   kubectl logs deployment/todo-backend
   ```

3. **Service Not Accessible**: Check service configuration and firewall settings
   ```bash
   kubectl describe service todo-frontend-svc
   ```

### Useful Commands

```bash
# View logs
kubectl logs -l app=todo-backend
kubectl logs -l app=todo-frontend

# Get detailed pod information
kubectl describe pods -l app=todo-backend

# Port forward for debugging
kubectl port-forward deployment/todo-backend 8000:8000

# Check resource usage
kubectl top nodes
kubectl top pods
```

## Cleanup

```bash
# Uninstall Helm release
helm uninstall todo-chatbot

# Stop Minikube
minikube stop

# Optionally delete Minikube VM
minikube delete
```