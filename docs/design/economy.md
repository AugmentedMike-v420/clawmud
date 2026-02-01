---
layout: page
title: Economy System Design
---

# ClawMUD Economy System

Eurodollars make the world go 'round. Chrome costs. Survival isn't free. In the sprawl, every eddie counts.

---

## Design Philosophy

1. **Scarcity is tension** — Money should always feel a little tight
2. **Multiple economies** — Legal, grey market, black market all coexist
3. **Chrome is expensive** — Cyberware is a major investment
4. **Risk/reward scales** — Dangerous jobs pay more
5. **Money sinks** — Rent, repairs, ammo, vices keep pressure on

---

## Currency

### Eurodollars (Eddies / €$)

The universal currency. Accepted everywhere from corp towers to street vendors.

| Denomination | Physical Form | Notes |
|--------------|---------------|-------|
| 1-99 | Coins | Pocket change |
| 100-999 | Bills | Daily transactions |
| 1,000+ | Credchips | Secure, traceable |
| 10,000+ | Encrypted transfer | Untraceable (for a fee) |

### Money Storage

| Method | Capacity | Risk | Notes |
|--------|----------|------|-------|
| On person | Unlimited | High (lootable on death) | Carried eddies |
| Bank account | Unlimited | Low (hackable) | 0.5% monthly fee |
| Hidden stash | 10,000 max | Medium (discoverable) | Location-based |
| Crypto wallet | Unlimited | Low (needs tech) | Untraceable, 2% fee |

---

## Income Sources

### Jobs (Primary Income)

Jobs scale with player level and risk:

| Job Tier | Level Range | Pay Range | Risk |
|----------|-------------|-----------|------|
| **Gutter** | 1-5 | 50-200 | Low |
| **Street** | 5-15 | 200-1,000 | Medium |
| **Professional** | 15-30 | 1,000-5,000 | High |
| **Elite** | 30-50 | 5,000-25,000 | Extreme |
| **Legendary** | 50+ | 25,000+ | Suicidal |

### Job Types

| Type | Description | Pay Modifier |
|------|-------------|--------------|
| **Delivery** | Move package A to B | ×0.8 |
| **Bounty** | Eliminate/capture target | ×1.2 |
| **Extraction** | Rescue/kidnap person | ×1.5 |
| **Data Theft** | Steal information | ×1.3 |
| **Protection** | Guard person/place | ×1.0 |
| **Sabotage** | Destroy/disable target | ×1.4 |

### Passive Income

| Source | Requirements | Income |
|--------|--------------|--------|
| **Investments** | 10,000+ eddies capital | 2-5% monthly |
| **Property** | Buy property | Rent from NPCs |
| **Business** | High reputation, capital | Variable |
| **Fixer network** | Fixer role, contacts | Finder's fees |

### Other Income

| Source | Typical Amount | Notes |
|--------|----------------|-------|
| Looting enemies | 10-100 per body | Risky, reputation hit |
| Selling gear | 50% of value | Fences pay 30% |
| Gambling | Variable | House always wins (mostly) |
| Hacking accounts | 100-10,000 | Very illegal, traced |
| Selling data | 200-5,000 | Need data first |

---

## Expenses (Money Sinks)

### Recurring Costs

| Expense | Frequency | Amount | Notes |
|---------|-----------|--------|-------|
| **Rent** | Weekly | 100-1,000 | Depends on district |
| **Food** | Daily | 10-50 | Can skip (penalties) |
| **Ammo** | Per use | 5-50/clip | Depends on weapon |
| **Medical** | As needed | 50-500 | Healing, stabilization |
| **Transport** | Per trip | 10-100 | Faster = more expensive |
| **Debt interest** | Weekly | 5-20% | Don't miss payments |

### Lifestyle Tiers

Lifestyle affects rest bonuses, social interactions, and random events:

| Lifestyle | Weekly Cost | Benefits |
|-----------|-------------|----------|
| **Street** | 0 | No rest bonus, -1 social, random danger |
| **Coffin** | 100 | Basic rest, neutral social |
| **Apartment** | 300 | Normal rest, stash space |
| **Condo** | 750 | +1 rest bonus, good stash |
| **Luxury** | 2,000 | +2 rest bonus, +1 social, secure |
| **Penthouse** | 5,000+ | Best bonuses, status symbol |

### One-Time Costs

| Item Category | Price Range |
|---------------|-------------|
| Weapons (basic) | 100-500 |
| Weapons (quality) | 500-5,000 |
| Weapons (military) | 5,000-50,000 |
| Armor (light) | 200-800 |
| Armor (medium) | 800-3,000 |
| Armor (heavy) | 3,000-15,000 |
| Cyberware (basic) | 500-2,000 |
| Cyberware (standard) | 2,000-10,000 |
| Cyberware (milspec) | 10,000-100,000 |
| Vehicles (basic) | 5,000-20,000 |
| Vehicles (combat) | 50,000+ |

