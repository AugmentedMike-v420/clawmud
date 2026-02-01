"""
ClawMUD Combat System
Core combat engine, turn management, and attack resolution.
"""
import random
from dataclasses import dataclass, field
from enum import Enum
from typing import Optional, Callable

from .weapons import Weapon, RangeBand, RANGE_ORDER, UNARMED
from .armor import Armor, ArmorSet


class CombatAction(Enum):
    """Available combat actions."""
    ATTACK = "attack"
    AIM = "aim"
    TAKE_COVER = "take_cover"
    RELOAD = "reload"
    USE_ITEM = "use_item"
    HACK = "hack"
    GRAPPLE = "grapple"
    MOVE = "move"
    FLEE = "flee"


class CoverType(Enum):
    """Types of cover."""
    NONE = "none"
    LIGHT = "light"      # +2 Defense
    MEDIUM = "medium"    # +4 Defense
    HEAVY = "heavy"      # +6 Defense
    FULL = "full"        # Cannot be targeted


COVER_BONUS = {
    CoverType.NONE: 0,
    CoverType.LIGHT: 2,
    CoverType.MEDIUM: 4,
    CoverType.HEAVY: 6,
    CoverType.FULL: 100  # Effectively untargetable
}


class StatusEffect(Enum):
    """Combat status effects."""
    BLEEDING = "bleeding"
    STUNNED = "stunned"
    PRONE = "prone"
    SUPPRESSED = "suppressed"
    HACKED = "hacked"
    ON_FIRE = "on_fire"


@dataclass
class CritLocation:
    """Critical hit location result."""
    roll: int
    location: str
    effect: str
    stat_penalty: dict = field(default_factory=dict)


# Crit location table (1d10)
CRIT_TABLE = [
    CritLocation(1, "leg", "Speed halved, -2 Dodge", {"dodge": -2, "speed_halved": True}),
    CritLocation(2, "leg", "Speed halved, -2 Dodge", {"dodge": -2, "speed_halved": True}),
    CritLocation(3, "arm", "Drop weapon, -2 attacks", {"attack": -2, "drop_weapon": True}),
    CritLocation(4, "arm", "Drop weapon, -2 attacks", {"attack": -2, "drop_weapon": True}),
    CritLocation(5, "torso", "Bleeding (1 dmg/round)", {"bleeding": True}),
    CritLocation(6, "torso", "Bleeding (1 dmg/round)", {"bleeding": True}),
    CritLocation(7, "torso", "Wind knocked out, lose next action", {"lose_action": True}),
    CritLocation(8, "torso", "Wind knocked out, lose next action", {"lose_action": True}),
    CritLocation(9, "head", "Stunned 1 round", {"stunned": True}),
    CritLocation(10, "head", "Unconscious (0 HP)", {"unconscious": True}),
]


