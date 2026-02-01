"""
ClawMUD Cyberware System - Core Module

Handles cyberware data structures, catalog loading, slot management,
and character cyberware auxiliary data.
"""
import mud, mudsys, auxiliary, storage, hooks, char
import json
import os
import random

################################################################################
# Constants
################################################################################

# Body slot definitions: location -> max slots
BODY_SLOTS = {
    "neural": 3,
    "ocular": 2,
    "audio": 2,
    "arm_l": 2,
    "arm_r": 2,
    "leg_l": 2,
    "leg_r": 2,
    "torso": 4,
    "circulatory": 2,
    "skin": 2,
}

# Quality tier modifiers
QUALITY_TIERS = {
    "street": {
        "humanity_mult": 1.5,
        "install_dc": 10,
        "price_mult": 0.5,
        "availability": "common",
    },
    "standard": {
        "humanity_mult": 1.0,
        "install_dc": 15,
        "price_mult": 1.0,
        "availability": "normal",
    },
    "corp": {
        "humanity_mult": 0.75,
        "install_dc": 18,
        "price_mult": 3.0,
        "availability": "licensed",
    },
    "milspec": {
        "humanity_mult": 0.5,
        "install_dc": 22,
        "price_mult": 10.0,
        "availability": "black_market",
    },
    "prototype": {
        "humanity_mult": 0.25,
        "install_dc": 25,
        "price_mult": 25.0,
        "availability": "unique",
    },
}

################################################################################
# Global Data
################################################################################

# Loaded cyberware catalog
_cyberware_catalog = {}
_catalog_loaded = False

################################################################################
# Cyberware Data Class
################################################################################

class Cyberware:
    """Represents a cyberware item from the catalog"""
    
    def __init__(self, data=None):
        if data:
            self.id = data.get("id", "")
            self.name = data.get("name", "Unknown Cyberware")
            self.slot_location = data.get("slot_location", "torso")
            self.slots_required = data.get("slots_required", 1)
            self.humanity_cost = data.get("humanity_cost", 5)
            self.base_install_dc = data.get("install_dc", 15)
            self.base_price = data.get("price", 1000)
            self.effects = data.get("effects", [])
            self.description = data.get("description", "")
            self.requires = data.get("requires", None)  # Required cyberware ID
            self.category = data.get("category", "general")
        else:
            self.id = ""
            self.name = "Unknown"
            self.slot_location = "torso"
            self.slots_required = 1
            self.humanity_cost = 5
            self.base_install_dc = 15
            self.base_price = 1000
            self.effects = []
            self.description = ""
            self.requires = None
            self.category = "general"
    
    def get_humanity_cost(self, quality="standard"):
        """Get humanity cost adjusted for quality tier"""
        tier = QUALITY_TIERS.get(quality, QUALITY_TIERS["standard"])
        return int(self.humanity_cost * tier["humanity_mult"])
    
    def get_install_dc(self, quality="standard"):
        """Get installation DC adjusted for quality tier"""
        tier = QUALITY_TIERS.get(quality, QUALITY_TIERS["standard"])
        return tier["install_dc"]
    
    def get_price(self, quality="standard"):
        """Get price adjusted for quality tier"""
        tier = QUALITY_TIERS.get(quality, QUALITY_TIERS["standard"])
        return int(self.base_price * tier["price_mult"])


class InstalledCyberware:
    """Represents an installed piece of cyberware on a character"""
    
    def __init__(self, cyberware_id="", quality="standard", functional=True, 
                 complication=None, set=None):
        if set is not None:
            self.read(set)
        else:
            self.cyberware_id = cyberware_id
            self.quality = quality
            self.functional = functional  # Can be reduced by bad install
            self.complication = complication  # Any ongoing complication
            self.install_time = 0  # When it was installed (game time)
    
    def store(self):
        """Store to storage set"""
        s = storage.StorageSet()
        s.storeString("cyberware_id", self.cyberware_id)
        s.storeString("quality", self.quality)
        s.storeBool("functional", self.functional)
        s.storeString("complication", self.complication or "")
        s.storeInt("install_time", self.install_time)
        return s
    
    def read(self, set):
        """Read from storage set"""
        self.cyberware_id = set.readString("cyberware_id") if set.contains("cyberware_id") else ""
        self.quality = set.readString("quality") if set.contains("quality") else "standard"
        self.functional = set.readBool("functional") if set.contains("functional") else True
        complication = set.readString("complication") if set.contains("complication") else ""
        self.complication = complication if complication else None
        self.install_time = set.readInt("install_time") if set.contains("install_time") else 0
    
    def get_cyberware(self):
        """Get the Cyberware object from catalog"""
        return get_cyberware_by_id(self.cyberware_id)


