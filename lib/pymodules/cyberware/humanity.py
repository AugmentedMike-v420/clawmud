"""
ClawMUD Cyberware System - Humanity Module

Handles humanity tracking, thresholds, cyberpsychosis mechanics,
recovery through therapy and chrome removal.
"""
import mud, mudsys, auxiliary, storage, hooks, char
import random

################################################################################
# Constants
################################################################################

# Humanity thresholds and their effects
HUMANITY_THRESHOLDS = {
    "human": {
        "min": 71,
        "max": 100,
        "social_mod": 0,
        "description": "Normal social interactions",
        "color": "g",
    },
    "chromed": {
        "min": 41,
        "max": 70,
        "social_mod": -1,
        "description": "Some NPCs wary, minor social penalty",
        "color": "y",
    },
    "heavy_chrome": {
        "min": 21,
        "max": 40,
        "social_mod": -2,
        "description": "Corps/civilians avoid you",
        "color": "Y",
    },
    "bordering": {
        "min": 11,
        "max": 20,
        "social_mod": -3,
        "description": "Random glitches, therapy required",
        "color": "r",
    },
    "cyberpsycho_risk": {
        "min": 1,
        "max": 10,
        "social_mod": -4,
        "description": "Daily COOL check or episode",
        "color": "R",
    },
    "cyberpsychosis": {
        "min": 0,
        "max": 0,
        "social_mod": -99,
        "description": "Character becomes NPC",
        "color": "R",
    },
}

# Episode severity table
EPISODE_SEVERITY = {
    1: ("dissociation", "You lose an hour, confused and disoriented."),
    2: ("dissociation", "You lose an hour, confused and disoriented."),
    3: ("paranoia", "Everyone is a threat. You lash out and flee."),
    4: ("paranoia", "Everyone is a threat. You lash out and flee."),
    5: ("rage", "Red fills your vision. Everything must die."),
    6: ("full_break", "You are no longer in control. The chrome has won."),
}

# Therapy costs and effectiveness
THERAPY_CONFIG = {
    "cost_per_session": 500,
    "humanity_per_session": 1,
    "sessions_per_week": 1,
    "minimum_humanity_for_therapy": 1,
}


################################################################################
# Humanity Auxiliary Data
################################################################################

class HumanityAuxData:
    """Holds character humanity data"""
    
    def __init__(self, set=None):
        self.current = 100
        self.maximum = 100
        self.therapy_sessions = 0
        self.last_therapy_time = 0
        self.last_psychosis_check = 0
        self.episodes_total = 0
        self.in_episode = False
        self.episode_type = None
        
        if set is not None:
            self.read(set)
    
    def copyTo(self, to):
        """Copy humanity data to another instance"""
        to.current = self.current
        to.maximum = self.maximum
        to.therapy_sessions = self.therapy_sessions
        to.last_therapy_time = self.last_therapy_time
        to.last_psychosis_check = self.last_psychosis_check
        to.episodes_total = self.episodes_total
        to.in_episode = self.in_episode
        to.episode_type = self.episode_type
    
    def copy(self):
        """Create a copy of this humanity data"""
        newdata = HumanityAuxData()
        self.copyTo(newdata)
        return newdata
    
    def store(self):
        """Store humanity data to a storage set"""
        set = storage.StorageSet()
        set.storeInt("current", self.current)
        set.storeInt("maximum", self.maximum)
        set.storeInt("therapy_sessions", self.therapy_sessions)
        set.storeInt("last_therapy_time", self.last_therapy_time)
        set.storeInt("last_psychosis_check", self.last_psychosis_check)
        set.storeInt("episodes_total", self.episodes_total)
        set.storeBool("in_episode", self.in_episode)
        set.storeString("episode_type", self.episode_type or "")
        return set
    
    def read(self, set):
        """Read humanity data from a storage set"""
        if set.contains("current"):
            self.current = set.readInt("current")
        if set.contains("maximum"):
            self.maximum = set.readInt("maximum")
        if set.contains("therapy_sessions"):
            self.therapy_sessions = set.readInt("therapy_sessions")
        if set.contains("last_therapy_time"):
            self.last_therapy_time = set.readInt("last_therapy_time")
        if set.contains("last_psychosis_check"):
            self.last_psychosis_check = set.readInt("last_psychosis_check")
        if set.contains("episodes_total"):
            self.episodes_total = set.readInt("episodes_total")
        if set.contains("in_episode"):
            self.in_episode = set.readBool("in_episode")
        if set.contains("episode_type"):
            episode = set.readString("episode_type")
            self.episode_type = episode if episode else None


