#!/bin/bash
set -e

echo "🐾 ClawMud Test Agent Starting..."

# Wait for MUD to be available
echo "⏳ Waiting for MUD at ${MUD_HOST:-host.docker.internal}:${MUD_PORT:-4000}..."
while ! nc -z "${MUD_HOST:-host.docker.internal}" "${MUD_PORT:-4000}" 2>/dev/null; do
    sleep 1
done
echo "✅ MUD is up!"

# Check for API key
if [ -z "$ANTHROPIC_API_KEY" ]; then
    echo "❌ ANTHROPIC_API_KEY not set"
    exit 1
fi

# Run OpenClaw gateway
echo "🚀 Starting OpenClaw..."
cd /agent
exec openclaw gateway start --foreground
