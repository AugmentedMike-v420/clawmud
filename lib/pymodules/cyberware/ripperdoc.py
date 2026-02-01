"""
ClawMUD Cyberware System - Ripperdoc Module

Handles cyberware installation, removal, ripperdoc types,
installation checks, and complications.
"""
import mud, mudsys, hooks
import random

from .cyberware import (
    get_cyberware_by_id, 
    can_install_cyberware,
    InstalledCyberware,
    apply_cyberware_effects,
    remove_cyberware_effects,
)
from .humanity import modify_humanity

################################################################################
# Constants
################################################################################

# Ripperdoc types and their bonuses
RIPPERDOC_TYPES = {
    "street_doc": {
        "name": "Street Doc",
        "install_bonus": 0,
        "risk": "high",
        "cost_mult": 0.5,
        "description": "Back-alley surgery. Cheap but risky.",
    },
    "licensed_clinic": {
        "name": "Licensed Clinic",
        "install_bonus": 4,
        "risk": "low",
        "cost_mult": 1.0,
        "description": "Legal operation. Safe but regulated.",
    },
    "corp_hospital": {
        "name": "Corp Hospital",
        "install_bonus": 8,
        "risk": "minimal",
        "cost_mult": 3.0,
        "description": "Top-tier medical care. Very safe, very expensive.",
    },
    "black_clinic": {
        "name": "Black Clinic",
        "install_bonus": 2,
        "risk": "moderate",
        "cost_mult": 1.5,
        "description": "Underground but professional. Black market access.",
    },
}

# Complications table (1d10)
COMPLICATIONS = {
    1: {
        "name": "infection",
        "description": "Infection: -2 all stats until treated",
        "effect": "stat_penalty",
        "value": -2,
        "duration": "until_treated",
    },
    2: {
        "name": "infection",
        "description": "Infection: -2 all stats until treated",
        "effect": "stat_penalty",
        "value": -2,
        "duration": "until_treated",
    },
    3: {
        "name": "neural_glitch",
        "description": "Neural glitch: Random malfunction 1/day",
        "effect": "malfunction",
        "value": 1,
        "duration": "permanent",
    },
    4: {
        "name": "neural_glitch",
        "description": "Neural glitch: Random malfunction 1/day",
        "effect": "malfunction",
        "value": 1,
        "duration": "permanent",
    },
    5: {
        "name": "rejection",
        "description": "Rejection: Lose 1 extra Humanity",
        "effect": "humanity_loss",
        "value": 1,
        "duration": "instant",
    },
    6: {
        "name": "rejection",
        "description": "Rejection: Lose 1 extra Humanity",
        "effect": "humanity_loss",
        "value": 1,
        "duration": "instant",
    },
    7: {
        "name": "scarring",
        "description": "Scarring: -1 social permanently",
        "effect": "social_penalty",
        "value": -1,
        "duration": "permanent",
    },
    8: {
        "name": "scarring",
        "description": "Scarring: -1 social permanently",
        "effect": "social_penalty",
        "value": -1,
        "duration": "permanent",
    },
    9: {
        "name": "chronic_pain",
        "description": "Chronic pain: -1 all actions until fixed",
        "effect": "action_penalty",
        "value": -1,
        "duration": "until_treated",
    },
    10: {
        "name": "catastrophic",
        "description": "Catastrophic: Take 2d6 additional damage",
        "effect": "damage",
        "value": "2d6",
        "duration": "instant",
    },
}

# Installation result messages
INSTALL_RESULTS = {
    "success": [
        "The chrome slides into place perfectly.",
        "Installation complete. Systems online.",
        "Clean work. You barely feel different... but you are.",
        "The doc steps back, admiring their work. 'Good as new, choom.'",
    ],
    "partial": [
        "It's in, but something feels... off.",
        "Installation complete, but there were complications.",
        "The chrome works, but not at full capacity.",
        "The doc frowns. 'It'll work, but you might notice some issues.'",
    ],
    "complication": [
        "Something went wrong during the procedure.",
        "The installation didn't go smoothly.",
        "You wake up feeling worse than expected.",
        "The doc curses under their breath. 'We have a problem.'",
    ],
    "rejection": [
        "Your body violently rejects the chrome.",
        "The installation fails catastrophically.",
        "The cyberware fries itself during integration.",
        "The doc scrambles to stabilize you as the chrome dies.",
    ],
}