################################################################################
# Core Humanity Functions
################################################################################

def get_humanity(ch):
    """Get character's current humanity"""
    aux = ch.getAuxiliary("humanity_data")
    return aux.current if aux else 100


def get_max_humanity(ch):
    """Get character's maximum humanity"""
    aux = ch.getAuxiliary("humanity_data")
    return aux.maximum if aux else 100


def set_humanity(ch, value):
    """Set character's humanity to a specific value"""
    aux = ch.getAuxiliary("humanity_data")
    if not aux:
        return
    
    old_value = aux.current
    aux.current = max(0, min(aux.maximum, value))
    
    # Run hooks
    hooks.run("humanity_change", 
              hooks.build_info("ch int int", (ch, old_value, aux.current)))
    
    # Check thresholds
    check_humanity_thresholds(ch, old_value, aux.current)


def modify_humanity(ch, amount):
    """Modify character's humanity by an amount (positive or negative)"""
    aux = ch.getAuxiliary("humanity_data")
    if not aux:
        return 0
    
    old_value = aux.current
    aux.current = max(0, min(aux.maximum, aux.current + amount))
    actual_change = aux.current - old_value
    
    # Run hooks
    hooks.run("humanity_change",
              hooks.build_info("ch int int", (ch, old_value, aux.current)))
    
    # Check thresholds
    check_humanity_thresholds(ch, old_value, aux.current)
    
    return actual_change


def get_humanity_status(ch):
    """Get the humanity status category name"""
    humanity = get_humanity(ch)
    
    for status, data in HUMANITY_THRESHOLDS.items():
        if data["min"] <= humanity <= data["max"]:
            return status
    
    return "human"


def get_humanity_threshold_data(ch):
    """Get the threshold data for character's current humanity"""
    status = get_humanity_status(ch)
    return HUMANITY_THRESHOLDS.get(status, HUMANITY_THRESHOLDS["human"])


def get_social_modifier(ch):
    """Get the social check modifier based on humanity"""
    data = get_humanity_threshold_data(ch)
    return data["social_mod"]


def check_humanity_thresholds(ch, old_value, new_value):
    """Check if humanity crossed a threshold and apply effects"""
    old_status = None
    new_status = None
    
    for status, data in HUMANITY_THRESHOLDS.items():
        if data["min"] <= old_value <= data["max"]:
            old_status = status
        if data["min"] <= new_value <= data["max"]:
            new_status = status
    
    if old_status != new_status:
        # Crossed a threshold
        hooks.run("humanity_threshold_crossed",
                  hooks.build_info("ch str str", (ch, old_status or "human", new_status or "human")))
        
        # Notify character
        new_data = HUMANITY_THRESHOLDS.get(new_status, HUMANITY_THRESHOLDS["human"])
        if new_value < old_value:
            ch.send("{rYour humanity slips further away...{n")
            ch.send("{%sYou are now: %s{n" % (new_data["color"], new_status.replace("_", " ").title()))
            ch.send("{D%s{n" % new_data["description"])
        else:
            ch.send("{gYou feel more human...{n")
            ch.send("{%sYou are now: %s{n" % (new_data["color"], new_status.replace("_", " ").title()))
    
    # Check for cyberpsychosis
    if new_value <= 0:
        trigger_cyberpsychosis(ch)


################################################################################
# Cyberpsychosis System
################################################################################

def check_cyberpsychosis(ch):
    """
    Daily check for characters at risk of cyberpsychosis.
    Returns True if episode triggered.
    """
    aux = ch.getAuxiliary("humanity_data")
    if not aux:
        return False
    
    humanity = aux.current
    
    # Only check if in danger zone
    if humanity > 10:
        return False
    
    # DC = 15 - current_humanity
    dc = 15 - humanity
    
    # Roll 1d20 + COOL (we'll use a flat modifier for now)
    # TODO: Integrate with stats system
    roll = random.randint(1, 20)
    cool_mod = 0  # Will be replaced with actual COOL stat
    
    total = roll + cool_mod
    
    if total < dc:
        # Episode triggered
        trigger_episode(ch)
        return True
    
    return False


