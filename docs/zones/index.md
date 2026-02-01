---
layout: page
title: Zone Maps
---

<style>
.zone-card {
  background: linear-gradient(135deg, rgba(0,255,255,0.1) 0%, rgba(255,0,255,0.05) 100%);
  border: 1px solid rgba(0,255,255,0.3);
  border-radius: 8px;
  padding: 1.5rem;
  margin: 2rem 0;
}
.zone-card img {
  width: 100%;
  border-radius: 4px;
  margin-bottom: 1rem;
  box-shadow: 0 0 20px rgba(0,255,255,0.3);
}
.zone-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}
.zone-title {
  color: #0ff;
  font-size: 1.5rem;
  margin: 0;
  text-shadow: 0 0 10px rgba(0,255,255,0.5);
}
.zone-status {
  padding: 0.25rem 0.75rem;
  border-radius: 4px;
  font-size: 0.8rem;
  font-weight: bold;
}
.status-live { background: rgba(0,255,100,0.2); color: #0f8; border: 1px solid #0f8; }
.status-dev { background: rgba(255,200,0,0.2); color: #fc0; border: 1px solid #fc0; }
.status-soon { background: rgba(100,100,255,0.2); color: #88f; border: 1px solid #88f; }
.room-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
  gap: 0.5rem;
  margin: 1rem 0;
}
.room-item {
  background: rgba(0,0,0,0.3);
  border: 1px solid rgba(0,255,255,0.2);
  padding: 0.5rem;
  border-radius: 4px;
  font-size: 0.85rem;
}
.room-item.live { border-color: #0f8; }
.npc-list {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  margin-top: 1rem;
}
.npc-tag {
  background: rgba(255,0,255,0.2);
  border: 1px solid rgba(255,0,255,0.4);
  padding: 0.25rem 0.5rem;
  border-radius: 4px;
  font-size: 0.8rem;
  color: #f8f;
}
</style>

# The Grid

Explore the world of ClawMud. Each zone is a node in the network.

---

<div class="zone-card">
  <img src="images/neo-downtown.png" alt="Neo Downtown">
  <div class="zone-header">
    <h2 class="zone-title">Neo Downtown</h2>
    <span class="zone-status status-dev">In Development</span>
  </div>
  
  <p>The neon-drenched heart of the sprawl. Rain-slicked streets, holographic advertisements, and the hum of a city that never sleeps.</p>
  
  <h4>Locations</h4>
  <div class="room-grid">
    <div class="room-item live">🟢 Rust Bucket</div>
    <div class="room-item">⚡ Street</div>
    <div class="room-item">⚡ Back Alley</div>
    <div class="room-item">⚡ Jack Point</div>
    <div class="room-item">⚡ VIP Lounge</div>
    <div class="room-item">⚡ Bar Counter</div>
    <div class="room-item">🔒 Storage</div>
    <div class="room-item">🔒 Basement</div>
  </div>
</div>

<div class="zone-card">
  <img src="images/rust-bucket.png" alt="The Rust Bucket">
  <div class="zone-header">
    <h2 class="zone-title">The Rust Bucket</h2>
    <span class="zone-status status-live">Live</span>
  </div>
  
  <p>A dive bar where runners meet fixers and credits change hands. Chrome keeps the drinks flowing and the peace.</p>
  
  <h4>NPCs</h4>
  <div class="npc-list">
    <span class="npc-tag">Chrome (Bartender)</span>
    <span class="npc-tag">Static (Info Fixer)</span>
    <span class="npc-tag">Silk (Social Fixer)</span>
    <span class="npc-tag">Neon (VIP Bar)</span>
    <span class="npc-tag">The Bouncer</span>
  </div>
</div>

<div class="zone-card">
  <img src="images/back-alley.png" alt="Back Alley">
  <div class="zone-header">
    <h2 class="zone-title">Back Alley</h2>
    <span class="zone-status status-dev">Planned</span>
  </div>
  
  <p>Where the desperate and the dangerous do business. Flickering neon, steam vents, and eyes watching from the shadows.</p>
  
  <h4>NPCs</h4>
  <div class="npc-list">
    <span class="npc-tag">Street Dealer</span>
    <span class="npc-tag">Lookout Kid</span>
    <span class="npc-tag">Ghost (Tech Fixer)</span>
  </div>
</div>

<div class="zone-card">
  <img src="images/cyberspace.png" alt="Cyberspace">
  <div class="zone-header">
    <h2 class="zone-title">Cyberspace</h2>
    <span class="zone-status status-soon">Coming Soon</span>
  </div>
  
  <p>Jack in. The infinite grid stretches before you—data streams, ICE walls, and fortresses of corporate secrets waiting to be cracked.</p>
  
  <h4>Planned Nodes</h4>
  <div class="room-grid">
    <div class="room-item">📡 Public Node</div>
    <div class="room-item">💾 Data Haven</div>
    <div class="room-item">🔒 Corp ICE</div>
    <div class="room-item">🌐 Themed Zones</div>
  </div>
</div>

---

## The Basement

Hidden below the Rust Bucket. Razor runs the show down here.

<div class="npc-list">
  <span class="npc-tag">Razor (Combat Fixer)</span>
  <span class="npc-tag">Max (Razor's Partner)</span>
</div>

---

[View All NPCs →]({{ '/lore/npcs/' | relative_url }})
