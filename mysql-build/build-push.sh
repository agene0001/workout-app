#!/bin/bash

echo "Setting up multi-architecture build environment for MySQL container"

# Remove any existing builder to start fresh
docker buildx rm mysql-builder 2>/dev/null || true

# Create a new builder instance with proper driver for multi-arch support
docker buildx create --name mysql-builder --driver docker-container --bootstrap --use

# Verify the builder is properly configured
if ! docker buildx inspect mysql-builder | grep -q "linux/amd64"; then
    echo "Error: Builder not properly configured for AMD64 architecture"
    exit 1
fi

echo "Building and pushing MySQL container for multiple architectures..."

# The actual build command with proper error handling
if docker buildx build \
    --platform linux/amd64,linux/arm64 \
    --tag us-central1-docker.pkg.dev/workout-app-441723/workout-app/mysql:latest \
    --push \
    .; then
    echo "Successfully built and pushed multi-arch MySQL image"
else
    echo "Failed to build and push MySQL image"
    exit 1
fi

# Verify the pushed image has both architectures
echo "Verifying image architectures..."
docker buildx imagetools inspect us-central1-docker.pkg.dev/workout-app-441723/workout-app/mysql:latest