################################################################################
# Installation Functions
################################################################################

def get_installation_dc(cyberware_id, quality="standard"):
    """Get the installation DC for cyberware"""
    cyber = get_cyberware_by_id(cyberware_id)
    if not cyber:
        return 99  # Impossible
    
    return cyber.get_install_dc(quality)


def roll_installation(ch, cyberware_id, quality="standard", doc_type="street_doc"):
    """
    Roll an installation check.
    Returns (result: str, roll: int, dc: int, margin: int)
    
    Results: "success", "partial", "complication", "rejection"
    """
    cyber = get_cyberware_by_id(cyberware_id)
    if not cyber:
        return "rejection", 0, 99, -99
    
    doc = RIPPERDOC_TYPES.get(doc_type, RIPPERDOC_TYPES["street_doc"])
    
    # Calculate DC
    dc = cyber.get_install_dc(quality)
    
    # Roll: 1d20 + doc_bonus + patient_TECH
    roll = random.randint(1, 20)
    doc_bonus = doc["install_bonus"]
    
    # TODO: Get actual TECH stat from character
    tech_bonus = 0
    
    total = roll + doc_bonus + tech_bonus
    margin = total - dc
    
    # Determine result
    if margin >= 0:
        result = "success"
    elif margin >= -5:
        result = "partial"  # Installed but reduced function
    elif margin >= -10:
        result = "complication"  # Installed but complication
    else:
        result = "rejection"  # Failed completely
    
    return result, total, dc, margin


def get_complication():
    """Roll for a random complication"""
    roll = random.randint(1, 10)
    return COMPLICATIONS.get(roll, COMPLICATIONS[1])


def apply_complication(ch, complication, installed=None):
    """Apply a complication to the character"""
    effect = complication["effect"]
    value = complication["value"]
    
    if effect == "humanity_loss":
        modify_humanity(ch, -value)
        ch.send("{rThe botched installation costs you %d extra Humanity.{n" % value)
    
    elif effect == "damage":
        # Roll damage (2d6)
        damage = random.randint(1, 6) + random.randint(1, 6)
        # TODO: Apply actual damage through vitality system
        ch.send("{rYou take %d damage from the failed installation!{n" % damage)
        hooks.run("cyberware_complication_damage", 
                  hooks.build_info("ch int", (ch, damage)))
    
    elif effect == "stat_penalty":
        ch.send("{rYou feel weakened. -%d to all stats until treated.{n" % abs(value))
        hooks.run("cyberware_complication_stat_penalty",
                  hooks.build_info("ch int", (ch, value)))
    
    elif effect == "social_penalty":
        ch.send("{rPermanent scarring. %d to social checks.{n" % value)
        hooks.run("cyberware_complication_social_penalty",
                  hooks.build_info("ch int", (ch, value)))
    
    elif effect == "malfunction":
        if installed:
            installed.complication = complication["name"]
        ch.send("{rThe chrome has a glitch. Expect malfunctions.{n")
    
    elif effect == "action_penalty":
        ch.send("{rChronic pain. %d to all actions until fixed.{n" % value)
        hooks.run("cyberware_complication_action_penalty",
                  hooks.build_info("ch int", (ch, value)))


################################################################################
# Core Installation/Removal
################################################################################

