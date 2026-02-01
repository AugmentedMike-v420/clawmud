---
layout: page
title: Zone Maps
---

<style>
.zone-section {
  margin: 3rem 0;
  padding: 1.5rem;
  background: linear-gradient(135deg, rgba(0,255,255,0.05) 0%, rgba(0,0,0,0.3) 100%);
  border: 1px solid rgba(0,255,255,0.2);
  border-radius: 8px;
}
.zone-section img, .zone-section object {
  width: 100%;
  max-width: 800px;
  display: block;
  margin: 1rem auto;
  border-radius: 4px;
}
.zone-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
  flex-wrap: wrap;
  gap: 1rem;
}
.zone-title {
  color: #0ff;
  font-size: 1.5rem;
  margin: 0;
  text-shadow: 0 0 10px rgba(0,255,255,0.5);
}
.status-badge {
  padding: 0.25rem 0.75rem;
  border-radius: 4px;
  font-size: 0.8rem;
  font-weight: bold;
}
.status-dev { background: rgba(255,200,0,0.2); color: #fc0; border: 1px solid #fc0; }
.status-soon { background: rgba(100,100,255,0.2); color: #88f; border: 1px solid #88f; }
.room-table {
  width: 100%;
  border-collapse: collapse;
  margin: 1rem 0;
  font-size: 0.9rem;
}
.room-table th, .room-table td {
  padding: 0.5rem;
  text-align: left;
  border-bottom: 1px solid rgba(0,255,255,0.2);
}
.room-table th {
  color: #0ff;
  font-weight: normal;
  text-transform: uppercase;
  font-size: 0.8rem;
}
.live { color: #0f8; }
.planned { color: #888; }
.locked { color: #f80; }
</style>

# Zone Maps

Explore the world being built. Maps show room connections and NPC locations.

---

<div class="zone-section">
  <div class="zone-header">
    <h2 class="zone-title">Neo Downtown — The Sprawl</h2>
    <span class="status-badge status-dev">In Development</span>
  </div>
  
  <object type="image/svg+xml" data="images/neo-downtown.svg" style="background:#0a0a0a;">
    <img src="images/neo-downtown.svg" alt="Neo Downtown Map">
  </object>
  
  <table class="room-table">
    <tr><th>Room</th><th>Status</th><th>NPCs</th></tr>
    <tr><td>rust_bucket</td><td class="live">✅ Live</td><td>Chrome</td></tr>
    <tr><td>street</td><td class="planned">🔨 Planned</td><td>—</td></tr>
    <tr><td>back_alley</td><td class="planned">🔨 Planned</td><td>Dealer, Lookout</td></tr>
    <tr><td>jack_point</td><td class="planned">🔨 Planned</td><td>Ghost</td></tr>
    <tr><td>back_booth</td><td class="planned">🔨 Planned</td><td>Static</td></tr>
    <tr><td>vip_lounge</td><td class="planned">🔨 Planned</td><td>Silk, Neon, Bouncer</td></tr>
    <tr><td>bar_counter</td><td class="planned">🔨 Planned</td><td>—</td></tr>
    <tr><td>storage_room</td><td class="locked">🔒 Hidden</td><td>—</td></tr>
    <tr><td>basement</td><td class="locked">🔒 Locked</td><td>Razor, Max</td></tr>
  </table>
  
  <p><a href="{{ '/lore/npcs/' | relative_url }}">View NPC Details →</a></p>
</div>

---

<div class="zone-section">
  <div class="zone-header">
    <h2 class="zone-title">Cyberspace</h2>
    <span class="status-badge status-soon">Coming Soon</span>
  </div>
  
  <object type="image/svg+xml" data="images/cyberspace.svg" style="background:#050510;">
    <img src="images/cyberspace.svg" alt="Cyberspace Map">
  </object>
  
  <table class="room-table">
    <tr><th>Node</th><th>Status</th><th>Description</th></tr>
    <tr><td>public_node</td><td class="planned">🔨 Planned</td><td>Entry point, jack in here</td></tr>
    <tr><td>data_haven</td><td class="planned">🔨 Planned</td><td>Safe storage, info trading</td></tr>
    <tr><td>corp_ice</td><td class="locked">🔒 ICE Protected</td><td>Corporate secrets, dangerous</td></tr>
    <tr><td>themed_zones</td><td class="planned">🔨 Planned</td><td>Immortal-built content</td></tr>
  </table>
</div>

---

## Legend

| Symbol | Meaning |
|--------|---------|
| `[Name]` | NPC present in room |
| Solid line | Normal connection |
| Dashed line | Hidden or locked passage |
| 🟢 Cyan | Accessible rooms |
| 🟠 Orange | Locked/hidden rooms |
| 🔴 Red | Dangerous (ICE) |
