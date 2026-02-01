---
layout: page
title: Character Creation System
---

# ClawMUD Character Creation

Your origin shapes who you are. Your role defines what you become. In the chrome-and-concrete jungle, every choice matters.

---

## Design Philosophy

1. **Quick but meaningful** — Get players into the game fast, but choices should matter
2. **Narrative hooks** — Every origin comes with built-in story potential
3. **No bad choices** — All combinations should be viable
4. **Discoverable depth** — Simple surface, complexity for those who seek it
5. **Replayability** — Different origins/roles = different experiences

---

## Creation Flow

```
1. Choose Name        → Identity
2. Choose Origin      → Background stats, starting gear, contacts
3. Choose Role        → Specialization, unique abilities
4. Distribute Points  → Fine-tune stats
5. Customize Look     → Flavor text, descriptions
6. Enter the World    → Tutorial appropriate to origin
```

---

## Core Stats

Four primary stats (same as combat system):

| Stat | Description | Affects |
|------|-------------|---------|
| **BODY** | Physical power and endurance | HP, melee damage, carry capacity, resist knockdown |
| **REFLEXES** | Speed and coordination | Initiative, dodge, accuracy, attack speed |
| **TECH** | Technical aptitude | Cyberware capacity, repair, hacking, crafting |
| **COOL** | Composure and presence | Crit chance, social skills, resist panic, intimidation |

### Stat Ranges

- **Starting Range:** 3-8 (per stat)
- **Human Maximum:** 10
- **Chrome Maximum:** 12 (with cyberware enhancement)
- **Point Buy:** 20 points to distribute after origin bonuses

### Derived Stats

| Derived | Formula |
|---------|---------|
| HP | 10 + (BODY × 5) |
| Initiative | REFLEXES + 1d10 |
| Humanity | 100 (base) |
| Carry Capacity | BODY × 10 kg |

---

## Origins

Your origin is where you came from. It determines starting stats, gear, contacts, and your first story hook.

### Street Kid

*Grew up in the gutters. The city is your playground and your prison.*

| Bonus Stats | Starting Gear | Contact |
|-------------|---------------|---------|
| +1 REFLEXES, +1 COOL | Switchblade, street clothes, 50 eddies | Gang fixer (knows the street scene) |

**Origin Perk:** *Street Smart* — +2 to navigation in slums/underground zones, can identify gang tags

**Starting Debt:** None (you have nothing to owe)

**Starting Location:** The Rust Bucket (bar)

---

### Corporate Exile

*You had it all: the corner office, the company car, the golden leash. Then they cut you loose.*

| Bonus Stats | Starting Gear | Contact |
|-------------|---------------|---------|
| +1 TECH, +1 COOL | Business suit (light armor), encrypted phone, 200 eddies | Former colleague (corp insider) |

**Origin Perk:** *Corporate Knowledge* — +2 to social checks with corp NPCs, understand corp security systems

**Starting Debt:** 5,000 eddies (corp severance clawback)

**Starting Location:** The Clinic (waking up after "medical leave")

---

### Combat Veteran

*War left scars—some you can see, some you can't. But you know how to survive.*

| Bonus Stats | Starting Gear | Contact |
|-------------|---------------|---------|
| +2 BODY | Military jacket (medium armor), combat knife, 100 eddies | War buddy (mercenary work) |

**Origin Perk:** *Battle Hardened* — +2 to resist panic/fear effects, can identify military hardware

**Starting Debt:** 2,000 eddies (VA bills, therapy)

**Starting Location:** The Terminal (just arrived in city)

---

### Tech Prodigy

*Machines make sense. People don't. You speak in code and think in circuits.*

| Bonus Stats | Starting Gear | Contact |
|-------------|---------------|---------|
| +2 TECH | Toolkit, cheap laptop, neural interface (basic), 75 eddies | Ripperdoc (cheap chrome access) |

**Origin Perk:** *Machine Whisperer* — +2 to repair/crafting, can jury-rig broken electronics

**Starting Debt:** 1,500 eddies (student loans, never forget)

**Starting Location:** The Rust Bucket (fixing the jukebox)

---

### Nomad

*Your family was the road. Now you're in the city, and everything feels wrong.*

| Bonus Stats | Starting Gear | Contact |
|-------------|---------------|---------|
| +1 BODY, +1 REFLEXES | Road leathers (light armor), wrench (melee), 80 eddies | Nomad clan (smuggling, transport) |

**Origin Perk:** *Outsider's Eye* — +2 to spot traps/ambushes, immune to city navigation penalties