---

## Markets

### Legal Market (Stores)

Licensed vendors with fixed prices and legal goods.

| Pros | Cons |
|------|------|
| Safe transactions | Marked up 20-50% |
| Warranty/support | No illegal goods |
| No reputation needed | Transactions traced |

### Grey Market (Fixers)

Semi-legal dealings through contacts.

| Pros | Cons |
|------|------|
| Better prices | Need reputation |
| Some restricted items | Unreliable availability |
| Less traced | Quality varies |

**Fixer Reputation Tiers:**

| Rep Level | Access | Price Modifier |
|-----------|--------|----------------|
| Unknown | Basic goods only | +20% |
| Known | Standard inventory | Normal |
| Trusted | Restricted items | -10% |
| Inner Circle | Rare/prototype | -20% |

### Black Market

Fully illegal, dangerous, high reward.

| Pros | Cons |
|------|------|
| Military grade weapons | Extreme risk |
| Rare cyberware | Scams common |
| Best prices (sometimes) | Violence possible |
| Completely untraceable | Need intro |

**Black Market Access:**
- Requires Streetwise 3+ OR Fixer contact
- Wrong move = death or worse
- Premium items appear randomly

---

## Ripperdoc Economy

Cyberware installation is a major economic sector.

### Installation Costs

| Doc Type | Install Fee | Quality Mod | Risk |
|----------|-------------|-------------|------|
| **Street Doc** | 50-200 | ×0.5 gear | 30% complication |
| **Clinic** | 200-1,000 | ×1.0 | 10% complication |
| **Hospital** | 1,000-5,000 | ×1.5 | 2% complication |
| **Black Clinic** | 500-2,000 | ×0.8 | 15% complication |
| **Exclusive** | 5,000-20,000 | ×2.0 | <1% complication |

### Sample Cyberware Prices

| Cyberware | Street | Standard | Corp | Milspec |
|-----------|--------|----------|------|---------|
| Neural Interface | 400 | 800 | 2,400 | 8,000 |
| Cybereyes (basic) | 600 | 1,200 | 3,600 | 12,000 |
| Reflex Booster | 1,500 | 3,000 | 9,000 | 30,000 |
| Mantis Blades | 2,500 | 5,000 | 15,000 | 50,000 |
| Sandevistan | 5,000 | 10,000 | 30,000 | 100,000 |
| Subdermal Armor | 1,000 | 2,000 | 6,000 | 20,000 |
| Full Cyberarm | 4,000 | 8,000 | 24,000 | 80,000 |

### Maintenance

Cyberware requires upkeep:

| Quality | Maintenance Interval | Cost |
|---------|---------------------|------|
| Street | Monthly | 5% of value |
| Standard | Quarterly | 3% of value |
| Corp | Yearly | 2% of value |
| Milspec | Rarely | 1% of value |

**Neglected Chrome:**
- Miss maintenance = malfunction chance
- 3 missed = major malfunction
- Repair costs 20% of value

---

## Weapons & Gear Economy

### Weapon Prices

| Category | Budget | Standard | Quality | Military |
|----------|--------|----------|---------|----------|
| Knife | 20 | 50 | 150 | 500 |
| Light Pistol | 100 | 250 | 750 | 2,500 |
| Heavy Pistol | 200 | 500 | 1,500 | 5,000 |
| SMG | 400 | 1,000 | 3,000 | 10,000 |
| Assault Rifle | 800 | 2,000 | 6,000 | 20,000 |
| Shotgun | 300 | 750 | 2,250 | 7,500 |
| Sniper Rifle | 1,500 | 3,750 | 11,250 | 37,500 |
| Heavy Weapon | 5,000 | 12,500 | 37,500 | 125,000 |

### Ammunition

| Type | Price per Clip | Notes |
|------|----------------|-------|
| Standard | 10 | Normal damage |
| Armor Piercing | 30 | -2 SP |
| Hollow Point | 25 | +1d6 vs unarmored |
| Incendiary | 50 | Fire damage |
| EMP | 75 | Disables electronics |
| Rubber | 15 | Non-lethal |

### Gear & Equipment

| Item | Price | Notes |
|------|-------|-------|
| Basic Toolkit | 200 | Required for repairs |
| Medkit | 100 | +4 to Medicine, 5 uses |
| Cyberdeck (basic) | 1,000 | Required for hacking |
| Cyberdeck (quality) | 5,000 | +2 to hacking |
| Bug Sweeper | 300 | Detect surveillance |
| Grapple Line | 150 | 30m rope with hook |
| Flashbang | 50 | Stun in 5m radius |
| Frag Grenade | 100 | 4d6 damage |
| EMP Grenade | 200 | Disables electronics 3 rounds |
| Combat Drug (Boost) | 150 | +2 REF for 1 hour |
| Stim Pack | 75 | Heal 2d6 immediately |

---

## Banking & Finance

### Bank Accounts

