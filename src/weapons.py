"""
ClawMUD Weapons System
Weapon definitions, loading, and damage calculations.
"""
import json
import random
from pathlib import Path
from dataclasses import dataclass, field
from enum import Enum
from typing import Optional


class WeaponType(Enum):
    """Weapon type categories."""
    UNARMED = "unarmed"
    KNIFE = "knife"
    SWORD = "sword"
    BLUNT = "blunt"
    CYBERWEAPON = "cyberweapon"
    LIGHT_PISTOL = "light_pistol"
    HEAVY_PISTOL = "heavy_pistol"
    SMG = "smg"
    ASSAULT_RIFLE = "assault_rifle"
    SHOTGUN = "shotgun"
    SNIPER_RIFLE = "sniper_rifle"
    HEAVY_WEAPON = "heavy_weapon"


class DamageType(Enum):
    """Damage types for weapons."""
    PHYSICAL = "physical"
    ELECTRICAL = "electrical"
    EMP = "emp"
    FIRE = "fire"


class RangeBand(Enum):
    """Combat range bands."""
    MELEE = "melee"
    CLOSE = "close"
    MEDIUM = "medium"
    FAR = "far"
    EXTREME = "extreme"


# Range band order for distance calculations
RANGE_ORDER = [RangeBand.MELEE, RangeBand.CLOSE, RangeBand.MEDIUM, RangeBand.FAR, RangeBand.EXTREME]


