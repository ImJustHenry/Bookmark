#!/bin/bash
# Deployment script for Bookmark application
# This script builds the Docker image and provides deployment options

set -e  # Exit on error

SCRIPT_PATH="$(readlink -f "${BASH_SOURCE[0]}")"
SCRIPT_DIR="$(dirname "$SCRIPT_PATH")"
cd "$SCRIPT_DIR"
cd ..

echo "🚀 Starting deployment process..."

# Build Docker image
echo "📦 Building Docker image..."
docker build -t bookmark-app:latest .

echo "✅ Docker image built successfully!"

# Check if docker-compose is available
if command -v docker-compose &> /dev/null || command -v docker compose &> /dev/null; then
    echo ""
    echo "📋 Available deployment options:"
    echo "1. Run with docker-compose (recommended for local/staging)"
    echo "2. Run Docker container directly"
    echo "3. Save Docker image to tar file"
    echo ""
    read -p "Choose option (1-3) or press Enter to exit: " choice
    
    case $choice in
        1)
            echo "🐳 Starting with docker-compose..."
            docker-compose up -d || docker compose up -d
            echo "✅ Application deployed! Access at http://localhost:3000"
            ;;
        2)
            echo "🐳 Running Docker container..."
            docker run -d -p 3000:3000 --name bookmark-app bookmark-app:latest
            echo "✅ Application deployed! Access at http://localhost:3000"
            ;;
        3)
            echo "💾 Saving Docker image..."
            mkdir -p ./build
            docker save -o ./build/bookmarkimage.tar bookmark-app:latest
            echo "✅ Image saved to ./build/bookmarkimage.tar"
            ;;
        *)
            echo "Exiting..."
            ;;
    esac
else
    echo "⚠️  docker-compose not found. Running Docker container directly..."
    docker run -d -p 3000:3000 --name bookmark-app bookmark-app:latest
    echo "✅ Application deployed! Access at http://localhost:3000"
fi

echo ""
echo "📊 Container status:"
docker ps | grep bookmark-app || echo "Container not running"

