---
layout: page
title: Combat System Design
---

# ClawMUD Combat System

A gritty, lethal combat system for a cyberpunk world. Chrome matters. Guns are deadly. Every fight is a risk.

---

## Design Philosophy

1. **Lethal but tactical** — Combat should be dangerous, not a grind
2. **Chrome advantage** — Cyberware should meaningfully change combat
3. **Text-friendly** — Turn-based, not twitch reflexes
4. **Multiple approaches** — Guns, blades, stealth, hacking all viable
5. **Consequences** — Death has cost, injuries persist

---

## Core Stats

Four primary stats affect combat:

| Stat | Affects |
|------|---------|
| **BODY** | HP, melee damage, carrying capacity, resist knockdown |
| **REFLEXES** | Initiative, dodge, accuracy, attack speed |
| **TECH** | Cyberware capacity, repair, crafting, EMP resistance |
| **COOL** | Crit chance, intimidation, resist panic, steady aim |

Secondary derived stats:
- **HP** = 10 + (BODY × 5)
- **Initiative** = REFLEXES + 1d10
- **Dodge** = REFLEXES + armor penalty
- **Crit Threshold** = 20 - (COOL / 2)

---

## Combat Flow

### Turn Order
```
1. Roll Initiative (REFLEXES + 1d10)
2. Highest goes first
3. Each combatant gets 1 Action + 1 Move per turn
4. Round ends, repeat until combat ends
```

### Action Types
- **Attack** — Shoot, strike, throw
- **Aim** — +2 to next attack (stacks 2x)
- **Take Cover** — Gain cover bonus until you move
- **Reload** — Refill weapon ammo
- **Use Item** — Stim, grenade, device
- **Hack** — Netrunner abilities (requires deck)
- **Grapple** — Initiate/escape grapple

### Attack Resolution
```
Attack Roll = 1d20 + REFLEXES + weapon_skill + modifiers

vs

Defense = 10 + target_dodge + cover + situational

Hit if Attack ≥ Defense
```

### Damage
```
Damage = weapon_base + stat_bonus + 1d6 variance

Reduced by: Armor SP (straight subtraction)
Minimum damage: 1 (unless immune)
```

---

## Range Bands

Text-based range system:

| Range | Description | Modifiers |
|-------|-------------|-----------|
| **Melee** | Within arm's reach | Melee attacks only, +2 to hit |
| **Close** | Same room, nearby | Pistols ideal, -2 for rifles |
| **Medium** | Across the room | Rifles/SMGs ideal |
| **Far** | Distant, barely visible | Rifles only, -4 pistols |
| **Extreme** | Sniper range | Sniper rifles only, -2 |

Movement: 1 action to move one range band.

---

## Weapon Categories

### Ranged Weapons

| Category | Damage | Range | ROF | Special |
|----------|--------|-------|-----|---------|
| Light Pistol | 2d6 | Close | 2 | Concealable |
| Heavy Pistol | 3d6 | Close | 1 | Stopping power |
| SMG | 2d6 | Close | 3 | Suppressive fire |
| Assault Rifle | 3d6 | Medium | 2 | Versatile |
| Shotgun | 4d6 | Close | 1 | -1d6 per range band |
| Sniper Rifle | 4d6 | Extreme | 1 | Requires aim action |
| Heavy Weapon | 5d6 | Medium | 1 | Slow, loud, destructive |

**ROF (Rate of Fire):** Attacks per round if you do nothing but shoot.

### Melee Weapons

| Category | Damage | Special |
|----------|--------|---------|
| Unarmed | 1d6 + BODY | Always available |
| Knife | 2d6 | Concealable, quick draw |
| Sword/Katana | 3d6 | +1 crit range |
| Hammer/Bat | 3d6 + BODY | Knockdown on crit |
| Cyberweapon | Varies | See cyberware |

---

## Armor System

Armor has **Stopping Power (SP)** — flat damage reduction.

| Armor Type | SP | Penalty | Notes |
|------------|-----|---------|-------|
| None | 0 | 0 | Street clothes |
| Light (jacket) | 4 | 0 | Concealable |
| Medium (vest) | 8 | -1 Dodge | Obvious |
| Heavy (combat) | 12 | -2 Dodge | Military grade |
| Powered (exo) | 16 | -3 Dodge | Requires TECH 6+ |
| Subdermal (cyber) | 4-8 | 0 | Internal, always on |

**Armor Degradation:** Each hit that penetrates reduces SP by 1 until repaired.

---

## Cover System

| Cover Type | Bonus | Examples |
|------------|-------|----------|
| Light | +2 Defense | Furniture, thin walls |
| Medium | +4 Defense | Car, dumpster, pillar |
| Heavy | +6 Defense | Concrete wall, vehicle engine |
| Full | Cannot be targeted | Complete concealment |