def trigger_episode(ch):
    """Trigger a cyberpsychosis episode"""
    aux = ch.getAuxiliary("humanity_data")
    if not aux:
        return
    
    # Roll severity
    severity_roll = random.randint(1, 6)
    episode_type, description = EPISODE_SEVERITY[severity_roll]
    
    aux.in_episode = True
    aux.episode_type = episode_type
    aux.episodes_total += 1
    
    # Run hook
    hooks.run("cyberpsychosis_episode",
              hooks.build_info("ch str", (ch, episode_type)))
    
    # Notify
    ch.send("")
    ch.send("{R!!! CYBERPSYCHOSIS EPISODE !!!{n")
    ch.send("{r%s{n" % description)
    ch.send("")
    
    # Different effects based on type
    if episode_type == "dissociation":
        ch.send("{DYou come to your senses, an hour of your life missing.{n")
        aux.in_episode = False
        aux.episode_type = None
        
    elif episode_type == "paranoia":
        ch.send("{rYou must escape! Everyone is against you!{n")
        # Combat/flee behavior would be handled by AI/combat system
        
    elif episode_type == "rage":
        ch.send("{RKILL THEM ALL{n")
        # Berserk behavior would be handled by combat system
        
    elif episode_type == "full_break":
        trigger_cyberpsychosis(ch)


def trigger_cyberpsychosis(ch):
    """Full cyberpsychosis - character becomes NPC"""
    aux = ch.getAuxiliary("humanity_data")
    if aux:
        aux.current = 0
        aux.in_episode = True
        aux.episode_type = "full_break"
    
    ch.send("")
    ch.send("{R========================================{n")
    ch.send("{R       TOTAL CYBERPSYCHOSIS{n")
    ch.send("{R========================================{n")
    ch.send("")
    ch.send("{rThe chrome has consumed what remained of your humanity.{n")
    ch.send("{rYou are no longer in control. The machine thinks for you now.{n")
    ch.send("")
    ch.send("{DThis character is now an NPC and can no longer be played.{n")
    ch.send("{DYou may create a new character or contact an admin.{n")
    
    # Run hook for game to handle (could kick player, etc.)
    hooks.run("cyberpsychosis_full", hooks.build_info("ch", (ch,)))


def end_episode(ch):
    """End an active cyberpsychosis episode"""
    aux = ch.getAuxiliary("humanity_data")
    if not aux or not aux.in_episode:
        return
    
    if aux.episode_type == "full_break":
        # Can't end a full break
        return
    
    aux.in_episode = False
    aux.episode_type = None
    
    ch.send("{gThe episode passes. You regain control.{n")
    hooks.run("cyberpsychosis_episode_end", hooks.build_info("ch", (ch,)))


################################################################################
# Recovery Systems
################################################################################

def do_therapy(ch):
    """
    Perform a therapy session to recover humanity.
    Returns (success: bool, message: str)
    """
    aux = ch.getAuxiliary("humanity_data")
    if not aux:
        return False, "No humanity data found"
    
    # Check if at max
    if aux.current >= aux.maximum:
        return False, "You are already at maximum humanity"
    
    # Check minimum humanity
    if aux.current < THERAPY_CONFIG["minimum_humanity_for_therapy"]:
        return False, "You are too far gone for therapy to help"
    
    # TODO: Check for time since last therapy
    # TODO: Check for money
    
    # Apply therapy
    old_humanity = aux.current
    aux.current = min(aux.maximum, aux.current + THERAPY_CONFIG["humanity_per_session"])
    aux.therapy_sessions += 1
    
    actual_gain = aux.current - old_humanity
    
    # Run hooks
    hooks.run("therapy_session", hooks.build_info("ch int", (ch, actual_gain)))
    
    return True, "Therapy session complete. Humanity +%d (now %d/%d)" % (
        actual_gain, aux.current, aux.maximum)