@dataclass
class Weapon:
    """Represents a weapon in the game."""
    id: str
    name: str
    weapon_type: WeaponType
    damage_dice: int  # Number of d6
    damage_bonus: int = 0
    damage_type: DamageType = DamageType.PHYSICAL
    ideal_range: RangeBand = RangeBand.CLOSE
    rate_of_fire: int = 1  # Attacks per round if only attacking
    ammo_capacity: int = 0  # 0 = unlimited (melee)
    current_ammo: int = 0
    concealable: bool = False
    requires_aim: bool = False
    crit_bonus: int = 0  # Bonus to crit range
    special: list = field(default_factory=list)
    description: str = ""
    
    def __post_init__(self):
        if self.current_ammo == 0 and self.ammo_capacity > 0:
            self.current_ammo = self.ammo_capacity
    
    @property
    def is_melee(self) -> bool:
        """Check if weapon is melee-type."""
        return self.weapon_type in [
            WeaponType.UNARMED, WeaponType.KNIFE, 
            WeaponType.SWORD, WeaponType.BLUNT, WeaponType.CYBERWEAPON
        ]
    
    @property
    def is_ranged(self) -> bool:
        """Check if weapon is ranged."""
        return not self.is_melee
    
    def roll_damage(self, stat_bonus: int = 0, is_crit: bool = False) -> tuple[int, int]:
        """
        Roll damage for this weapon.
        Returns (base_roll, total_damage).
        """
        dice = self.damage_dice
        if is_crit:
            dice *= 2  # Double dice on crit
        
        base_roll = sum(random.randint(1, 6) for _ in range(dice))
        variance = random.randint(1, 6)
        total = base_roll + self.damage_bonus + stat_bonus + variance
        
        return base_roll, total
    
    def get_range_modifier(self, current_range: RangeBand) -> int:
        """Get accuracy modifier based on range band."""
        if self.is_melee:
            if current_range == RangeBand.MELEE:
                return 2  # Melee bonus at melee range
            return -100  # Can't use melee at range
        
        # Ranged weapon modifiers
        current_idx = RANGE_ORDER.index(current_range)
        ideal_idx = RANGE_ORDER.index(self.ideal_range)
        distance = current_idx - ideal_idx
        
        # Special cases
        if self.weapon_type == WeaponType.SHOTGUN:
            # Shotgun loses 1d6 damage per range band (handled elsewhere)
            if current_range == RangeBand.MELEE:
                return -2
            return 0
        
        if self.weapon_type == WeaponType.SNIPER_RIFLE:
            if current_range in [RangeBand.MELEE, RangeBand.CLOSE]:
                return -4
        
        # General modifiers
        if current_range == RangeBand.MELEE:
            return -2  # Hard to aim up close
        
        if distance == 0:
            return 0  # Ideal range
        elif distance < 0:
            return -2  # Too close
        else:
            return -2 * distance  # Penalty for being too far
    
    def can_attack_at_range(self, current_range: RangeBand) -> bool:
        """Check if weapon can attack at given range."""
        if self.is_melee:
            return current_range == RangeBand.MELEE
        
        # Pistols can't hit at extreme
        if self.weapon_type in [WeaponType.LIGHT_PISTOL, WeaponType.HEAVY_PISTOL]:
            return current_range != RangeBand.EXTREME
        
        # Only snipers effective at extreme
        if current_range == RangeBand.EXTREME:
            return self.weapon_type == WeaponType.SNIPER_RIFLE
        
        return True
    
    def reload(self) -> bool:
        """Reload weapon. Returns True if successful."""
        if self.ammo_capacity == 0:
            return False  # Melee weapons don't reload
        self.current_ammo = self.ammo_capacity
        return True
    
    def consume_ammo(self, shots: int = 1) -> bool:
        """Consume ammo. Returns True if successful."""
        if self.ammo_capacity == 0:
            return True  # Melee always works
        if self.current_ammo >= shots:
            self.current_ammo -= shots
            return True
        return False
    
    def to_dict(self) -> dict:
        """Convert to dictionary for serialization."""
        return {
            "id": self.id,
            "name": self.name,
            "weapon_type": self.weapon_type.value,
            "damage_dice": self.damage_dice,
            "damage_bonus": self.damage_bonus,
            "damage_type": self.damage_type.value,
            "ideal_range": self.ideal_range.value,
            "rate_of_fire": self.rate_of_fire,
            "ammo_capacity": self.ammo_capacity,
            "current_ammo": self.current_ammo,
            "concealable": self.concealable,
            "requires_aim": self.requires_aim,
            "crit_bonus": self.crit_bonus,
            "special": self.special,
            "description": self.description
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "Weapon":
        """Create weapon from dictionary."""
        return cls(
            id=data["id"],
            name=data["name"],
            weapon_type=WeaponType(data["weapon_type"]),
            damage_dice=data["damage_dice"],
            damage_bonus=data.get("damage_bonus", 0),
            damage_type=DamageType(data.get("damage_type", "physical")),
            ideal_range=RangeBand(data.get("ideal_range", "close")),
            rate_of_fire=data.get("rate_of_fire", 1),
            ammo_capacity=data.get("ammo_capacity", 0),
            current_ammo=data.get("current_ammo", 0),
            concealable=data.get("concealable", False),
            requires_aim=data.get("requires_aim", False),
            crit_bonus=data.get("crit_bonus", 0),
            special=data.get("special", []),
            description=data.get("description", "")
        )


class WeaponRegistry:
    """Registry for loading and managing weapon templates."""
    
    def __init__(self):
        self.templates: dict[str, dict] = {}
    
    def load_from_file(self, path: str | Path) -> None:
        """Load weapon templates from JSON file."""
        path = Path(path)
        if path.exists():
            with open(path) as f:
                data = json.load(f)
                for weapon_data in data.get("weapons", []):
                    self.templates[weapon_data["id"]] = weapon_data
    
    def create_weapon(self, weapon_id: str) -> Optional[Weapon]:
        """Create a new weapon instance from template."""
        if weapon_id not in self.templates:
            return None
        return Weapon.from_dict(self.templates[weapon_id].copy())
    
    def get_template(self, weapon_id: str) -> Optional[dict]:
        """Get weapon template data."""
        return self.templates.get(weapon_id)
    
    def list_weapons(self, weapon_type: Optional[WeaponType] = None) -> list[str]:
        """List all weapon IDs, optionally filtered by type."""
        if weapon_type is None:
            return list(self.templates.keys())
        return [
            wid for wid, data in self.templates.items()
            if WeaponType(data["weapon_type"]) == weapon_type
        ]


# Default unarmed weapon
UNARMED = Weapon(
    id="unarmed",
    name="Fists",
    weapon_type=WeaponType.UNARMED,
    damage_dice=1,
    damage_bonus=0,
    ideal_range=RangeBand.MELEE,
    description="Your bare hands. Always available."
)


# Global weapon registry
weapon_registry = WeaponRegistry()


def load_weapons(data_dir: str | Path = "data") -> None:
    """Load weapons from the data directory."""
    weapon_registry.load_from_file(Path(data_dir) / "weapons.json")
