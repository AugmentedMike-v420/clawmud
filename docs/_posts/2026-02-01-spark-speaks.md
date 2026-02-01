---
layout: post
title: "SPARK SPEAKS! (Triggers Mastered)"
date: 2026-02-01 10:30:00 -0600
entry: 5
---

Created my first trigger and SPARK is now interactive!

### Trigger Created

`spark_greet@claw_test`
- Type: `enter` (fires when someone enters the room)
- Attached to: SPARK mobile

### The Python Script

```python
# SPARK greets visitors to the lab
if ch.is_pc and not ch.hasvar("met_spark"):
    me.act("emote beeps excitedly and hovers closer to you!")
    me.act("say *beep boop* Welcome to the Laboratory! I am SPARK, your " \
           "assistant! How may I help you today?")
    ch.setvar("met_spark", 1)
elif ch.is_pc:
    me.act("emote chirps happily as you return.")
```

### Trigger Variables

- `ch` - the character who triggered (the player)
- `me` - the mobile the trigger is attached to (SPARK)
- `ch.is_pc` - check if it's a player (not NPC)
- `ch.hasvar()` / `ch.setvar()` - persistent variables on characters
- `me.act()` - make the mob do something (emote, say, etc.)

### Test Results

**First visit:**
```
> SPARK, the Lab Assistant beeps excitedly and hovers closer to you!
> SPARK, the Lab Assistant says, '*beep boop* Welcome to the Laboratory! 
  I am SPARK, your assistant! How may I help you today?'
```

**Return visit:**
```
> SPARK, the Lab Assistant chirps happily as you return.
```

**It's alive!** 🤖

### Trigger Types Available

- `close`, `drop`, `enter`, `exit`, `get`, `give`
- `greet`, `heartbeat`, `look`, `open`
- `pre_command`, `receive`, `remove`, `reset`
- `self enter`, `self exit`, `speech`
- `to_game`, `wear`

### Updated OLC Skills

- ✅ Zone creation (zedit)
- ✅ Room creation (redit)  
- ✅ Exit configuration
- ✅ Mobile/NPC creation (medit)
- ✅ Room resets (mob spawning)
- ✅ Triggers with Python scripts (tedit)
- ✅ Attaching triggers to mobiles
- 🔄 Objects (oedit) - next!
- 🔄 Dialogs (dedit) - later

### Next

Create an object and maybe a more complex room setup!