def recover_humanity_from_removal(ch, cyberware_id, quality):
    """
    Recover humanity from removing cyberware.
    Returns 50% of original humanity cost.
    """
    from .cyberware import get_cyberware_by_id
    
    cyber = get_cyberware_by_id(cyberware_id)
    if not cyber:
        return 0
    
    original_cost = cyber.get_humanity_cost(quality)
    recovery = original_cost // 2
    
    if recovery > 0:
        actual = modify_humanity(ch, recovery)
        return actual
    
    return 0


################################################################################
# Commands
################################################################################

def cmd_humanity(ch, cmd, arg):
    """Display detailed humanity status"""
    aux = ch.getAuxiliary("humanity_data")
    if not aux:
        ch.send("Error: No humanity data found.")
        return
    
    humanity = aux.current
    status = get_humanity_status(ch)
    data = HUMANITY_THRESHOLDS.get(status, HUMANITY_THRESHOLDS["human"])
    
    ch.send("{c=== Humanity Status ==={n")
    ch.send("")
    ch.send("{wCurrent Humanity:{n %d / %d" % (aux.current, aux.maximum))
    ch.send("")
    
    # Visual bar
    bar_width = 20
    filled = int((humanity / 100) * bar_width)
    bar = "{%s%s{D%s{n" % (
        data["color"],
        "=" * filled,
        "-" * (bar_width - filled)
    )
    ch.send("[%s] %d%%" % (bar, humanity))
    ch.send("")
    
    ch.send("{wStatus:{n {%s%s{n" % (data["color"], status.replace("_", " ").title()))
    ch.send("{wEffects:{n %s" % data["description"])
    ch.send("{wSocial Modifier:{n %+d" % data["social_mod"])
    ch.send("")
    
    # Statistics
    ch.send("{wTherapy Sessions:{n %d" % aux.therapy_sessions)
    ch.send("{wPsychosis Episodes:{n %d" % aux.episodes_total)
    
    if aux.in_episode:
        ch.send("")
        ch.send("{r!!! CURRENTLY IN EPISODE: %s !!!{n" % aux.episode_type.upper())
    
    # Thresholds reference
    ch.send("")
    ch.send("{c--- Humanity Thresholds ---{n")
    for name, info in sorted(HUMANITY_THRESHOLDS.items(), 
                             key=lambda x: -x[1]["max"]):
        if info["max"] > 0:
            indicator = " <-- YOU" if name == status else ""
            ch.send("{%s%3d-%3d: %s{n%s" % (
                info["color"], info["min"], info["max"],
                name.replace("_", " ").title(), indicator
            ))


def cmd_therapy(ch, cmd, arg):
    """Attempt a therapy session"""
    success, message = do_therapy(ch)
    ch.send(message)


################################################################################
# Heartbeat Hook
################################################################################

def humanity_heartbeat_hook(info):
    """Handle daily psychosis checks on heartbeat"""
    # This would need integration with the game's day/night cycle
    # For now, we'll just run occasional checks
    
    if not hasattr(humanity_heartbeat_hook, 'counter'):
        humanity_heartbeat_hook.counter = 0
    
    humanity_heartbeat_hook.counter += 1
    
    # Check every ~100 heartbeats (adjust based on game speed)
    if humanity_heartbeat_hook.counter < 100:
        return
    
    humanity_heartbeat_hook.counter = 0
    
    # Check all at-risk characters
    for ch in char.char_list():
        if ch.is_pc:
            aux = ch.getAuxiliary("humanity_data")
            if aux and aux.current <= 10 and not aux.in_episode:
                check_cyberpsychosis(ch)


################################################################################
# Initialization
################################################################################

def init_player_humanity(info):
    """Initialize humanity data for new characters"""
    ch, = hooks.parse_info(info)
    
    aux = ch.getAuxiliary("humanity_data")
    if aux:
        aux.current = 100
        aux.maximum = 100


# Install auxiliary data
auxiliary.install("humanity_data", HumanityAuxData, "character")

# Add hooks
hooks.add("init_player", init_player_humanity)
hooks.add("heartbeat", humanity_heartbeat_hook)

# Add commands
mudsys.add_cmd("humanity", None, cmd_humanity, "player", False)
mudsys.add_cmd("therapy", None, cmd_therapy, "player", False)


def __unload__():
    """Clean up when module is unloaded"""
    hooks.remove("init_player", init_player_humanity)
    hooks.remove("heartbeat", humanity_heartbeat_hook)
