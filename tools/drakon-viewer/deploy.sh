#!/bin/bash

# Deploy DRAKON Viewer to nginx container
# Usage: ./deploy.sh [commit_message]

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CONTAINER_NAME="motia_drakon_viewer"

echo "🚀 DRAKON Viewer Deployment Script"
echo "=================================="
echo ""

# Check if container is running
if ! docker ps | grep -q "$CONTAINER_NAME"; then
    echo "❌ Error: Container $CONTAINER_NAME is not running"
    exit 1
fi

echo "✅ Container $CONTAINER_NAME is running"
echo ""

# Git operations
cd "$SCRIPT_DIR/../.."

if [ -n "$(git status --porcelain)" ]; then
    echo "📝 Changes detected. Committing..."

    # Add files
    git add tools/drakon-viewer/public/

    # Use provided commit message or default
    COMMIT_MSG="${1:-Update DRAKON Viewer}"

    git commit -m "$COMMIT_MSG

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>"

    echo "✅ Changes committed"
    echo ""

    # Push to remote
    echo "📤 Pushing to remote..."
    git push origin main
    echo "✅ Pushed to remote"
    echo ""
else
    echo "ℹ️  No changes to commit"
    echo ""
fi

# Restart nginx container
echo "🔄 Restarting nginx container..."
docker restart "$CONTAINER_NAME" > /dev/null
sleep 2

# Verify container is running
if docker ps | grep -q "$CONTAINER_NAME"; then
    echo "✅ Container restarted successfully"
else
    echo "❌ Error: Container failed to restart"
    exit 1
fi

echo ""
echo "🎉 Deployment completed!"
echo ""
echo "🌐 Your site is live at: https://dangerboys.exodus.pp.ua/"
echo ""
echo "📋 Next steps:"
echo "   - Test the changes in browser"
echo "   - Check browser console for errors"
echo "   - Clear browser cache if needed (Ctrl+Shift+R)"
