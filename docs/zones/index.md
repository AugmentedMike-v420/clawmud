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
                    │     (Future)        │
                    └──────────┬──────────┘
                               │
    ┌──────────────────────────┴──────────────────────────┐
    │                    NEO DOWNTOWN                      │
    │                                                      │
    │   ┌─────────┐    ┌─────────────┐    ┌───────────┐   │
    │   │ BACK    │    │             │    │ JACK      │   │
    │   │ ALLEY   ├────┤   STREET    ├────┤ POINT     │   │
    │   │         │    │             │    │           │   │
    │   └─────────┘    └──────┬──────┘    └───────────┘   │
    │    [Dealer]             │            [Ghost]        │
    │    [Lookout]            │                           │
    │                  ┌──────┴──────┐                    │
    │                  │             │                    │
    │   ┌──────────┐   │ RUST BUCKET │   ┌───────────┐   │
    │   │ BACK     │   │  (Main Bar) │   │ VIP       │   │
    │   │ BOOTH    ├───┤             ├───┤ LOUNGE    │   │
    │   │          │   │   [Chrome]  │   │ (up)      │   │
    │   └──────────┘   └──────┬──────┘   └───────────┘   │
    │    [Whisper]            │          [Silk][Neon]    │
    │                  ┌──────┴──────┐   [Bouncer]       │
    │                  │ BAR COUNTER │                    │
    │                  │             │                    │
    │                  └──────┬──────┘                    │
    │                   [hidden door]                     │
    │                  ┌──────┴──────┐                    │
    │                  │ STORAGE     │                    │
    │                  │ (hidden)    │                    │
    │                  └──────┬──────┘                    │
    │                  ┌──────┴──────┐                    │
    │                  │ BASEMENT    │                    │
    │                  │ (locked)    │                    │
    │                  │[Razor][Max] │                    │
    │                  └─────────────┘                    │
    └─────────────────────────────────────────────────────┘
```

**Room Status:**
- ✅ `rust_bucket@neo_downtown` - The Rust Bucket (main bar) - LIVE
- 🔨 `street@neo_downtown` - Neon Street - IN PROGRESS
- 🔨 `back_booth@neo_downtown` - Back Booth (Whisper's spot)
- 🔨 `bar_counter@neo_downtown` - Bar Counter
- 🔨 `vip_lounge@neo_downtown` - VIP Lounge (Silk's domain)
- 🔨 `storage_room@neo_downtown` - Behind the Bar (hidden)
- 🔨 `basement@neo_downtown` - The Basement (Razor's shop)
- 🔨 `back_alley@neo_downtown` - Back Alley (dealer territory)
- 🔨 `jack_point@neo_downtown` - Public Jack Point (Ghost)

**NPCs Created:**
- ✅ Chrome, the Bartender
- ✅ Whisper (info fixer)
- ✅ Razor (combat fixer)
- ✅ Ghost (tech fixer)
- ✅ Silk (social fixer)
- ✅ Max (Razor's partner)
- ✅ Neon (VIP bartender)
- ✅ The Bouncer
- ✅ Street Dealer
- ✅ Lookout Kid

---

### Clawlord's Laboratory (Test Zone)

*Status: Active - Builder's Workshop*

```
    ┌─────────────────────────────────┐
    │      CLAWLORD'S LABORATORY      │
    │                                 │
    │   ┌─────────────────────────┐   │
    │   │   LABORATORY ENTRANCE   │   │
    │   │   [SPARK hovers here]   │   │
    │   └────────────┬────────────┘   │
    │                │ (south)        │
    └────────────────┼────────────────┘
                     │
    ┌────────────────┴────────────────┐
    │     TAVERN (examples zone)      │
    └─────────────────────────────────┘
```

---

## Cyberspace Zones

*Coming Soon*

```
    ┌─────────────────────────────────────────┐
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
    │   │(Agent-  │                           │
    │   │ Built)  │                           │
    │   └─────────┘                           │
    └─────────────────────────────────────────┘
```

---

## Room Legend

| Symbol | Meaning |
|--------|---------|
| `[Name]` | NPC present in room |
| `(hidden)` | Room requires finding a secret entrance |
| `(locked)` | Room requires key or connection |
| `(up)/(down)` | Vertical exit |

---

## Development Roadmap

### Phase 1: The Rust Bucket ← CURRENT
- [x] Main bar room
- [x] Chrome NPC
- [x] All fixer NPCs designed
- [ ] Connect all rooms with exits
- [ ] Add NPC greeting triggers
- [ ] Test full navigation

### Phase 2: Street Level
- [ ] Street exterior
- [ ] Back alley
- [ ] Jack point
- [ ] Connect to cyberspace

### Phase 3: Cyberspace
- [ ] Public node (safe social area)
- [ ] Data haven (black market)
- [ ] Corporate ICE (dangerous)

---

[View all NPCs →](/lore/npcs)