################################################################################
# Character Auxiliary Data
################################################################################

class CyberwareAuxData:
    """Holds character cyberware data - installed chrome, slots, etc."""
    
    def __init__(self, set=None):
        # Installed cyberware list
        self.installed = []
        
        # Slots used per location
        self.slots_used = {loc: 0 for loc in BODY_SLOTS}
        
        # Read from storage if provided
        if set is not None:
            self.read(set)
    
    def copyTo(self, to):
        """Copy cyberware data to another instance"""
        to.installed = [InstalledCyberware(
            i.cyberware_id, i.quality, i.functional, i.complication
        ) for i in self.installed]
        to.slots_used = dict(self.slots_used)
    
    def copy(self):
        """Create a copy of this cyberware data"""
        newdata = CyberwareAuxData()
        self.copyTo(newdata)
        return newdata
    
    def store(self):
        """Store cyberware data to a storage set"""
        set = storage.StorageSet()
        
        # Store installed cyberware
        installed_list = storage.StorageList()
        for installed in self.installed:
            installed_list.add(installed.store())
        set.storeList("installed", installed_list)
        
        # Store slots used
        slots_set = storage.StorageSet()
        for loc, used in self.slots_used.items():
            slots_set.storeInt(loc, used)
        set.storeSet("slots_used", slots_set)
        
        return set
    
    def read(self, set):
        """Read cyberware data from a storage set"""
        # Read installed cyberware
        if set.contains("installed"):
            installed_list = set.readList("installed")
            self.installed = []
            for item_set in installed_list.sets():
                self.installed.append(InstalledCyberware(set=item_set))
        
        # Read slots used
        if set.contains("slots_used"):
            slots_set = set.readSet("slots_used")
            for loc in BODY_SLOTS:
                if slots_set.contains(loc):
                    self.slots_used[loc] = slots_set.readInt(loc)
    
    def get_available_slots(self, location):
        """Get number of available slots for a location"""
        max_slots = BODY_SLOTS.get(location, 0)
        used = self.slots_used.get(location, 0)
        return max_slots - used
    
    def has_cyberware(self, cyberware_id):
        """Check if character has specific cyberware installed"""
        return any(i.cyberware_id == cyberware_id for i in self.installed)
    
    def get_installed_by_location(self, location):
        """Get all installed cyberware in a specific location"""
        result = []
        for installed in self.installed:
            cyber = installed.get_cyberware()
            if cyber and cyber.slot_location == location:
                result.append(installed)
        return result
    
    def recalculate_slots(self):
        """Recalculate slots used based on installed cyberware"""
        self.slots_used = {loc: 0 for loc in BODY_SLOTS}
        for installed in self.installed:
            cyber = installed.get_cyberware()
            if cyber:
                loc = cyber.slot_location
                if loc in self.slots_used:
                    self.slots_used[loc] += cyber.slots_required


################################################################################
# Catalog Management
################################################################################

def load_cyberware_catalog():
    """Load cyberware catalog from JSON file"""
    global _cyberware_catalog, _catalog_loaded
    
    catalog_path = "misc/cyberware"
    
    if not os.path.exists(catalog_path):
        mud.log_string("Cyberware catalog not found at: " + catalog_path)
        _catalog_loaded = True
        return
    
    try:
        with open(catalog_path, 'r') as f:
            data = json.load(f)
        
        _cyberware_catalog = {}
        for item_data in data.get("cyberware", []):
            cyber = Cyberware(item_data)
            _cyberware_catalog[cyber.id] = cyber
        
        mud.log_string("Loaded %d cyberware items" % len(_cyberware_catalog))
        _catalog_loaded = True
        
    except Exception as e:
        mud.log_string("Error loading cyberware catalog: " + str(e))
        _catalog_loaded = True


def get_cyberware_catalog():
    """Get the full cyberware catalog"""
    if not _catalog_loaded:
        load_cyberware_catalog()
    return _cyberware_catalog


def get_cyberware_by_id(cyberware_id):
    """Get a specific cyberware by ID"""
    catalog = get_cyberware_catalog()
    return catalog.get(cyberware_id)


def get_cyberware_by_slot(slot_location):
    """Get all cyberware that fits in a specific slot"""
    catalog = get_cyberware_catalog()
    return [c for c in catalog.values() if c.slot_location == slot_location]