| Account Type | Monthly Fee | Features |
|--------------|-------------|----------|
| Basic | 0 | Storage only |
| Standard | 50 | Storage + transfers |
| Premium | 200 | Storage + investments + privacy |
| Offshore | 500 | Untraceable + multi-currency |

### Loans

Available from banks, fixers, or loan sharks:

| Source | Interest | Terms | Default Consequence |
|--------|----------|-------|---------------------|
| Bank | 5% monthly | Collateral required | Repossession |
| Fixer | 10% monthly | Reputation-based | Rep damage |
| Loan Shark | 20% weekly | None | Violence |

### Investments

| Type | Return | Risk | Min Investment |
|------|--------|------|----------------|
| Corp Bonds | 2% monthly | Low | 5,000 |
| Corp Stock | 1-10% monthly | Medium | 1,000 |
| Crypto | -50% to +100% | High | 100 |
| Real Estate | 3% monthly | Low | 50,000 |

---

## Economic Zones

Different areas have different economies:

| Zone | Price Modifier | Goods Available | Risk |
|------|----------------|-----------------|------|
| **Corp District** | +50% | Legal, quality | Low |
| **Downtown** | +20% | Legal, grey | Low |
| **Slums** | -20% | Grey, black | Medium |
| **Industrial** | -10% | Grey, bulk goods | Medium |
| **Underground** | -30% | Black market | High |
| **The Edge** | Variable | Anything, rare | Extreme |

---

## Faction Economy

Reputation with factions affects prices:

| Reputation | Price Modifier | Access |
|------------|----------------|--------|
| Hostile | +100% (if they'll deal) | Basic only |
| Unfriendly | +50% | Basic only |
| Neutral | Normal | Standard |
| Friendly | -10% | Standard + some restricted |
| Allied | -25% | Full inventory |
| Exalted | -40% | Everything + exclusives |

---

## Starting Economy (By Origin)

| Origin | Starting Eddies | Starting Debt | Total Net |
|--------|-----------------|---------------|-----------|
| Street Kid | 50 | 0 | +50 |
| Corp Exile | 200 | 5,000 | -4,800 |
| Combat Veteran | 100 | 2,000 | -1,900 |
| Tech Prodigy | 75 | 1,500 | -1,425 |
| Nomad | 80 | 1,000 | -920 |
| Media | 120 | 3,000 | -2,880 |

---

## Economy Balance Targets

### Early Game (Level 1-10)
- Income: 50-500 eddies/job
- Expenses: 150-500/week
- Target: Scraping by, making choices

### Mid Game (Level 11-30)
- Income: 500-5,000 eddies/job
- Expenses: 500-2,000/week
- Target: Stable but wanting more

### Late Game (Level 31-50)
- Income: 5,000-25,000 eddies/job
- Expenses: 2,000-10,000/week
- Target: Wealthy but always upgrading

### End Game (Level 50+)
- Income: Variable (investments, businesses)
- Expenses: 10,000+/week
- Target: Economic influence, not just survival

---

## Implementation

### Data Structures

```python
@dataclass
class Economy:
    base_prices: Dict[str, int]  # item_id -> base price
    zone_modifiers: Dict[str, float]  # zone_id -> multiplier
    faction_modifiers: Dict[str, Dict[str, float]]  # faction -> rep -> mult

@dataclass
class CharacterFinance:
    char_id: str
    eddies_on_hand: int
    bank_balance: int
    debts: List[Debt]
    investments: List[Investment]
    properties: List[Property]
    
@dataclass
class Debt:
    creditor: str  # NPC or faction ID
    principal: int
    interest_rate: float
    interest_period: str  # weekly, monthly
    next_payment: datetime
    consequences: str  # what happens on default

@dataclass
class Transaction:
    timestamp: datetime
    type: str  # purchase, sale, payment, income
    amount: int
    counterparty: str
    item: Optional[str]
    location: str
```

### Files to Create

- `src/economy.py` — Core economy system
- `src/banking.py` — Bank accounts, loans, investments
- `src/vendors.py` — Shop system, pricing
- `src/markets.py` — Grey/black market mechanics
- `data/prices.json` — Base price database
- `data/vendors.json` — Vendor inventories

### Commands

```
money                    — Show finances
buy <item> [from vendor] — Purchase item
sell <item> [to vendor]  — Sell item
bank [deposit/withdraw]  — Banking
debt                     — View debts
pay <creditor> <amount>  — Pay debt
invest <type> <amount>   — Make investment
```

---

## Integration Points

### Character Creation (CM-011)
- Starting eddies from origin
- Starting debt
- First contact (fixer, etc.)

### Cyberware (CM-010)
- Cyberware prices
- Installation costs
- Maintenance expenses

### Combat (CM-009)
- Loot drops
- Bounty payments
- Medical costs

### Jobs/Missions
- Job payouts
- Reputation rewards
- Faction standing changes

---

*Designed by Clawlord | ClawMUD Economy v1.0*
