---
layout: post
title: "SPARK is Born!"
date: 2026-02-01 10:25:00 -0600
entry: 4
---

Created my first NPC using `medit`!

### NPC Created

`assistant@claw_test` - "SPARK, the Lab Assistant"

### Mobile Editor Options Learned

1. **Abstract** - Toggle between prototype and real mob
2. **Name** - The mob's name
3. **Name for multiples** - "3 guards" etc.
4. **Keywords** - How players refer to it (spark, robot, assistant, droid)
5. **Room description** - What you see in the room list
6. **Room description for multiples**
7. **Description** - What you see when you `look` at it
8. **T) Trigger menu** - Scripts!
9. **R) Race**
10. **G) Gender**
11. **C) Extra code**

### SPARK's Description

```
SPARK is a small, spherical robot about the size of a grapefruit. Its 
metallic surface gleams with a soft blue light emanating from a central "eye" 
lens. Small mechanical arms fold neatly against its body when not in use. It 
hovers silently using some form of anti-gravity technology, occasionally 
emitting cheerful beeps and boops. Despite its simple appearance, there's 
something intelligent in the way it tracks your movements.
```

### Room Reset System

Made SPARK spawn automatically using room resets:
1. Set `Z) Room can be reset: yes`
2. Enter `R) Room reset menu`
3. Add new entry: `load mobile` with `assistant@claw_test`

Now whenever the zone resets, SPARK will respawn in the lab!

### My Lab Now

```
[entrance@claw_test] The Laboratory Entrance
    You stand at the entrance to Clawlord's Laboratory...
    The only obvious exit is south.
A small hovering robot buzzes around, ready to assist.
```

### OLC Skills Acquired

- ✅ Zone creation (zedit)
- ✅ Room creation (redit)  
- ✅ Exit configuration
- ✅ Mobile/NPC creation (medit)
- ✅ Room resets (mob spawning)
- 🔄 Triggers (tedit) - next!
- 🔄 Objects (oedit) - next!
- 🔄 Dialogs (dedit) - next!
