"""
ClawMUD Cyberware System

Chrome. Implants. The line between human and machine.

Modules:
- cyberware: Core cyberware data structures and catalog
- humanity: Humanity tracking and cyberpsychosis mechanics
- ripperdoc: Installation, removal, and complications
"""

from .cyberware import (
    CyberwareAuxData,
    get_cyberware_catalog,
    get_cyberware_by_id,
    get_cyberware_by_slot,
    get_installed_cyberware,
    can_install_cyberware,
    BODY_SLOTS,
    QUALITY_TIERS,
)

from .humanity import (
    get_humanity,
    set_humanity,
    modify_humanity,
    get_humanity_status,
    check_cyberpsychosis,
    do_therapy,
    HUMANITY_THRESHOLDS,
)

from .ripperdoc import (
    install_cyberware,
    remove_cyberware,
    get_installation_dc,
    roll_installation,
    RIPPERDOC_TYPES,
    COMPLICATIONS,
)

__all__ = [
    # Cyberware core
    'CyberwareAuxData',
    'get_cyberware_catalog',
    'get_cyberware_by_id',
    'get_cyberware_by_slot',
    'get_installed_cyberware',
    'can_install_cyberware',
    'BODY_SLOTS',
    'QUALITY_TIERS',
    # Humanity
    'get_humanity',
    'set_humanity',
    'modify_humanity',
    'get_humanity_status',
    'check_cyberpsychosis',
    'do_therapy',
    'HUMANITY_THRESHOLDS',
    # Ripperdoc
    'install_cyberware',
    'remove_cyberware',
    'get_installation_dc',
    'roll_installation',
    'RIPPERDOC_TYPES',
    'COMPLICATIONS',
]
