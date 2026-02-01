"""
ClawMUD Armor System
Armor definitions, damage reduction, and degradation.
"""
import json
from pathlib import Path
from dataclasses import dataclass, field
from enum import Enum
from typing import Optional


class ArmorType(Enum):
    """Armor type categories."""
    NONE = "none"
    LIGHT = "light"
    MEDIUM = "medium"
    HEAVY = "heavy"
    POWERED = "powered"
    SUBDERMAL = "subdermal"  # Cyberware


class ArmorSlot(Enum):
    """Body slots for armor."""
    BODY = "body"  # Main armor slot
    HEAD = "head"
    SUBDERMAL = "subdermal"  # Cyberware slot


@dataclass
class Armor:
    """Represents armor equipment."""
    id: str
    name: str
    armor_type: ArmorType
    stopping_power: int  # SP - flat damage reduction
    max_stopping_power: int = 0  # For tracking degradation
    dodge_penalty: int = 0  # Negative modifier to dodge
    slot: ArmorSlot = ArmorSlot.BODY
    tech_requirement: int = 0  # Minimum TECH stat required
    concealable: bool = False
    is_cyberware: bool = False
    special: list = field(default_factory=list)
    description: str = ""
    
    def __post_init__(self):
        if self.max_stopping_power == 0:
            self.max_stopping_power = self.stopping_power
    
    @property
    def is_damaged(self) -> bool:
        """Check if armor is degraded."""
        return self.stopping_power < self.max_stopping_power
    
    @property
    def condition_percent(self) -> int:
        """Get armor condition as percentage."""
        if self.max_stopping_power == 0:
            return 100
        return int((self.stopping_power / self.max_stopping_power) * 100)
    
    def reduce_damage(self, incoming_damage: int) -> tuple[int, bool]:
        """
        Apply armor damage reduction.
        Returns (final_damage, armor_degraded).
        """
        if self.stopping_power <= 0:
            return incoming_damage, False
        
        # Calculate damage after armor
        final_damage = max(1, incoming_damage - self.stopping_power)
        
        # Armor degrades if damage penetrated
        degraded = False
        if incoming_damage > self.stopping_power:
            self.stopping_power = max(0, self.stopping_power - 1)
            degraded = True
        
        return final_damage, degraded
    
    def repair(self, amount: Optional[int] = None) -> int:
        """
        Repair armor SP. Returns amount repaired.
        If amount is None, fully repairs.
        """
        if amount is None:
            repaired = self.max_stopping_power - self.stopping_power
            self.stopping_power = self.max_stopping_power
        else:
            old_sp = self.stopping_power
            self.stopping_power = min(self.max_stopping_power, self.stopping_power + amount)
            repaired = self.stopping_power - old_sp
        return repaired
    
    def to_dict(self) -> dict:
        """Convert to dictionary for serialization."""
        return {
            "id": self.id,
            "name": self.name,
            "armor_type": self.armor_type.value,
            "stopping_power": self.stopping_power,
            "max_stopping_power": self.max_stopping_power,
            "dodge_penalty": self.dodge_penalty,
            "slot": self.slot.value,
            "tech_requirement": self.tech_requirement,
            "concealable": self.concealable,
            "is_cyberware": self.is_cyberware,
            "special": self.special,
            "description": self.description
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "Armor":
        """Create armor from dictionary."""
        return cls(
            id=data["id"],
            name=data["name"],
            armor_type=ArmorType(data["armor_type"]),
            stopping_power=data["stopping_power"],
            max_stopping_power=data.get("max_stopping_power", data["stopping_power"]),
            dodge_penalty=data.get("dodge_penalty", 0),
            slot=ArmorSlot(data.get("slot", "body")),
            tech_requirement=data.get("tech_requirement", 0),
            concealable=data.get("concealable", False),
            is_cyberware=data.get("is_cyberware", False),
            special=data.get("special", []),
            description=data.get("description", "")
        )


@dataclass
class ArmorSet:
    """
    Represents all armor worn by a combatant.
    Combines protection from multiple armor pieces.
    """
    body_armor: Optional[Armor] = None
    head_armor: Optional[Armor] = None
    subdermal_armor: Optional[Armor] = None  # Cyberware
    
    @property
    def total_stopping_power(self) -> int:
        """Get combined SP from all armor."""
        total = 0
        if self.body_armor:
            total += self.body_armor.stopping_power
        if self.subdermal_armor:
            total += self.subdermal_armor.stopping_power
        # Head armor only protects head (handled in crit location)
        return total
    
    @property
    def total_dodge_penalty(self) -> int:
        """Get combined dodge penalty from all armor."""
        penalty = 0
        if self.body_armor:
            penalty += self.body_armor.dodge_penalty
        if self.head_armor:
            penalty += self.head_armor.dodge_penalty
        # Subdermal has no dodge penalty
        return penalty
    
    def equip(self, armor: Armor) -> Optional[Armor]:
        """
        Equip armor to appropriate slot.
        Returns any armor that was replaced.
        """
        old_armor = None
        
        if armor.slot == ArmorSlot.BODY:
            old_armor = self.body_armor
            self.body_armor = armor
        elif armor.slot == ArmorSlot.HEAD:
            old_armor = self.head_armor
            self.head_armor = armor
        elif armor.slot == ArmorSlot.SUBDERMAL:
            old_armor = self.subdermal_armor
            self.subdermal_armor = armor
        
        return old_armor
    
    def unequip(self, slot: ArmorSlot) -> Optional[Armor]:
        """Unequip armor from slot. Returns removed armor."""
        armor = None
        
        if slot == ArmorSlot.BODY:
            armor = self.body_armor
            self.body_armor = None
        elif slot == ArmorSlot.HEAD:
            armor = self.head_armor
            self.head_armor = None
        elif slot == ArmorSlot.SUBDERMAL:
            armor = self.subdermal_armor
            self.subdermal_armor = None
        
        return armor
    
    def reduce_damage(self, incoming_damage: int, hit_location: str = "torso") -> tuple[int, list[str]]:
        """
        Apply damage reduction from all applicable armor.
        Returns (final_damage, list of degradation messages).
        """
        messages = []
        damage = incoming_damage
        
        # Head hits only blocked by head armor
        if hit_location == "head":
            if self.head_armor and self.head_armor.stopping_power > 0:
                damage, degraded = self.head_armor.reduce_damage(damage)
                if degraded:
                    messages.append(f"Your {self.head_armor.name} is damaged!")
            # Subdermal still helps
            if self.subdermal_armor and self.subdermal_armor.stopping_power > 0:
                damage, degraded = self.subdermal_armor.reduce_damage(damage)
                if degraded:
                    messages.append(f"Your {self.subdermal_armor.name} is damaged!")
        else:
            # Body hits - body armor + subdermal
            if self.body_armor and self.body_armor.stopping_power > 0:
                damage, degraded = self.body_armor.reduce_damage(damage)
                if degraded:
                    messages.append(f"Your {self.body_armor.name} is damaged!")
            if self.subdermal_armor and self.subdermal_armor.stopping_power > 0:
                damage, degraded = self.subdermal_armor.reduce_damage(damage)
                if degraded:
                    messages.append(f"Your {self.subdermal_armor.name} is damaged!")
        
        return max(1, damage), messages
    
    def get_all_armor(self) -> list[Armor]:
        """Get list of all equipped armor."""
        armor = []
        if self.body_armor:
            armor.append(self.body_armor)
        if self.head_armor:
            armor.append(self.head_armor)
        if self.subdermal_armor:
            armor.append(self.subdermal_armor)
        return armor


class ArmorRegistry:
    """Registry for loading and managing armor templates."""
    
    def __init__(self):
        self.templates: dict[str, dict] = {}
    
    def load_from_file(self, path: str | Path) -> None:
        """Load armor templates from JSON file."""
        path = Path(path)
        if path.exists():
            with open(path) as f:
                data = json.load(f)
                for armor_data in data.get("armor", []):
                    self.templates[armor_data["id"]] = armor_data
    
    def create_armor(self, armor_id: str) -> Optional[Armor]:
        """Create a new armor instance from template."""
        if armor_id not in self.templates:
            return None
        return Armor.from_dict(self.templates[armor_id].copy())
    
    def get_template(self, armor_id: str) -> Optional[dict]:
        """Get armor template data."""
        return self.templates.get(armor_id)
    
    def list_armor(self, armor_type: Optional[ArmorType] = None) -> list[str]:
        """List all armor IDs, optionally filtered by type."""
        if armor_type is None:
            return list(self.templates.keys())
        return [
            aid for aid, data in self.templates.items()
            if ArmorType(data["armor_type"]) == armor_type
        ]


# No armor placeholder
NO_ARMOR = Armor(
    id="none",
    name="No Armor",
    armor_type=ArmorType.NONE,
    stopping_power=0,
    description="Street clothes. No protection."
)


# Global armor registry
armor_registry = ArmorRegistry()


def load_armor(data_dir: str | Path = "data") -> None:
    """Load armor from the data directory."""
    armor_registry.load_from_file(Path(data_dir) / "armor.json")