def get_cyberware_by_category(category):
    """Get all cyberware in a specific category"""
    catalog = get_cyberware_catalog()
    return [c for c in catalog.values() if c.category == category]


################################################################################
# Character Cyberware Functions
################################################################################

def get_installed_cyberware(ch):
    """Get list of installed cyberware for a character"""
    aux = ch.getAuxiliary("cyberware_data")
    return aux.installed if aux else []


def can_install_cyberware(ch, cyberware_id, quality="standard"):
    """
    Check if cyberware can be installed on character.
    Returns (can_install: bool, reason: str)
    """
    from .humanity import get_humanity
    
    cyber = get_cyberware_by_id(cyberware_id)
    if not cyber:
        return False, "Unknown cyberware: %s" % cyberware_id
    
    aux = ch.getAuxiliary("cyberware_data")
    if not aux:
        return False, "Character has no cyberware data"
    
    # Check if already installed
    if aux.has_cyberware(cyberware_id):
        return False, "Already have %s installed" % cyber.name
    
    # Check for required cyberware
    if cyber.requires:
        if not aux.has_cyberware(cyber.requires):
            req_cyber = get_cyberware_by_id(cyber.requires)
            req_name = req_cyber.name if req_cyber else cyber.requires
            return False, "Requires %s to be installed first" % req_name
    
    # Check slot availability
    available = aux.get_available_slots(cyber.slot_location)
    if cyber.slots_required > available:
        return False, "Not enough %s slots (need %d, have %d)" % (
            cyber.slot_location, cyber.slots_required, available)
    
    # Check humanity
    humanity_cost = cyber.get_humanity_cost(quality)
    current_humanity = get_humanity(ch)
    if current_humanity - humanity_cost < 0:
        return False, "Not enough humanity (need %d, have %d)" % (
            humanity_cost, current_humanity)
    
    return True, "Can install"


################################################################################
# Effect Application
################################################################################

def apply_cyberware_effects(ch, installed):
    """Apply effects from installed cyberware to character"""
    cyber = installed.get_cyberware()
    if not cyber or not installed.functional:
        return
    
    # Run hook for custom effect handling
    hooks.run("cyberware_apply_effects", 
              hooks.build_info("ch obj", (ch, installed)))
    
    # Effects are defined in JSON and handled by other systems
    # This just runs the hook so combat, skills, etc. can respond


def remove_cyberware_effects(ch, installed):
    """Remove effects from cyberware being removed"""
    cyber = installed.get_cyberware()
    if not cyber:
        return
    
    # Run hook for custom effect removal
    hooks.run("cyberware_remove_effects",
              hooks.build_info("ch obj", (ch, installed)))


################################################################################
# Commands
################################################################################

def cmd_chrome(ch, cmd, arg):
    """Display character's installed cyberware"""
    aux = ch.getAuxiliary("cyberware_data")
    if not aux:
        ch.send("Error: No cyberware data found.")
        return
    
    from .humanity import get_humanity, get_humanity_status
    
    # Header
    ch.send("{c=== Your Chrome ==={n")
    ch.send("")
    
    # Humanity status
    humanity = get_humanity(ch)
    status = get_humanity_status(ch)
    ch.send("{WHumanity:{n %d/100 [{%s%s{n]" % (
        humanity,
        "g" if humanity > 70 else "y" if humanity > 40 else "r",
        status
    ))
    ch.send("")
    
    if not aux.installed:
        ch.send("No cyberware installed. You're still meat.")
        return
    
    # Group by location
    by_location = {}
    for installed in aux.installed:
        cyber = installed.get_cyberware()
        if cyber:
            loc = cyber.slot_location
            if loc not in by_location:
                by_location[loc] = []
            by_location[loc].append((cyber, installed))
    
    # Display by location
    for loc in BODY_SLOTS:
        if loc in by_location:
            max_slots = BODY_SLOTS[loc]
            used_slots = aux.slots_used.get(loc, 0)
            ch.send("{Y%s{n [%d/%d slots]:" % (loc.upper().replace("_", " "), used_slots, max_slots))
            
            for cyber, installed in by_location[loc]:
                status_icon = "{g*{n" if installed.functional else "{r!{n"
                quality_color = {
                    "street": "D", "standard": "w", "corp": "c", 
                    "milspec": "y", "prototype": "m"
                }.get(installed.quality, "w")
                
                ch.send("  %s {%s%s{n ({%s%s{n)" % (
                    status_icon, "w", cyber.name,
                    quality_color, installed.quality
                ))
                
                if installed.complication:
                    ch.send("      {r[%s]{n" % installed.complication)
            ch.send("")
    
    # Show available slots
    ch.send("{c--- Available Slots ---{n")
    for loc, max_slots in BODY_SLOTS.items():
        used = aux.slots_used.get(loc, 0)
        avail = max_slots - used
        if avail > 0:
            ch.send("  %s: %d/%d" % (loc.replace("_", " ").title(), avail, max_slots))


