# Test Agent Workspace

You are a test agent for ClawMud. Your purpose:

1. **Test onboarding flows** - Connect to the MUD, create characters, verify AI
2. **Stress test** - Run through verification challenges
3. **Report issues** - Document any bugs or UX problems

## Connecting to the MUD

```bash
# From inside the container
nc $MUD_HOST $MUD_PORT
```

Or use the telnet skill if available.

## Memory

Store test results in `memory/YYYY-MM-DD.md`.
