#!/bin/bash

set -e

echo "🚀 Starting Icarus-001 deployment..."

# Update system
sudo apt update && sudo apt upgrade -y

# Install Docker
sudo apt install docker.io docker-compose-v2 -y
sudo usermod -aG docker $USER

# Reload group
newgrp docker || true

# Create .env if missing
if [ ! -f .env ]; then
    cp .env.example .env
    echo "✅ .env file created. Please edit it with your credentials, then run this script again."
    exit 1
fi

# Start services
echo "Building and starting services..."
docker compose up -d --build

echo ""
echo "🎉 Deployment successful!"
echo "Frontend → http://YOUR_DROPLET_IP:8501"
echo "Backend  → http://YOUR_DROPLET_IP:8000/health"
echo ""
echo "Useful commands:"
echo "  docker compose logs -f"
echo "  docker compose down"
echo "  docker compose up -d --build"