def install_cyberware(ch, cyberware_id, quality="standard", doc_type="street_doc"):
    """
    Install cyberware on a character.
    Returns (success: bool, message: str)
    """
    # Check if can install
    can, reason = can_install_cyberware(ch, cyberware_id, quality)
    if not can:
        return False, reason
    
    cyber = get_cyberware_by_id(cyberware_id)
    if not cyber:
        return False, "Unknown cyberware"
    
    # Roll installation
    result, total, dc, margin = roll_installation(ch, cyberware_id, quality, doc_type)
    
    # Get random flavor text
    flavor = random.choice(INSTALL_RESULTS.get(result, INSTALL_RESULTS["success"]))
    
    # Handle results
    if result == "rejection":
        ch.send("{r%s{n" % flavor)
        ch.send("{rInstallation failed! The cyberware is destroyed.{n")
        ch.send("{D(Roll: %d vs DC %d, margin: %d){n" % (total, dc, margin))
        
        # Still lose some humanity for the trauma
        trauma_cost = cyber.get_humanity_cost(quality) // 4
        if trauma_cost > 0:
            modify_humanity(ch, -trauma_cost)
            ch.send("{rThe trauma costs you %d Humanity.{n" % trauma_cost)
        
        return False, "Installation failed - cyberware rejected"
    
    # Get character's cyberware data
    aux = ch.getAuxiliary("cyberware_data")
    if not aux:
        return False, "No cyberware data found"
    
    # Create installed cyberware record
    installed = InstalledCyberware(
        cyberware_id=cyberware_id,
        quality=quality,
        functional=True,
        complication=None
    )
    
    # Handle partial success
    if result == "partial":
        installed.functional = False  # Reduced functionality
        ch.send("{y%s{n" % flavor)
        ch.send("{yThe cyberware is installed but not at full capacity.{n")
    
    # Handle complication
    elif result == "complication":
        complication = get_complication()
        ch.send("{y%s{n" % flavor)
        ch.send("{r%s{n" % complication["description"])
        apply_complication(ch, complication, installed)
    
    else:
        ch.send("{g%s{n" % flavor)
    
    ch.send("{D(Roll: %d vs DC %d, margin: %d){n" % (total, dc, margin))
    
    # Add to installed list
    aux.installed.append(installed)
    
    # Update slots
    loc = cyber.slot_location
    aux.slots_used[loc] = aux.slots_used.get(loc, 0) + cyber.slots_required
    
    # Apply humanity cost
    humanity_cost = cyber.get_humanity_cost(quality)
    modify_humanity(ch, -humanity_cost)
    ch.send("{wHumanity: -%d{n" % humanity_cost)
    
    # Apply effects
    apply_cyberware_effects(ch, installed)
    
    # Run hook
    hooks.run("cyberware_installed",
              hooks.build_info("ch str str str", (ch, cyberware_id, quality, result)))
    
    ch.send("{gSuccessfully installed: %s (%s quality){n" % (cyber.name, quality))
    
    return True, "Installation complete"


def remove_cyberware(ch, cyberware_id):
    """
    Remove cyberware from a character.
    Returns (success: bool, message: str)
    """
    from .humanity import recover_humanity_from_removal
    
    aux = ch.getAuxiliary("cyberware_data")
    if not aux:
        return False, "No cyberware data found"
    
    # Find the installed cyberware
    installed = None
    for i in aux.installed:
        if i.cyberware_id == cyberware_id:
            installed = i
            break
    
    if not installed:
        return False, "You don't have that cyberware installed"
    
    cyber = get_cyberware_by_id(cyberware_id)
    if not cyber:
        return False, "Unknown cyberware in your system"
    
    # Check for dependencies
    for other in aux.installed:
        other_cyber = other.get_cyberware()
        if other_cyber and other_cyber.requires == cyberware_id:
            return False, "Cannot remove - %s depends on this cyberware" % other_cyber.name
    
    # Remove effects
    remove_cyberware_effects(ch, installed)
    
    # Remove from list
    aux.installed.remove(installed)
    
    # Update slots
    loc = cyber.slot_location
    aux.slots_used[loc] = max(0, aux.slots_used.get(loc, 0) - cyber.slots_required)
    
    # Recover partial humanity
    recovered = recover_humanity_from_removal(ch, cyberware_id, installed.quality)
    
    ch.send("{gRemoved: %s{n" % cyber.name)
    if recovered > 0:
        ch.send("{wHumanity: +%d (50%% recovery){n" % recovered)
    
    # Run hook
    hooks.run("cyberware_removed",
              hooks.build_info("ch str", (ch, cyberware_id)))
    
    return True, "Removal complete"


################################################################################
# Commands
################################################################################

