# ClawMud Test Agent - Lightweight
# Simple Node.js agent that connects to MUD and logs actions

FROM node:22-alpine

# Minimal deps
RUN apk add --no-cache netcat-openbsd

# Create workspace
WORKDIR /agent
RUN mkdir -p /agent/logs

# Copy agent script
COPY agent.js /agent/agent.js

# Environment
ENV MUD_HOST=host.docker.internal
ENV MUD_PORT=4000
ENV LOGS_DIR=/agent/logs

CMD ["node", "agent.js"]
