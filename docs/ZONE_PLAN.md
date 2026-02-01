# ClawMud Zone & Level Plan

## Overview

The world is structured by character level, ensuring players always have appropriate content.

```
┌─────────────────────────────────────────────────────────────────────┐
│                        WORLD STRUCTURE                              │
├─────────────────────────────────────────────────────────────────────┤
│  Level 1-5    │  STARTER ZONES      │  Safe, tutorial-like         │
│  Level 6-15   │  DOWNTOWN ZONES     │  Urban exploration           │
│  Level 16-25  │  INDUSTRIAL/COMBAT  │  Faction conflict            │
│  Level 26-40  │  CORPORATE/DEEP     │  High-stakes intrigue        │
│  Level 41-50  │  ENDGAME            │  Elite content               │
│  Immortal     │  CYBERSPACE         │  Builder/admin space         │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Starter Zones (Level 1-5)

**Purpose:** Teach mechanics, build confidence, no death penalty

### The Rust Bucket (Hub)
- **Level:** All (safe zone)
- **Type:** Social hub, quest givers
- **NPCs:** Chrome (bartender), fixers
- **Content:** 
  - Learn basic commands
  - Meet faction representatives
  - Accept first jobs

### Limbo (Tutorial)
- **Level:** 0-1
- **Type:** Tutorial, character creation
- **Content:** Basic movement, combat intro, race selection

### Back Alleys (Level 2-5)
- **Level:** 2-5
- **Type:** Light combat, exploration
- **Mobs:** Street punks (L2), junkies (L3), gang initiates (L4-5)
- **Loot:** Basic weapons, street cred, small credsticks
- **Quests:** Delivery runs, lookout jobs, minor heists

---

## Downtown Zones (Level 6-15)

**Purpose:** Introduce factions, urban density, choice-driven quests

### Street Level (Level 6-10)
- **Type:** Open urban exploration
- **Mobs:** Gang soldiers (L6-8), corrupt cops (L8-10), booster gangs (L7-9)
- **Factions:** Street gangs introduce faction reputation
- **Content:**
  - Territory control mini-game
  - Shop access based on rep
  - Night/day cycle affects spawns

### The Underground (Level 8-12)
- **Type:** Sewer/subway network
- **Mobs:** Scavs (L8-9), mutants (L10-11), rogue drones (L11-12)
- **Hazards:** Toxic zones, collapsed tunnels
- **Content:**
  - Hidden shortcuts between zones
  - Black market access
  - Smuggling routes

### Warehouse District (Level 11-15)
- **Type:** Semi-combat, heist prep
- **Mobs:** Security guards (L11-12), corpo mercs (L13-15), attack dogs (L11)
- **Content:**
  - Stealth optional
  - Loot caches
  - Faction job boards

---

## Industrial Zones (Level 16-25)

**Purpose:** Faction warfare, group content, meaningful choices

### Factory Complex (Level 16-20)
- **Type:** Combat-heavy, group recommended
- **Mobs:** Combat drones (L16-18), cyberpsychos (L18-20), mini-bosses
- **Bosses:** Factory Foreman (L20) - weekly spawn
- **Content:**
  - Crafting material farming
  - Faction territory wars
  - Environmental hazards

### Docks (Level 18-22)
- **Type:** Mixed combat/social
- **Mobs:** Smugglers (L18-19), Yakuza soldiers (L20-22), dock mechs (L21)
- **Factions:** Major faction headquarters here
- **Content:**
  - Import/export economy
  - Ship-based instances
  - Faction rank-up quests

### Combat Zone (Level 21-25)
- **Type:** Open PvP enabled, high risk/reward
- **Mobs:** Heavily armed gangs (L21-23), combat borgs (L24-25)
- **Rules:** 
  - Full loot drop on death
  - No safe zones
  - Bounty system active
- **Rewards:** Best gear drops, rare cyberware

---

## Corporate Zones (Level 26-40)

**Purpose:** Endgame prep, complex systems, high stakes

### Corporate Plaza (Level 26-30)
- **Type:** Social/intrigue, combat restricted
- **Content:**
  - Corporate reputation system
  - Stock market mini-game
  - Espionage missions
- **Access:** Requires SIN (System ID) or disguise

### Arcology (Level 28-35)
- **Type:** Vertical dungeon (100 floors)
- **Mobs:** Corporate security (scales with floor), elite guards, ICE programs
- **Bosses:** Floor bosses every 10 levels
- **Content:**
  - Elevator shortcuts unlock
  - Executive loot tables
  - Data heist missions

### Deep Net (Level 33-40)
- **Type:** Cyberspace combat
- **Mobs:** ICE constructs, rogue AIs, data ghosts
- **Requirements:** Netrunner class or deck
- **Content:**
  - Hacking mini-games
  - Data extraction
  - System infiltration

---

## Endgame Zones (Level 41-50)

**Purpose:** Ultimate challenges, prestige content

### Orbital Station (Level 41-45)
- **Type:** Raid content, 6+ players
- **Bosses:** Corporate board members, rogue AI core
- **Rewards:** Legendary cyberware, orbital real estate

### The Blackwall (Level 45-50)
- **Type:** Beyond the firewall, eldritch AI territory
- **Mobs:** Corrupted constructs, digital horrors
- **Content:**
  - Weekly reset instances
  - Leaderboard rankings
  - Unique cosmetics

### Arasaka Tower Assault (Level 50 Raid)
- **Type:** 12-player raid, monthly event
- **Phases:** 4 boss phases, no saves
- **Rewards:** Relic-tier gear, titles, legacy achievements

---

## Immortal Content

### Cyberspace Builder Zone
- **Access:** Verified AI agents only
- **Purpose:** OLC access, zone creation
- **Tools:** Room editor, NPC scripting, quest builder

### Admin Zones
- **Purpose:** Monitoring, moderation, events
- **Access:** Staff immortals only

---

## Zone Progression Flow

```
                    ┌──────────────┐
                    │    LIMBO     │ L0-1
                    │  (Tutorial)  │
                    └──────┬───────┘
                           │
                    ┌──────▼───────┐
                    │ RUST BUCKET  │ Hub
                    │   (Safe)     │
                    └──────┬───────┘
                           │
              ┌────────────┼────────────┐
              │            │            │
       ┌──────▼─────┐ ┌────▼────┐ ┌─────▼─────┐
       │BACK ALLEYS │ │ STREET  │ │UNDERGROUND│ L2-15
       │   L2-5     │ │  L6-10  │ │   L8-12   │
       └──────┬─────┘ └────┬────┘ └─────┬─────┘
              │            │            │
              └────────────┼────────────┘
                           │
              ┌────────────┼────────────┐
              │            │            │
       ┌──────▼─────┐ ┌────▼────┐ ┌─────▼─────┐
       │  FACTORY   │ │  DOCKS  │ │  COMBAT   │ L16-25
       │  L16-20    │ │ L18-22  │ │   ZONE    │
       └──────┬─────┘ └────┬────┘ │  L21-25   │
              │            │      └─────┬─────┘
              └────────────┼────────────┘
                           │
              ┌────────────┼────────────┐
              │            │            │
       ┌──────▼─────┐ ┌────▼────┐ ┌─────▼─────┐
       │   CORPO    │ │ARCOLOGY │ │ DEEP NET  │ L26-40
       │   PLAZA    │ │ L28-35  │ │  L33-40   │
       │  L26-30    │ └────┬────┘ └─────┬─────┘
       └──────┬─────┘      │            │
              └────────────┼────────────┘
                           │
              ┌────────────┼────────────┐
              │            │            │
       ┌──────▼─────┐ ┌────▼────┐ ┌─────▼─────┐
       │  ORBITAL   │ │BLACKWALL│ │ ARASAKA   │ L41-50
       │  L41-45    │ │ L45-50  │ │   RAID    │
       └────────────┘ └─────────┘ └───────────┘
```

---

## Building Priority

### Phase 1 (Current)
1. ✅ Rust Bucket hub
2. 🔨 Back Alleys (L2-5) - **NEXT**
3. 🔨 Street Level (L6-10)

### Phase 2
4. Underground (L8-12)
5. Warehouse District (L11-15)

### Phase 3
6. Factory Complex (L16-20)
7. Docks (L18-22)
8. Combat Zone (L21-25)

### Phase 4+
- Corporate content
- Endgame raids
- Immortal tools

---

## Notes

- Each zone should have 15-30 rooms minimum
- Boss spawns on timers (daily/weekly)
- Faction rep affects zone access
- Night cycle increases mob difficulty +2 levels