@dataclass
class CombatStats:
    """Combat-relevant stats for a combatant."""
    body: int = 5
    reflexes: int = 5
    tech: int = 5
    cool: int = 5
    
    # Derived stats (can be overridden)
    _hp: Optional[int] = None
    _max_hp: Optional[int] = None
    
    # Combat modifiers from cyberware/effects
    initiative_bonus: int = 0
    attack_bonus: int = 0
    dodge_bonus: int = 0
    damage_bonus: int = 0
    crit_bonus: int = 0
    
    @property
    def max_hp(self) -> int:
        """Calculate max HP: 10 + (BODY × 5)"""
        if self._max_hp is not None:
            return self._max_hp
        return 10 + (self.body * 5)
    
    @max_hp.setter
    def max_hp(self, value: int):
        self._max_hp = value
    
    @property
    def hp(self) -> int:
        """Current HP."""
        if self._hp is None:
            self._hp = self.max_hp
        return self._hp
    
    @hp.setter
    def hp(self, value: int):
        self._hp = min(value, self.max_hp)
    
    @property
    def crit_threshold(self) -> int:
        """Roll needed to crit: 20 - (COOL / 2)"""
        return 20 - (self.cool // 2)
    
    def roll_initiative(self) -> int:
        """Roll initiative: REFLEXES + 1d10 + bonus"""
        return self.reflexes + random.randint(1, 10) + self.initiative_bonus
    
    def get_dodge(self, armor_penalty: int = 0) -> int:
        """Get dodge value: REFLEXES + bonus - armor penalty"""
        return self.reflexes + self.dodge_bonus - armor_penalty


@dataclass
class Combatant:
    """Represents an entity in combat."""
    id: str
    name: str
    stats: CombatStats
    armor: ArmorSet = field(default_factory=ArmorSet)
    weapon: Weapon = field(default_factory=lambda: UNARMED)
    
    # Combat state
    initiative: int = 0
    range_band: RangeBand = RangeBand.MEDIUM
    cover: CoverType = CoverType.NONE
    aim_bonus: int = 0  # Stacks from aim actions
    status_effects: dict = field(default_factory=dict)  # Effect -> rounds remaining
    
    # Action tracking
    has_acted: bool = False
    has_moved: bool = False
    
    @property
    def is_alive(self) -> bool:
        return self.stats.hp > -10
    
    @property
    def is_conscious(self) -> bool:
        return self.stats.hp > 0
    
    @property
    def is_bleeding_out(self) -> bool:
        return self.stats.hp <= 0 and self.stats.hp > -10
    
    @property
    def defense(self) -> int:
        """Calculate defense: 10 + dodge + cover + situational"""
        base = 10
        dodge = self.stats.get_dodge(self.armor.total_dodge_penalty)
        cover = COVER_BONUS.get(self.cover, 0)
        
        # Status effect modifiers
        modifier = 0
        if StatusEffect.STUNNED in self.status_effects:
            modifier -= dodge // 2  # Half dodge when stunned
        if StatusEffect.PRONE in self.status_effects:
            modifier += 2  # Easier to hit when prone
        
        return base + dodge + cover + modifier
    
    def roll_attack(self, weapon_skill: int = 0) -> tuple[int, int, bool]:
        """
        Roll attack: 1d20 + REFLEXES + skill + modifiers.
        Returns (roll, total, is_nat20).
        """
        roll = random.randint(1, 20)
        modifiers = (
            self.stats.reflexes +
            weapon_skill +
            self.stats.attack_bonus +
            self.aim_bonus +
            self.weapon.get_range_modifier(self.range_band)
        )
        
        # Status penalties
        if StatusEffect.PRONE in self.status_effects:
            modifiers -= 4
        
        return roll, roll + modifiers, roll == 20
    
    def is_crit(self, roll: int, is_nat20: bool) -> bool:
        """Check if attack is a critical hit."""
        threshold = self.stats.crit_threshold - self.weapon.crit_bonus - self.stats.crit_bonus
        return is_nat20 or roll >= threshold
    
    def take_damage(self, damage: int, hit_location: str = "torso") -> tuple[int, list[str]]:
        """
        Take damage after armor reduction.
        Returns (actual_damage, messages).
        """
        actual_damage, armor_messages = self.armor.reduce_damage(damage, hit_location)
        self.stats.hp -= actual_damage
        
        messages = armor_messages.copy()
        
        if self.stats.hp <= 0 and self.stats.hp > -10:
            messages.append(f"{self.name} falls unconscious and is bleeding out!")
            self.status_effects[StatusEffect.BLEEDING] = -1  # Indefinite until stabilized
        elif self.stats.hp <= -10:
            messages.append(f"{self.name} has flatlined!")
        
        return actual_damage, messages
    
    def apply_status(self, effect: StatusEffect, duration: int = 1) -> None:
        """Apply a status effect."""
        self.status_effects[effect] = duration
    
    def remove_status(self, effect: StatusEffect) -> None:
        """Remove a status effect."""
        if effect in self.status_effects:
            del self.status_effects[effect]
    
    def tick_effects(self) -> list[str]:
        """Process status effects at end of round. Returns messages."""
        messages = []
        expired = []
        
        for effect, duration in self.status_effects.items():
            if effect == StatusEffect.BLEEDING:
                self.stats.hp -= 1
                messages.append(f"{self.name} takes 1 bleeding damage!")
                if self.stats.hp <= -10:
                    messages.append(f"{self.name} has bled out!")
            
            elif effect == StatusEffect.ON_FIRE:
                fire_damage = sum(random.randint(1, 6) for _ in range(2))
                self.stats.hp -= fire_damage
                messages.append(f"{self.name} takes {fire_damage} fire damage!")
            
            # Tick down duration
            if duration > 0:
                self.status_effects[effect] = duration - 1
                if duration - 1 <= 0:
                    expired.append(effect)
        
        for effect in expired:
            del self.status_effects[effect]
            messages.append(f"{self.name} is no longer {effect.value}!")
        
        return messages
    
    def start_turn(self) -> None:
        """Reset turn state."""
        self.has_acted = False
        self.has_moved = False
    
    def end_turn(self) -> None:
        """End turn cleanup."""
        # Aim bonus resets if you do anything but aim
        pass  # Handled by action processing


@dataclass
class AttackResult:
    """Result of an attack action."""
    attacker: str
    defender: str
    weapon: str
    hit: bool
    roll: int
    total_attack: int
    defense: int
    is_crit: bool = False
    damage: int = 0
    damage_dealt: int = 0  # After armor
    crit_location: Optional[CritLocation] = None
    messages: list = field(default_factory=list)
    
    def to_narrative(self) -> str:
        """Generate narrative text for the attack."""
        lines = []
        
        if not self.hit:
            lines.append(f"{self.attacker}'s attack with {self.weapon} misses! "
                        f"(Roll: {self.total_attack} vs Defense: {self.defense})")
        else:
            if self.is_crit:
                lines.append(f"CRITICAL HIT! {self.attacker} strikes {self.defender} with {self.weapon}!")
                if self.crit_location:
                    lines.append(f"Hit location: {self.crit_location.location.upper()} - {self.crit_location.effect}")
            else:
                lines.append(f"{self.attacker} hits {self.defender} with {self.weapon}!")
            
            lines.append(f"Damage: {self.damage} → {self.damage_dealt} after armor")
        
        lines.extend(self.messages)
        
        return "\n".join(lines)


class CombatEncounter:
    """Manages a combat encounter between multiple combatants."""
    
    def __init__(self):
        self.combatants: dict[str, Combatant] = {}
        self.turn_order: list[str] = []
        self.current_turn_index: int = 0
        self.round_number: int = 0
        self.is_active: bool = False
        
        # Event callbacks
        self.on_combat_start: Optional[Callable] = None
        self.on_round_start: Optional[Callable] = None
        self.on_round_end: Optional[Callable] = None
        self.on_combat_end: Optional[Callable] = None
        self.on_death: Optional[Callable] = None
        self.on_damage: Optional[Callable] = None
    
    def add_combatant(self, combatant: Combatant) -> None:
        """Add a combatant to the encounter."""
        self.combatants[combatant.id] = combatant
    
    def remove_combatant(self, combatant_id: str) -> Optional[Combatant]:
        """Remove a combatant from the encounter."""
        if combatant_id in self.combatants:
            combatant = self.combatants.pop(combatant_id)
            if combatant_id in self.turn_order:
                self.turn_order.remove(combatant_id)
            return combatant
        return None
    
    def start_combat(self) -> list[str]:
        """Begin combat, roll initiative, set turn order."""
        messages = ["Combat begins!"]
        
        # Roll initiative for all combatants
        initiatives = []
        for cid, combatant in self.combatants.items():
            combatant.initiative = combatant.stats.roll_initiative()
            initiatives.append((cid, combatant.initiative, combatant.name))
            messages.append(f"{combatant.name} rolls initiative: {combatant.initiative}")
        
        # Sort by initiative (highest first)
        initiatives.sort(key=lambda x: x[1], reverse=True)
        self.turn_order = [i[0] for i in initiatives]
        
        self.current_turn_index = 0
        self.round_number = 1
        self.is_active = True
        
        messages.append(f"\nRound {self.round_number} begins!")
        messages.append(f"Turn order: {', '.join(i[2] for i in initiatives)}")
        
        if self.on_combat_start:
            self.on_combat_start(self)
        
        return messages
    
    def get_current_combatant(self) -> Optional[Combatant]:
        """Get the combatant whose turn it is."""
        if not self.turn_order:
            return None
        cid = self.turn_order[self.current_turn_index]
        return self.combatants.get(cid)
    
    def next_turn(self) -> list[str]:
        """Advance to the next turn."""
        messages = []
        
        # End current combatant's turn
        current = self.get_current_combatant()
        if current:
            current.end_turn()
            effect_messages = current.tick_effects()
            messages.extend(effect_messages)
        
        # Move to next combatant
        self.current_turn_index += 1
        
        # Check if round ended
        if self.current_turn_index >= len(self.turn_order):
            self.current_turn_index = 0
            self.round_number += 1
            messages.append(f"\n--- Round {self.round_number} ---")
            
            if self.on_round_end:
                self.on_round_end(self)
            if self.on_round_start:
                self.on_round_start(self)
        
        # Start new combatant's turn
        next_combatant = self.get_current_combatant()
        if next_combatant:
            next_combatant.start_turn()
            
            # Skip unconscious/dead combatants
            if not next_combatant.is_conscious:
                skip_msg = f"{next_combatant.name} is {'dead' if not next_combatant.is_alive else 'unconscious'}!"
                messages.append(skip_msg)
                messages.extend(self.next_turn())
            else:
                messages.append(f"\n{next_combatant.name}'s turn!")
        
        return messages
    
    def resolve_attack(self, attacker_id: str, defender_id: str, 
                       weapon_skill: int = 0) -> AttackResult:
        """Resolve an attack action."""
        attacker = self.combatants.get(attacker_id)
        defender = self.combatants.get(defender_id)
        
        if not attacker or not defender:
            return AttackResult(
                attacker=attacker_id,
                defender=defender_id,
                weapon="unknown",
                hit=False,
                roll=0,
                total_attack=0,
                defense=0,
                messages=["Invalid attacker or defender!"]
            )
        
        # Check if weapon can attack at current range
        if not attacker.weapon.can_attack_at_range(attacker.range_band):
            return AttackResult(
                attacker=attacker.name,
                defender=defender.name,
                weapon=attacker.weapon.name,
                hit=False,
                roll=0,
                total_attack=0,
                defense=defender.defense,
                messages=[f"Cannot attack with {attacker.weapon.name} at {attacker.range_band.value} range!"]
            )
        
        # Check ammo for ranged weapons
        if attacker.weapon.is_ranged and not attacker.weapon.consume_ammo():
            return AttackResult(
                attacker=attacker.name,
                defender=defender.name,
                weapon=attacker.weapon.name,
                hit=False,
                roll=0,
                total_attack=0,
                defense=defender.defense,
                messages=[f"{attacker.weapon.name} is empty! Reload required."]
            )
        
        # Roll attack
        roll, total_attack, is_nat20 = attacker.roll_attack(weapon_skill)
        defense = defender.defense
        
        # Full cover = untargetable
        if defender.cover == CoverType.FULL:
            return AttackResult(
                attacker=attacker.name,
                defender=defender.name,
                weapon=attacker.weapon.name,
                hit=False,
                roll=roll,
                total_attack=total_attack,
                defense=defense,
                messages=[f"{defender.name} is in full cover and cannot be targeted!"]
            )
        
        # Check hit
        hit = total_attack >= defense
        
        result = AttackResult(
            attacker=attacker.name,
            defender=defender.name,
            weapon=attacker.weapon.name,
            hit=hit,
            roll=roll,
            total_attack=total_attack,
            defense=defense
        )
        
        if hit:
            # Check for crit
            is_crit = attacker.is_crit(roll, is_nat20)
            result.is_crit = is_crit
            
            # Roll damage
            stat_bonus = attacker.stats.body if attacker.weapon.is_melee else 0
            stat_bonus += attacker.stats.damage_bonus
            
            base_damage, total_damage = attacker.weapon.roll_damage(stat_bonus, is_crit)
            result.damage = total_damage
            
            # Determine hit location for crits
            hit_location = "torso"
            if is_crit:
                crit_roll = random.randint(1, 10)
                result.crit_location = CRIT_TABLE[crit_roll - 1]
                hit_location = result.crit_location.location
                
                # Apply crit effects
                if result.crit_location.stat_penalty.get("bleeding"):
                    defender.apply_status(StatusEffect.BLEEDING, -1)
                if result.crit_location.stat_penalty.get("stunned"):
                    defender.apply_status(StatusEffect.STUNNED, 1)
                if result.crit_location.stat_penalty.get("unconscious"):
                    defender.stats.hp = 0
            
            # Apply damage
            damage_dealt, damage_messages = defender.take_damage(total_damage, hit_location)
            result.damage_dealt = damage_dealt
            result.messages.extend(damage_messages)
            
            # Trigger on_damage callback
            if self.on_damage:
                self.on_damage(attacker, defender, damage_dealt)
            
            # Check for death
            if not defender.is_alive and self.on_death:
                self.on_death(defender)
        
        # Reset aim bonus after attack
        attacker.aim_bonus = 0
        attacker.has_acted = True
        
        return result
    
    def do_aim(self, combatant_id: str, target_id: Optional[str] = None) -> list[str]:
        """Perform aim action. +2 to next attack, stacks 2x."""
        combatant = self.combatants.get(combatant_id)
        if not combatant:
            return ["Invalid combatant!"]
        
        if combatant.aim_bonus >= 4:  # Max +4 from 2 aims
            return [f"{combatant.name} is already fully aimed."]
        
        combatant.aim_bonus += 2
        combatant.has_acted = True
        
        return [f"{combatant.name} takes aim... (+{combatant.aim_bonus} to next attack)"]
    
    def do_take_cover(self, combatant_id: str, cover_type: CoverType) -> list[str]:
        """Take cover action."""
        combatant = self.combatants.get(combatant_id)
        if not combatant:
            return ["Invalid combatant!"]
        
        combatant.cover = cover_type
        combatant.has_acted = True
        
        bonus = COVER_BONUS.get(cover_type, 0)
        return [f"{combatant.name} takes {cover_type.value} cover. (+{bonus} Defense)"]
    
    def do_reload(self, combatant_id: str) -> list[str]:
        """Reload weapon action."""
        combatant = self.combatants.get(combatant_id)
        if not combatant:
            return ["Invalid combatant!"]
        
        if combatant.weapon.reload():
            combatant.has_acted = True
            return [f"{combatant.name} reloads their {combatant.weapon.name}. "
                   f"({combatant.weapon.current_ammo}/{combatant.weapon.ammo_capacity})"]
        else:
            return [f"{combatant.weapon.name} doesn't need reloading."]
    
    def do_move(self, combatant_id: str, direction: str) -> list[str]:
        """Move one range band closer or farther."""
        combatant = self.combatants.get(combatant_id)
        if not combatant:
            return ["Invalid combatant!"]
        
        if combatant.has_moved:
            return [f"{combatant.name} has already moved this turn!"]
        
        current_idx = RANGE_ORDER.index(combatant.range_band)
        
        if direction == "closer":
            if current_idx == 0:
                return [f"{combatant.name} is already at melee range!"]
            combatant.range_band = RANGE_ORDER[current_idx - 1]
        elif direction == "farther":
            if current_idx == len(RANGE_ORDER) - 1:
                return [f"{combatant.name} is already at extreme range!"]
            combatant.range_band = RANGE_ORDER[current_idx + 1]
        else:
            return [f"Invalid direction: {direction}"]
        
        # Moving breaks cover
        combatant.cover = CoverType.NONE
        combatant.has_moved = True
        
        return [f"{combatant.name} moves to {combatant.range_band.value} range."]
    
    def check_combat_end(self) -> Optional[str]:
        """
        Check if combat should end.
        Returns winning side or None if combat continues.
        """
        alive_combatants = [c for c in self.combatants.values() if c.is_alive]
        
        if len(alive_combatants) <= 1:
            self.is_active = False
            if self.on_combat_end:
                self.on_combat_end(self)
            if alive_combatants:
                return alive_combatants[0].name
            return "draw"
        
        return None
    
    def get_status(self) -> str:
        """Get current combat status."""
        lines = [f"=== Combat Status (Round {self.round_number}) ==="]
        
        for cid in self.turn_order:
            combatant = self.combatants.get(cid)
            if not combatant:
                continue
            
            marker = "→ " if cid == self.turn_order[self.current_turn_index] else "  "
            status = "DEAD" if not combatant.is_alive else (
                "KO" if not combatant.is_conscious else "OK"
            )
            
            hp_str = f"{combatant.stats.hp}/{combatant.stats.max_hp}"
            effects = ", ".join(e.value for e in combatant.status_effects.keys())
            effects_str = f" [{effects}]" if effects else ""
            
            lines.append(f"{marker}{combatant.name}: HP {hp_str} | {status}{effects_str}")
        
        return "\n".join(lines)


# Convenience function for creating a basic combatant
def create_combatant(
    id: str,
    name: str,
    body: int = 5,
    reflexes: int = 5,
    tech: int = 5,
    cool: int = 5,
    weapon: Optional[Weapon] = None,
    armor: Optional[ArmorSet] = None
) -> Combatant:
    """Create a combatant with given stats."""
    stats = CombatStats(body=body, reflexes=reflexes, tech=tech, cool=cool)
    return Combatant(
        id=id,
        name=name,
        stats=stats,
        weapon=weapon or UNARMED,
        armor=armor or ArmorSet()
    )
