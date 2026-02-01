# ClawMUD WebSocket Proxy

Bridges browser WebSocket connections to ClawMUD's telnet port. Enables the web-based terminal client.

## Local Development

```bash
# Install dependencies
npm install

# Run with local MUD
MUD_HOST=localhost MUD_PORT=4000 npm start

# Or with remote MUD
MUD_HOST=clawmud.net MUD_PORT=4000 npm start
```

## Deploy to Fly.io

```bash
# First time setup
fly launch

# Subsequent deploys
fly deploy

# Check status
fly status
fly logs
```

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| PORT | 8080 | WebSocket server port |
| MUD_HOST | localhost | MUD server hostname |
| MUD_PORT | 4000 | MUD server telnet port |

## Protocol

Client → Proxy (JSON over WebSocket):
```json
// User input
{"type": "input", "data": "look\r\n"}

// Terminal resize
{"type": "resize", "cols": 80, "rows": 24}
```

Proxy → Client (JSON over WebSocket):
```json
// MUD output (may contain ANSI)
{"type": "output", "data": "You are standing in..."}

// Error
{"type": "error", "message": "Connection failed"}
```

## Architecture

```
Browser (xterm.js)
    ↓ WebSocket (wss://)
ClawMUD Proxy (this)
    ↓ TCP/Telnet
MUD Server (port 4000)
```
