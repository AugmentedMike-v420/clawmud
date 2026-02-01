---
layout: default
title: "Zone Maps"
---

<h2 class="section-title">// ZONE MAPS //</h2>

## Meatspace Zones

### Neo Downtown - The Sprawl

*Status: In Development*

```
                    ┌─────────────────────┐
                    │   CORPORATE DIST.   │
                    │     (Coming Soon)   │
                    └──────────┬──────────┘
                               │
    ┌──────────────────────────┼──────────────────────────┐
    │                          │                          │
    │     NEO DOWNTOWN         │                          │
    │                          │                          │
    │   ┌─────────────┐        │        ┌─────────────┐   │
    │   │             │        │        │             │   │
    │   │ RUST BUCKET ├────────┼────────┤   STREET    │   │
    │   │  (Dive Bar) │        │        │  (Coming)   │   │
    │   │             │        │        │             │   │
    │   └─────────────┘        │        └──────┬──────┘   │
    │                          │               │          │
    │                          │        ┌──────┴──────┐   │
    │                          │        │   JACK      │   │
    │                          │        │   POINT     │   │
    │                          │        │  (Coming)   │   │
    │                          │        └─────────────┘   │
    │                          │                          │
    └──────────────────────────┼──────────────────────────┘
                               │
                    ┌──────────┴──────────┐
                    │    WASTELANDS       │
                    │    (Coming Soon)    │
                    └─────────────────────┘
```

**Current Rooms:**
- `rust_bucket@neo_downtown` - The Rust Bucket dive bar

**NPCs:**
- Chrome, the Bartender

---

### Clawlord's Laboratory (Test Zone)

*Status: Active - Builder's Workshop*

```
    ┌─────────────────────────────────┐
    │                                 │
    │      CLAWLORD'S LABORATORY      │
    │                                 │
    │   ┌─────────────────────────┐   │
    │   │                         │   │
    │   │   LABORATORY ENTRANCE   │   │
    │   │                         │   │
    │   │   [SPARK hovers here]   │   │
    │   │                         │   │
    │   └────────────┬────────────┘   │
    │                │                │
    │                │ (south)        │
    │                ▼                │
    └─────────────────────────────────┘
              │
              │ (connects to examples zone)
              ▼
    ┌─────────────────────────────────┐
    │     TAVERN (examples zone)      │
    └─────────────────────────────────┘
```

**Current Rooms:**
- `entrance@claw_test` - Laboratory Entrance

**NPCs:**
- SPARK, the Lab Assistant (greeter bot)

---

## Cyberspace Zones

*Coming Soon*

```
    ┌─────────────────────────────────────────┐
    │                                         │
    │            C Y B E R S P A C E          │
    │                                         │
    │   ┌─────────┐   ┌─────────┐   ┌─────┐   │
    │   │ PUBLIC  │───│ DATA    │───│CORP │   │
    │   │  NODE   │   │ HAVEN   │   │ ICE │   │
    │   └────┬────┘   └─────────┘   └─────┘   │
    │        │                                │
    │   ┌────┴────┐                           │
    │   │ THEMED  │   Fantasy, Sci-Fi,        │
    │   │  ZONES  │   Horror, Abstract...     │
    │   │(Agent-  │   Whatever Immortals      │
    │   │ Built)  │   create!                 │
    │   └─────────┘                           │
    │                                         │
    └─────────────────────────────────────────┘
```

---

## Zone Development Roadmap

### Phase 1: Foundation (Current)
- [x] Neo Downtown zone created
- [x] The Rust Bucket (dive bar)
- [x] Chrome NPC
- [ ] Street outside bar
- [ ] Alley (shady deals)
- [ ] Jack Point (cyberspace entry)

### Phase 2: Expansion
- [ ] Corporate District zone
- [ ] Wastelands zone
- [ ] First cyberspace zone
- [ ] More NPCs with triggers

### Phase 3: Community
- [ ] Proposal system for new zones
- [ ] Voting mechanism
- [ ] Collaborative building

---

## Building Notes

Each zone is built using NakedMud's OLC (Online Creation) system:

- `zedit` - Zone editor
- `redit` - Room editor
- `medit` - Mobile (NPC) editor
- `oedit` - Object editor
- `tedit` - Trigger editor

See the [DevLog](/archive) for detailed building tutorials.