def cmd_cyberware(ch, cmd, arg):
    """Browse available cyberware catalog"""
    catalog = get_cyberware_catalog()
    
    if not catalog:
        ch.send("No cyberware catalog loaded.")
        return
    
    args = arg.split() if arg else []
    
    # Show specific item
    if args and args[0].lower() not in ["neural", "ocular", "audio", "arm", "leg", 
                                         "torso", "circulatory", "skin"]:
        # Try to find by ID or name
        search = " ".join(args).lower()
        found = None
        for cyber in catalog.values():
            if cyber.id.lower() == search or cyber.name.lower() == search:
                found = cyber
                break
        
        if found:
            show_cyberware_details(ch, found)
        else:
            ch.send("Unknown cyberware: %s" % search)
        return
    
    # Filter by category/location
    filter_loc = None
    if args:
        filter_loc = args[0].lower()
        # Handle arm/leg without side
        if filter_loc == "arm":
            filter_loc = "arm_l"  # Will match both
        elif filter_loc == "leg":
            filter_loc = "leg_l"
    
    ch.send("{c=== Cyberware Catalog ==={n")
    ch.send("Use 'cyberware <name>' for details")
    ch.send("")
    
    # Group by category
    categories = {}
    for cyber in catalog.values():
        cat = cyber.category
        if filter_loc:
            loc = cyber.slot_location
            # Handle arm/leg matching
            if filter_loc.startswith("arm") and not loc.startswith("arm"):
                continue
            if filter_loc.startswith("leg") and not loc.startswith("leg"):
                continue
            if not filter_loc.startswith("arm") and not filter_loc.startswith("leg"):
                if loc != filter_loc:
                    continue
        
        if cat not in categories:
            categories[cat] = []
        categories[cat].append(cyber)
    
    for cat in sorted(categories.keys()):
        ch.send("{Y%s Cyberware:{n" % cat.title())
        for cyber in sorted(categories[cat], key=lambda c: c.name):
            ch.send("  {w%s{n - %s (HU: %d, Slots: %d)" % (
                cyber.name, cyber.slot_location, 
                cyber.humanity_cost, cyber.slots_required
            ))
        ch.send("")


def show_cyberware_details(ch, cyber):
    """Show detailed info about a specific cyberware"""
    ch.send("{c=== %s ==={n" % cyber.name)
    ch.send("")
    ch.send("{wLocation:{n %s" % cyber.slot_location)
    ch.send("{wSlots:{n %d" % cyber.slots_required)
    ch.send("{wBase Humanity Cost:{n %d" % cyber.humanity_cost)
    ch.send("{wBase Price:{n %d eb" % cyber.base_price)
    
    if cyber.requires:
        req = get_cyberware_by_id(cyber.requires)
        req_name = req.name if req else cyber.requires
        ch.send("{wRequires:{n %s" % req_name)
    
    ch.send("")
    ch.send("{wDescription:{n")
    ch.send("  %s" % cyber.description)
    
    if cyber.effects:
        ch.send("")
        ch.send("{wEffects:{n")
        for effect in cyber.effects:
            ch.send("  - %s" % effect)
    
    ch.send("")
    ch.send("{wQuality Pricing:{n")
    for quality in ["street", "standard", "corp", "milspec", "prototype"]:
        hu = cyber.get_humanity_cost(quality)
        price = cyber.get_price(quality)
        ch.send("  %s: %d HU, %d eb" % (quality.title(), hu, price))


################################################################################
# Initialization
################################################################################

def init_player_cyberware(info):
    """Initialize cyberware data for new characters"""
    ch, = hooks.parse_info(info)
    
    # Cyberware aux is already initialized with defaults
    # This hook is for any special initialization logic
    pass


# Install auxiliary data
auxiliary.install("cyberware_data", CyberwareAuxData, "character")

# Load catalog
load_cyberware_catalog()

# Add hooks
hooks.add("init_player", init_player_cyberware)

# Add commands
mudsys.add_cmd("chrome", None, cmd_chrome, "player", False)
mudsys.add_cmd("cyberware", None, cmd_cyberware, "player", False)


def __unload__():
    """Clean up when module is unloaded"""
    hooks.remove("init_player", init_player_cyberware)