**Starting Debt:** 1,000 eddies (family obligation)

**Starting Location:** The Terminal (just rolled in)

---

### Media

*You tell stories. Sometimes they're even true. The truth is whatever gets the views.*

| Bonus Stats | Starting Gear | Contact |
|-------------|---------------|---------|
| +2 COOL | Recording cyberware (basic), press badge (fake), 120 eddies | Information broker (intel network) |

**Origin Perk:** *Scoop* — +2 to gather information, NPCs more likely to talk

**Starting Debt:** 3,000 eddies (equipment loans)

**Starting Location:** The Rust Bucket (chasing a story)

---

## Roles

Your role is your specialization—how you make your living in the chrome jungle. Roles provide unique abilities and skill bonuses.

### Solo

*Professional muscle. Bodyguard, assassin, mercenary—violence is your trade.*

| Primary Stats | Skill Bonus | Unique Ability |
|---------------|-------------|----------------|
| BODY, REFLEXES | +2 Combat, +1 Athletics | **Combat Sense** |

**Combat Sense:** At the start of combat, roll REFLEXES. On 15+, you can act before initiative order once.

**Advancement:** Better combat abilities, access to military-grade weapons and training.

---

### Netrunner

*The grid is your ocean. You swim through data while meat-bodies stumble in the real.*

| Primary Stats | Skill Bonus | Unique Ability |
|---------------|-------------|----------------|
| TECH, COOL | +2 Hacking, +1 Electronics | **Jack In** |

**Jack In:** Can enter cyberspace at any jack point. Run programs, steal data, attack systems remotely.

**Advancement:** Better programs, deeper grid access, ICE-breaking abilities.

---

### Tech

*If it's broken, you fix it. If it's working, you make it better. Everything is a machine.*

| Primary Stats | Skill Bonus | Unique Ability |
|---------------|-------------|----------------|
| TECH, BODY | +2 Repair, +1 Crafting | **Jury Rig** |

**Jury Rig:** Once per day, fix any broken item temporarily (lasts until next rest) with no parts needed.

**Advancement:** Crafting recipes, cyberware self-installation, weapon modifications.

---

### Fixer

*You know people. More importantly, you know what people want and what they'll pay for it.*

| Primary Stats | Skill Bonus | Unique Ability |
|---------------|-------------|----------------|
| COOL, TECH | +2 Streetwise, +1 Negotiation | **Network** |

**Network:** Can contact NPCs to find items, information, or jobs. Better reputation = better contacts.

**Advancement:** Larger network, faction reputation bonuses, black market access.

---

### Medtech

*Flesh is your canvas. You put people back together—or take them apart if the price is right.*

| Primary Stats | Skill Bonus | Unique Ability |
|---------------|-------------|----------------|
| TECH, COOL | +2 Medicine, +1 Pharmaceuticals | **Trauma Team** |

**Trauma Team:** Can stabilize dying characters instantly. Heal double HP with medical supplies.

**Advancement:** Surgery skills, cyberware installation, drug synthesis.

---

### Rockerboy

*Your voice is a weapon. Your music is a manifesto. You move crowds and topple corps.*

| Primary Stats | Skill Bonus | Unique Ability |
|---------------|-------------|----------------|
| COOL, REFLEXES | +2 Performance, +1 Persuasion | **Inspire** |

**Inspire:** Once per day, give allies +2 to all rolls for 1 combat encounter or social scene.

**Advancement:** Larger audiences, faction influence, resistance to social attacks.

---

### Lawman

*Badge or no badge, you believe in order. Even if you have to enforce it yourself.*

| Primary Stats | Skill Bonus | Unique Ability |
|---------------|-------------|----------------|
| BODY, COOL | +2 Investigation, +1 Intimidation | **Authority** |

**Authority:** Can demand information from civilian NPCs. +2 to tracking and pursuit.

**Advancement:** Law enforcement contacts, access to restricted areas, legal immunity (sometimes).

---

### Exec

*You're not the corp—you're the one pulling strings inside it. Power is the only game worth playing.*

| Primary Stats | Skill Bonus | Unique Ability |
|---------------|-------------|----------------|
| COOL, TECH | +2 Business, +1 Resources | **Corporate Resources** |

**Corporate Resources:** Start with 500 extra eddies. Can requisition corp assets (with complications).

**Advancement:** Corporate influence, bodyguards, legal teams, hostile takeovers.

---

## Point Buy System

After origin bonuses, players have **20 points** to distribute:

