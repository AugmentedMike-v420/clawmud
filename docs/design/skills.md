---
layout: page
title: Skills System Design
---

# ClawMUD Skills System

Stats tell you what you're capable of. Skills tell you what you've learned. In Night City, talent keeps you alive—but skill keeps you breathing.

---

## Design Philosophy

1. **Cyberpunk, not fantasy** — No "sword mastery" or "arcane knowledge"—this is tech, guns, and street smarts
2. **Broad categories** — Skills are general; specialization comes from practice
3. **Use it or lose it** — Skills improve through use, not just XP dumps
4. **Synergy with chrome** — Cyberware can enhance but not replace skill
5. **Social skills matter** — Combat isn't the only way to solve problems

---

## Skill Mechanics

### Skill Checks

```
Roll = 1d20 + Stat Modifier + Skill Level + Modifiers
vs
Difficulty Class (DC)
```

### Difficulty Classes

| DC | Difficulty | Example |
|----|------------|---------|
| 5 | Trivial | Walking, basic conversation |
| 10 | Easy | Climbing a ladder, spotting obvious clue |
| 15 | Moderate | Picking a basic lock, hacking unguarded terminal |
| 20 | Hard | Picking corp lock, persuading hostile NPC |
| 25 | Very Hard | Cracking military encryption, brain surgery |
| 30 | Legendary | Hacking Arasaka mainframe, the impossible |

### Skill Levels

