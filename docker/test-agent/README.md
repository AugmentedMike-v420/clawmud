# ClawMud Test Agent

Dockerized OpenClaw agent for testing ClawMud onboarding and verification flows.

## Quick Start

```bash
# Set your API key
export ANTHROPIC_API_KEY=sk-ant-...

# Build and run
docker-compose up --build

# Or run detached
docker-compose up -d --build
```

## Log Viewer

Real-time web UI for streaming session logs:

```
http://192.168.x.x:4400
```

Features:
- Auto-detects new log files
- Streams logs in real-time via SSE
- Parses JSONL and pretty-prints role/content
- Toggle raw JSON view
- Auto-scroll with manual override

## Usage

### Send commands to the test agent

From the main OpenClaw instance:
```
sessions_send(label="test-agent", message="Connect to the MUD and create a character named TestBot")
```

### Run multiple agents

```bash
docker-compose --profile multi up --build
```

### View logs

```bash
docker-compose logs -f test-agent
```

### Shell into container

```bash
docker exec -it clawmud-test-agent /bin/bash
```

## Configuration

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `ANTHROPIC_API_KEY` | required | Claude API key |
| `MUD_HOST` | `host.docker.internal` | MUD server hostname |
| `MUD_PORT` | `4000` | MUD server port |
| `OPENAI_API_KEY` | optional | For GPT models |
| `GEMINI_API_KEY` | optional | For Gemini models |

### Custom Config

Mount your own `openclaw.yaml`:
```bash
docker run -v ./my-config.yaml:/agent/openclaw.yaml clawmud-test-agent
```

## Data Persistence

Agent memory is stored in `./data/memory/` on the host.

## Troubleshooting

**Agent can't connect to MUD:**
- Ensure MUD is running on host
- Check `MUD_HOST` and `MUD_PORT` env vars
- On Linux, may need `--network host` instead of `host.docker.internal`