def cmd_install(ch, cmd, arg):
    """Install cyberware (admin/ripperdoc command)"""
    if not arg:
        ch.send("Usage: install <cyberware_id> [quality] [doc_type]")
        ch.send("Qualities: street, standard, corp, milspec, prototype")
        ch.send("Doc types: street_doc, licensed_clinic, corp_hospital, black_clinic")
        return
    
    args = arg.split()
    cyberware_id = args[0]
    quality = args[1] if len(args) > 1 else "standard"
    doc_type = args[2] if len(args) > 2 else "licensed_clinic"
    
    # Validate quality
    from .cyberware import QUALITY_TIERS
    if quality not in QUALITY_TIERS:
        ch.send("Invalid quality. Options: %s" % ", ".join(QUALITY_TIERS.keys()))
        return
    
    # Validate doc type
    if doc_type not in RIPPERDOC_TYPES:
        ch.send("Invalid doc type. Options: %s" % ", ".join(RIPPERDOC_TYPES.keys()))
        return
    
    # Check cyberware exists
    cyber = get_cyberware_by_id(cyberware_id)
    if not cyber:
        ch.send("Unknown cyberware: %s" % cyberware_id)
        ch.send("Use 'cyberware' to browse available options.")
        return
    
    # Show confirmation
    doc = RIPPERDOC_TYPES[doc_type]
    hu_cost = cyber.get_humanity_cost(quality)
    price = cyber.get_price(quality) * doc["cost_mult"]
    install_dc = cyber.get_install_dc(quality)
    
    ch.send("{c--- Installation Preview ---{n")
    ch.send("{wCyberware:{n %s" % cyber.name)
    ch.send("{wQuality:{n %s" % quality)
    ch.send("{wRipperdoc:{n %s (%s risk)" % (doc["name"], doc["risk"]))
    ch.send("{wHumanity Cost:{n %d" % hu_cost)
    ch.send("{wPrice:{n %d eb" % int(price))
    ch.send("{wInstall DC:{n %d (doc bonus: +%d)" % (install_dc, doc["install_bonus"]))
    ch.send("")
    
    # Perform installation
    success, message = install_cyberware(ch, cyberware_id, quality, doc_type)
    if not success:
        ch.send("{r%s{n" % message)


def cmd_remove(ch, cmd, arg):
    """Remove cyberware (admin/ripperdoc command)"""
    if not arg:
        ch.send("Usage: remove <cyberware_id>")
        ch.send("Use 'chrome' to see your installed cyberware.")
        return
    
    cyberware_id = arg.strip()
    
    # Check if they have it
    aux = ch.getAuxiliary("cyberware_data")
    if not aux:
        ch.send("Error: No cyberware data found.")
        return
    
    has_it = aux.has_cyberware(cyberware_id)
    if not has_it:
        ch.send("You don't have '%s' installed." % cyberware_id)
        return
    
    cyber = get_cyberware_by_id(cyberware_id)
    if cyber:
        ch.send("{yPreparing to remove: %s{n" % cyber.name)
    
    success, message = remove_cyberware(ch, cyberware_id)
    if not success:
        ch.send("{r%s{n" % message)


def cmd_ripperdoc(ch, cmd, arg):
    """Display information about ripperdoc types"""
    ch.send("{c=== Ripperdoc Types ==={n")
    ch.send("")
    
    for doc_id, doc in RIPPERDOC_TYPES.items():
        risk_color = {
            "minimal": "g", "low": "G", "moderate": "y", "high": "r"
        }.get(doc["risk"], "w")
        
        ch.send("{Y%s{n (%s)" % (doc["name"], doc_id))
        ch.send("  %s" % doc["description"])
        ch.send("  {wInstall Bonus:{n +%d" % doc["install_bonus"])
        ch.send("  {wRisk:{n {%s%s{n" % (risk_color, doc["risk"]))
        ch.send("  {wCost Multiplier:{n %.1fx" % doc["cost_mult"])
        ch.send("")


################################################################################
# Initialization
################################################################################

# Add commands
mudsys.add_cmd("install", None, cmd_install, "admin", False)
mudsys.add_cmd("remove", None, cmd_remove, "admin", False)
mudsys.add_cmd("ripperdoc", None, cmd_ripperdoc, "player", False)
mudsys.add_cmd("ripperdocs", None, cmd_ripperdoc, "player", False)


def __unload__():
    """Clean up when module is unloaded"""
    pass
