#!/bin/bash

# Set variables
PROJECT_ID="workout-app-441723"
REGION="us-central1"
REPOSITORY="workout-app"

# Enable BuildKit for multi-platform builds
export DOCKER_BUILDKIT=1

# Create a new builder if it doesn't exist
docker buildx create --name multiplatform-builder --use || true
docker buildx use multiplatform-builder

# Build and push Spring Backend
echo "Building and pushing Spring Backend..."
docker buildx build \
  --platform linux/amd64,linux/arm64 \
  --tag "${REGION}-docker.pkg.dev/${PROJECT_ID}/${REPOSITORY}/spring-backend:latest" \
  --target backend-builder \
  --push \
  .

# Build and push React Frontend
echo "Building and pushing React Frontend..."
docker buildx build \
  --platform linux/amd64,linux/arm64 \
  --tag "${REGION}-docker.pkg.dev/${PROJECT_ID}/${REPOSITORY}/react-frontend:latest" \
  --target frontend-final \
  --push \
  .

echo "Build and push completed!"