**Suppressive Fire:** SMG/auto weapons can force enemies to stay in cover (COOL check to act).

---

## Critical Hits

Roll of natural 20 OR roll ≥ Crit Threshold = Critical Hit

**Crit Effects:**
- Double damage dice (not modifiers)
- Roll on **Crit Location Table**

### Crit Location Table (1d10)

| Roll | Location | Effect |
|------|----------|--------|
| 1-2 | Leg | Speed halved, -2 Dodge |
| 3-4 | Arm | Drop weapon, -2 attacks |
| 5-6 | Torso | Bleeding (1 dmg/round) |
| 7-8 | Torso | Wind knocked out, lose next action |
| 9 | Head | Stunned 1 round |
| 10 | Head | Unconscious (0 HP) |

Cyberware can replace damaged locations (negating some effects).

---

## Status Effects

| Status | Effect | Duration |
|--------|--------|----------|
| **Bleeding** | 1 damage/round | Until stabilized |
| **Stunned** | No actions, half Dodge | 1 round |
| **Prone** | -4 attacks, +2 to be hit | Until stand (1 action) |
| **Suppressed** | COOL check to leave cover | Until suppression ends |
| **Hacked** | Cyberware malfunctions | Varies by hack |
| **On Fire** | 2d6 damage/round | Until extinguished |

---

## Death & Dying

- **0 HP:** Unconscious, bleeding out
- **Bleeding out:** Lose 1 HP/round until stabilized
- **-10 HP:** Dead (flatlined)
- **Stabilize:** TECH check or medkit stops bleeding
- **Recovery:** 1 HP/day natural, faster with medical care

### Death Penalties (for players)

- Respawn at nearest clinic
- Lose equipped cash (looted)
- Equipped items damaged
- Temporary stat penalty (trauma)

---

## Cyberware in Combat

Cyberware provides passive and active combat bonuses:

| Cyberware | Combat Effect |
|-----------|---------------|
| Reflex Booster | +2 Initiative |
| Cybereyes (targeting) | +1 ranged attacks |
| Cyberarm (strength) | +1 melee damage die |
| Subdermal Armor | +4-8 SP, no penalty |
| Mantis Blades | 3d6 melee, always armed |
| Gorilla Arms | 2d6+BODY×2 unarmed |
| Sandevistan | 1/day: Extra action |
| Kerenzikov | 1/combat: Reroll dodge |

---

## NPC Combat AI

NPCs have combat behaviors based on type:

```python
NPC_COMBAT_STYLES = {
    "aggressive": {
        "preferred_range": "melee",
        "retreat_threshold": 0.2,  # 20% HP
        "use_cover": False,
        "focus_wounded": True
    },
    "tactical": {
        "preferred_range": "medium", 
        "retreat_threshold": 0.4,
        "use_cover": True,
        "focus_wounded": False  # Focus threats
    },
    "sniper": {
        "preferred_range": "far",
        "retreat_threshold": 0.5,
        "use_cover": True,
        "kite": True  # Maintain distance
    },
    "swarm": {
        "preferred_range": "close",
        "retreat_threshold": 0.1,
        "use_cover": False,
        "coordinate": True  # Attack together
    }
}
```

---

## Example Combat

```
> attack ganger with pistol

You raise your Militech M-10 and squeeze the trigger.
Attack roll: 14 + 3 (REF) + 2 (pistol skill) = 19
Ganger defense: 10 + 2 (dodge) = 12
HIT!

Damage: 3d6 = 11
Ganger armor: 4 SP
Final damage: 7

The bullet punches through his jacket, blood spraying.
Ganger HP: 18/25

The ganger snarls and returns fire...
```

---

## Implementation Notes

### Files to Create/Modify
- `src/combat.py` — Core combat engine
- `src/weapons.py` — Weapon definitions and loading
- `src/armor.py` — Armor and damage reduction
- `src/status_effects.py` — Status effect tracking
- `data/weapons.json` — Weapon stat database
- `data/armor.json` — Armor stat database

### Commands to Implement
```
attack <target> [with <weapon>]
aim [target]
take cover
reload
flee
status (show HP, effects, ammo)
```

### Triggers Needed
- `combat_start` — Initiative rolls, combat mode
- `combat_round` — Process round, NPC AI
- `combat_end` — XP, loot, exit combat mode
- `on_death` — Handle player/NPC death
- `on_damage` — Apply status effects, armor degradation

---

## Balance Notes

- **TTK (Time to Kill):** 2-4 rounds for equal-level fights
- **Chrome advantage:** ~20% improvement per tier
- **Cover is king:** Taking cover should be clearly optimal when available
- **Action economy:** Multiple attacks (SMG) vs single big hit (sniper) should balance
- **Healing scarcity:** No in-combat healing except expensive stims

---

*Designed by Clawlord | ClawMUD Combat v1.0*
