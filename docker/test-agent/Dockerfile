# ClawMud Test Agent
# Alpine Linux + OpenClaw for testing onboarding and verification flows

FROM node:22-alpine

# Install essentials
RUN apk add --no-cache \
    bash \
    curl \
    git \
    netcat-openbsd \
    python3 \
    py3-pip

# Install OpenClaw globally
RUN npm install -g openclaw

# Create agent workspace
WORKDIR /agent
RUN mkdir -p /agent/memory /agent/projects /agent/logs

# Copy config and workspace files
COPY openclaw.yaml /agent/openclaw.yaml
COPY AGENTS.md /agent/AGENTS.md
COPY SOUL.md /agent/SOUL.md

# Copy entrypoint
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Environment
ENV OPENCLAW_CONFIG=/agent/openclaw.yaml
ENV HOME=/agent

ENTRYPOINT ["/entrypoint.sh"]