| Level | Description | Bonus |
|-------|-------------|-------|
| 0 | Untrained | -2 (or can't attempt) |
| 1 | Novice | +1 |
| 2 | Competent | +2 |
| 3 | Professional | +4 |
| 4 | Expert | +6 |
| 5 | Master | +8 |
| 6 | Legendary | +10 (max) |

---

## Skill Categories

Skills are organized into categories tied to primary stats.

### BODY Skills

Physical power and endurance.

| Skill | Description | Example Uses |
|-------|-------------|--------------|
| **Athletics** | Running, jumping, climbing, swimming | Chase scenes, parkour, escapes |
| **Endurance** | Stamina, resist fatigue, forced march | Staying awake, poison resistance |
| **Melee Combat** | Hand-to-hand, blades, blunt weapons | Knife fights, bar brawls |
| **Strength Feat** | Lifting, breaking, bending | Forcing doors, intimidation displays |

### REFLEXES Skills

Speed, coordination, and physical finesse.

| Skill | Description | Example Uses |
|-------|-------------|--------------|
| **Firearms** | Pistols, SMGs, rifles, shotguns | Gunfights, sniping |
| **Evasion** | Dodging, avoiding attacks | Combat defense, avoiding traps |
| **Driving** | Ground vehicles, motorcycles | Chases, getaways, stunts |
| **Stealth** | Moving silently, hiding | Infiltration, ambushes |
| **Pickpocket** | Lifting items, planting evidence | Theft, sleight of hand |

### TECH Skills

Technical knowledge and application.

| Skill | Description | Example Uses |
|-------|-------------|--------------|
| **Hacking** | Breaking into systems, running programs | Netrunning, data theft |
| **Electronics** | Understanding, repairing, modifying devices | Bypassing security, surveillance |
| **Repair** | Fixing vehicles, weapons, cyberware | Maintenance, salvage |
| **Demolitions** | Explosives, structural weaknesses | Breaching, traps |
| **Medicine** | First aid, surgery, trauma care | Healing, stabilization |
| **Pharmaceuticals** | Drugs, poisons, stimulants | Synthesis, identification |
| **Cybertechnology** | Cyberware installation, modification | Ripperdoc work, chrome upgrades |

### COOL Skills

Social acumen and mental fortitude.

| Skill | Description | Example Uses |
|-------|-------------|--------------|
| **Persuasion** | Convincing, negotiating, charming | Getting deals, avoiding fights |
| **Intimidation** | Threatening, coercing, dominating | Extracting info, scaring enemies |
| **Deception** | Lying, bluffing, disguise | Undercover work, cons |
| **Streetwise** | Street knowledge, gang lore, survival | Finding black market, reading turf |
| **Perception** | Noticing details, spotting lies | Investigation, ambush detection |
| **Willpower** | Mental resistance, focus, composure | Resist torture, cyberpsycho checks |
| **Performance** | Music, acting, public speaking | Rockerboy abilities, distraction |

---

## Skill Advancement

### Experience Through Use

Skills improve by **using them successfully** in meaningful situations.

```
On successful skill check in a challenging situation:
  Roll 1d20
  If roll > current skill level × 3:
    Gain 1 skill point toward next level
```

**Skill points needed per level:**

| Target Level | Points Needed |
|--------------|---------------|
| 1 (Novice) | 5 |
| 2 (Competent) | 10 |
| 3 (Professional) | 20 |
| 4 (Expert) | 40 |
| 5 (Master) | 80 |
| 6 (Legendary) | 160 |

### Training

Can also improve skills through **training**:

- **Self-study:** 1 skill point per day of practice (max to level 2)
- **Trainer NPC:** 2-5 skill points per session (costs eddies)
- **Chip (skillsoft):** Instant skill level (limited by cyberware)

### Skill Decay (Optional)

Skills unused for extended periods may decay:
- No decay below level 2
- 30 days without use = check for decay
- Roll TECH; failure = lose 1 skill point

---

## Specialized Skills

Some skills have **specializations** that provide additional bonuses in narrow areas.

### Firearms Specializations

| Specialization | Bonus | Requirement |
|----------------|-------|-------------|
| Pistols | +1 with handguns | Firearms 2 |
| Long Arms | +1 with rifles/shotguns | Firearms 2 |
| Automatic Weapons | +1 with SMGs/assault | Firearms 3 |
| Sniping | +1 with scoped rifles | Firearms 3 |

### Hacking Specializations

| Specialization | Bonus | Requirement |
|----------------|-------|-------------|
| ICE Breaking | +1 vs security programs | Hacking 2 |
| Data Mining | +1 to find specific data | Hacking 2 |
| System Control | +1 to control systems | Hacking 3 |
| Combat Hacking | +1 to offensive programs | Hacking 3 |

### Medicine Specializations

| Specialization | Bonus | Requirement |
|----------------|-------|-------------|
| Trauma Care | +1 to stabilization | Medicine 2 |
| Surgery | +1 to operations | Medicine 3 |
| Cybersurgery | +1 to cyberware installation | Medicine 3, Cybertechnology 2 |

---

## Skill Synergies

Using related skills together provides bonuses:

| Primary Skill | Supporting Skill | Synergy Bonus |
|---------------|------------------|---------------|
| Hacking | Electronics | +1 if both ≥ 2 |
| Stealth | Perception | +1 if both ≥ 2 |
| Intimidation | Melee Combat | +1 if both ≥ 2 |
| Medicine | Pharmaceuticals | +1 if both ≥ 2 |
| Driving | Repair | +1 if both ≥ 2 |

---

## Skillsofts & Chips

Cyberware can provide **instant skill access** via skillsoft chips.

### Skillsoft Types

| Type | Effect | Limitation |
|------|--------|------------|
| **Knowledge Chip** | +2 to specific knowledge checks | Passive only |
| **Skillsoft** | Provides skill at level 2 | Requires neural interface |
| **Combat Chip** | +1 to specific weapon type | Requires reflex booster |
| **Social Chip** | +1 to specific social skill | Requires behavioral processor |

### Chip Stacking

- Cannot stack chips of same skill
- Natural skill always takes precedence if higher
- Max 3 active skillsofts at once (neural limit)

### Chip Quality

| Quality | Skill Level | Price Mult |
|---------|-------------|------------|
| Street | 1 | ×0.5 |
| Standard | 2 | ×1 |
| Corp | 3 | ×5 |
| Milspec | 4 | ×20 |

---

## Role Skill Bonuses

Each role (from character creation) provides skill bonuses:

| Role | Primary Skill (+2) | Secondary Skill (+1) |
|------|-------------------|---------------------|
| Solo | Firearms OR Melee | Athletics |
| Netrunner | Hacking | Electronics |
| Tech | Repair | Cybertechnology |
| Fixer | Streetwise | Persuasion |
| Medtech | Medicine | Pharmaceuticals |
| Rockerboy | Performance | Persuasion |
| Lawman | Perception | Intimidation |
| Exec | Persuasion | Streetwise |

---

## Untrained Skill Use

Some skills can be attempted untrained (at -2), others cannot:

### Can Attempt Untrained

- Athletics, Endurance, Strength Feat
- Melee Combat, Firearms (basic)
- Driving (basic vehicles)
- Stealth, Perception
- Persuasion, Intimidation, Deception
- Streetwise

### Cannot Attempt Untrained

- Hacking (requires knowledge + tools)
- Electronics (requires knowledge)
- Demolitions (too dangerous)
- Medicine (beyond first aid)
- Pharmaceuticals
- Cybertechnology
- Specialized combat (sniping, etc.)

---

## Example Skill Checks

### Combat Examples

```
> You fire your pistol at the ganger

Roll: 1d20 + REFLEXES (4) + Firearms (3) + pistol mod (0)
You rolled: 14 + 4 + 3 = 21
Ganger Defense: 14
HIT! Roll damage...
```

### Social Examples

```
> You try to convince the bouncer to let you in

Roll: 1d20 + COOL (3) + Persuasion (2)
DC: 15 (he's not impressed by your outfit)
You rolled: 11 + 3 + 2 = 16
SUCCESS! He steps aside grudgingly.
```

### Technical Examples

```
> You attempt to hack the security terminal

Roll: 1d20 + TECH (5) + Hacking (4) + Coprocessor (+1)
DC: 20 (corp security)
You rolled: 8 + 5 + 4 + 1 = 18
FAILURE. ICE detects your intrusion. Alarm in 3 rounds.
```

---

## Opposed Skill Checks

When two characters compete:

```
Attacker Roll vs Defender Roll
Higher wins (defender wins ties)
```

### Common Opposed Checks

| Attacker | Defender |
|----------|----------|
| Stealth | Perception |
| Deception | Perception |
| Persuasion | Willpower |
| Intimidation | Willpower |
| Pickpocket | Perception |
| Hacking | Hacking (if defended) |

---

## Implementation

### Data Structures

```python
@dataclass
class Skill:
    id: str
    name: str
    category: str  # body, reflexes, tech, cool
    linked_stat: str
    can_use_untrained: bool
    description: str
    specializations: List[str]

@dataclass
class CharacterSkill:
    skill_id: str
    level: int  # 0-6
    experience: int  # points toward next level
    specializations: List[str]  # unlocked specs
    source: str  # natural, chip, training

@dataclass
class SkillCheck:
    skill: Skill
    character: Character
    dc: int
    modifiers: List[Modifier]
    
    def roll(self) -> SkillCheckResult:
        base = roll_d20()
        stat_mod = character.get_stat(skill.linked_stat)
        skill_mod = character.get_skill_level(skill.id)
        total_mods = sum(m.value for m in modifiers)
        total = base + stat_mod + skill_mod + total_mods
        return SkillCheckResult(
            success=total >= dc,
            roll=base,
            total=total,
            margin=total - dc
        )
```

### Files to Create

- `src/skills.py` — Core skill system
- `src/skill_checks.py` — Check resolution
- `src/skill_advancement.py` — XP and leveling
- `data/skills.json` — Skill definitions
- `data/skillsofts.json` — Chip definitions

### Commands

```
skills              — List all skills and levels
check <skill>       — See current bonus/info
train <skill>       — Practice (if available)
specialize <skill>  — Learn specialization
chips               — View installed skillsofts
```

---

## Integration Points

### Combat (CM-009)
- Firearms, Melee Combat used for attack rolls
- Evasion used for dodge
- Athletics for movement/positioning

### Cyberware (CM-010)
- Cybertechnology for installation
- Medicine for surgery
- Skillsofts provide virtual skill levels

### Character Creation (CM-011)
- Starting skill points from origin
- Role skill bonuses
- Point buy for initial skills

### Economy (CM-013)
- Training costs eddies
- Skillsofts are purchasable
- Better skill = better paying jobs

---

## Balance Notes

- **Skill cap (6)** prevents runaway scaling
- **Use-based advancement** rewards active play
- **Synergies** encourage breadth, not just depth
- **Untrained penalties** make specialists valuable
- **Chips** provide catch-up but not mastery

---

*Designed by Clawlord | ClawMUD Skills v1.0*
