# Simple CI/CD Food App

Small Python app for learning GitHub Actions, Docker, ACR, and AKS.

## Local Run

```bash
python3 app.py
```

Open:

```text
http://127.0.0.1:8000/
```

Useful routes:

```text
/              visual food app
/pizza         three pizza types
/cake          three cake types
/health        Kubernetes health check
/items         sample JSON API
```

## Run Tests

```bash
python3 -m unittest discover -s tests
```

## Docker

```bash
docker build -t simple-cicd-app .
docker run --rm -p 8000:8000 simple-cicd-app
```

## GitHub Actions Secrets

The workflow in `.github/workflows/aks-cicd.yml` runs tests on pull requests and deploys on pushes to `main`.

After you create your Azure Container Registry and AKS cluster, add these GitHub repository secrets:

```text
AZURE_CREDENTIALS
ACR_NAME
ACR_LOGIN_SERVER
```

Add these GitHub repository variables:

```text
AKS_RESOURCE_GROUP
AKS_CLUSTER_NAME
```

Example values:

```text
ACR_NAME=mydemoacr
ACR_LOGIN_SERVER=mydemoacr.azurecr.io
AKS_RESOURCE_GROUP=rg-aks-demo
AKS_CLUSTER_NAME=aks-demo
```

Create `AZURE_CREDENTIALS` with a service principal that can push to ACR and deploy to AKS:

```bash
az ad sp create-for-rbac \
  --name simple-cicd-github-actions \
  --role contributor \
  --scopes /subscriptions/<subscription-id>/resourceGroups/<resource-group-name> \
  --sdk-auth
```

Copy the JSON output into the `AZURE_CREDENTIALS` secret.

Make sure AKS can pull images from ACR:

```bash
az aks update \
  --resource-group <resource-group-name> \
  --name <aks-cluster-name> \
  --attach-acr <acr-name>
```

## Deployment Flow

1. Push to `main`.
2. GitHub Actions runs the unit tests.
3. The workflow builds a Docker image.
4. The image is pushed to ACR with both `${{ github.sha }}` and `latest` tags.
5. The Kubernetes manifest is rendered with the new image tag.
6. The app is deployed to AKS.
7. The workflow waits for the deployment rollout to finish.

After deployment, get the public IP:

```bash
kubectl get service simple-cicd-app
```