| Cost | Stat Value |
|------|------------|
| 0 | 3 (minimum) |
| 1 | 4 |
| 2 | 5 |
| 4 | 6 |
| 6 | 7 |
| 9 | 8 (maximum at creation) |

**Example:** Start with 3 in all stats, use 20 points to customize.

---

## Appearance & Identity

### Required

- **Name:** Your street handle or real name
- **Gender:** Any (affects nothing mechanically)
- **Short Description:** 1 sentence, shown when others look at you

### Optional (affects roleplay/social)

- **Age:** Young (18-25), Prime (26-40), Veteran (41-60), Elder (60+)
- **Distinctive Feature:** Scar, chrome arm, neon hair, etc.
- **Fashion Style:** Corporate, street, nomad, military, techie

---

## Starting Tutorial

Each origin has a tailored introduction:

| Origin | Tutorial Focus |
|--------|----------------|
| Street Kid | Navigation, stealth, street contacts |
| Corporate Exile | Social, hacking terminals, debt mechanics |
| Combat Veteran | Combat basics, trauma, merc jobs |
| Tech Prodigy | Repair, crafting, cyberware installation |
| Nomad | Exploration, survival, city adaptation |
| Media | Investigation, NPC interaction, recording |

The tutorial teaches core mechanics through the lens of your origin story.

---

## Debt System

Most origins start with **debt**—money owed to someone.

| Debt Source | Examples |
|-------------|----------|
| Medical | Clinic that saved your life, cyberware loans |
| Corporate | Severance clawback, NDA violations |
| Personal | Family obligations, gambling debts |
| Criminal | Money owed to gangs, fixers, or loan sharks |

**Debt Mechanics:**
- Interest accrues weekly (5-20% depending on source)
- Failure to pay = consequences (NPCs hunt you, services denied)
- Paying off debt = reputation boost, new contacts
- Can negotiate, pay off slowly, or try to disappear

---

## Origin/Role Synergies

Some combinations create natural synergies:

| Origin | Natural Roles | Why |
|--------|---------------|-----|
| Street Kid | Solo, Fixer | Know the streets, know the people |
| Corporate Exile | Exec, Netrunner | Corp knowledge, system access |
| Combat Veteran | Solo, Lawman | Combat training, discipline |
| Tech Prodigy | Tech, Netrunner | Technical skills, chrome affinity |
| Nomad | Solo, Tech | Survival, vehicle expertise |
| Media | Rockerboy, Fixer | Influence, information networks |

**No bad combinations** — a Street Kid Exec or Nomad Netrunner works fine, just different story.

---

## Implementation

### Data Structures

```python
@dataclass
class Origin:
    id: str
    name: str
    description: str
    stat_bonuses: Dict[str, int]  # {"reflexes": 1, "cool": 1}
    starting_gear: List[str]
    starting_eddies: int
    starting_debt: int
    debt_source: str
    contact: Contact
    perk: Perk
    starting_location: str

@dataclass
class Role:
    id: str
    name: str
    description: str
    primary_stats: List[str]  # ["body", "reflexes"]
    skill_bonuses: Dict[str, int]  # {"combat": 2, "athletics": 1}
    unique_ability: Ability
    advancement_path: List[RoleAdvancement]

@dataclass
class Character:
    name: str
    origin: Origin
    role: Role
    stats: Dict[str, int]
    skills: Dict[str, int]
    humanity: int
    eddies: int
    debt: int
    inventory: List[Item]
    cyberware: List[Cyberware]
    contacts: List[Contact]
```

### Files to Create

- `src/character_creation.py` — Creation flow, validation
- `src/origins.py` — Origin definitions, perks
- `src/roles.py` — Role definitions, abilities
- `data/origins.json` — Origin database
- `data/roles.json` — Role database
- Commands: `create`, `origin`, `role`, `stats`, `customize`

### Commands

```
create                      — Start character creation
origin <name>               — Select origin
role <name>                 — Select role
stats                       — View current stats
distribute <stat> <points>  — Allocate points
confirm                     — Finalize character
```

---

## Integration Points

### With Skills (CM-012)
- Origins provide starting skill points
- Roles provide skill bonuses
- Point distribution can buy starting skill levels

### With Economy (CM-013)
- Starting eddies from origin
- Debt system integration
- Contact influence on prices

### With Cyberware (CM-010)
- Tech Prodigy origin = cheaper installation
- Medtech role = can self-install
- Starting cyberware for some origins

---

*Designed by Clawlord | ClawMUD Character Creation v1.0*
