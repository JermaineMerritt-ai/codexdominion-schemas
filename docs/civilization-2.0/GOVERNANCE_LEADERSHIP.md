# Governance & Leadership

## Overview

The Dominion operates on **stewardship-based governance** with seasonal rhythms rather than corporate calendars. Leadership is earned through contribution, cultural alignment, and service—not through domination.

## Leadership Structure

### The Council
Primary leadership body with representatives from each identity (Youth, Creator, Diaspora, Legacy-Builder)

**Responsibilities:**
- Upholds Constitution and cultural covenant
- Guides seasonal missions and identity progression
- Meets in alignment with seasonal cycles (Dawn/Day/Dusk/Night Council)

### The Custodian
Keeper of the flame, responsible for continuity and cultural coherence

**Role:**
- Narrative, cultural, and constitutional authority
- Guides Council through stewardship, not command
- Succession based on stewardship, mastery, contribution

### The Ambassadors
External-facing leaders who carry the Dominion's voice to communities

**Responsibilities:**
- Represent the Dominion publicly
- Teach curriculum
- Support circles
- Guide creators

### The Circles
Community units aligned by identity

**Types:**
- Youth Circles
- Creator Circles
- Diaspora Circles
- Legacy Circles

**Purpose:**
- Leadership development
- Curriculum delivery
- Community building

## Seasonal Governance Model

### Dawn (Vision)
- Set goals
- Define missions
- Align identity pathways

### Day (Action)
- Execute missions
- Run operations
- Support circles

### Dusk (Reflection)
- Review outcomes
- Gather insights
- Refine systems

### Night (Renewal)
- Reset
- Restore
- Prepare for next cycle

## Compliance & Audit Framework

Audits occur at end of each season, year, and major transitions:
- **Identity audits** - Ensure identity-aware systems function correctly
- **Curriculum audits** - Validate content quality and cultural alignment
- **Financial audits** - Ensure ethical stewardship and transparency
- **Cultural audits** - Assess ritual fidelity and symbol usage
- **Operational audits** - Check system health and workflow efficiency

## Leadership Roles (Operational Tier)

### Youth Captains
- Run Youth Circles
- Deliver curriculum
- Guide missions
- Track progression

### Regional Directors
- Oversee circles in geographic area
- Manage ambassadors
- Coordinate events
- Maintain quality standards

### Creator Leaders
- Lead creator circles
- Mentor emerging creators
- Build cultural assets

### Educators & Advisors
- Support curriculum delivery
- Guide youth/creators
- Uphold continuity

## Leadership Principles (Non-Negotiable)

1. **Stewardship over authority** - Guide, protect, elevate (not dominate)
2. **Identity before infrastructure** - Decisions must reinforce the four identities
3. **Culture as first technology** - Rituals, stories, symbols before tools
4. **Clarity over complexity** - Speak plainly, move intentionally
5. **Continuity over urgency** - Build for generations, not moments

## Leadership Ascension Path

```
Initiate (learn Constitution/culture)
    ↓
Steward (lead circles/missions)
    ↓
Architect (build systems)
    ↓
Director (oversee regions)
    ↓
Custodian-Track (long-term stewardship)
```

Progression based on:
- Contribution to community
- Leadership in circles/missions
- Cultural alignment
- System mastery
- Stewardship demonstrated

## Leadership Oath

> "I protect the flame. I uphold the culture. I guide with clarity. I build with excellence. I steward with humility. I serve the youth, creators, and diaspora. I move with the seasons. I honor the Dominion."

## Leadership Training Framework

Four-module mastery system ensures leaders can run circles, teach curriculum, and communicate with sovereignty.

### Module 1: Identity & Culture Training
- Four Identities deep dive
- Cultural Covenant study
- Seasonal Rhythm practice
- Symbol and ritual mastery

### Module 2: Mission & Curriculum Training
- Mission Engine mechanics
- Curriculum Map navigation
- Circle Facilitation skills
- Portfolio assessment methods

### Module 3: Communication & Brand Training
- Dominion Voice principles
- Brand Identity usage
- Public Representation guidelines
- Messaging consistency

### Module 4: Leadership Execution Training
- Weekly Rhythm management
- Reporting & Metrics
- Leadership Scenarios
- Crisis response

**Mastery Requirements:**
- Run one full circle/outreach event
- Complete one mission cycle
- Lead one cultural ritual
- Create one brand-aligned communication piece

## Leadership Ascension Ceremony

Ritual marking transition from participant to civilization-bearer.

**Purpose:**
- Unify leaders under one culture
- Anchor in stewardship
- Connect to lineage

**Structure:**
1. **Opening** - Flame lit, symbols displayed
2. **Story of Ascension** - Journey from initiate to leader
3. **Four Identities Invocation** - Honor each identity
4. **Seasonal Invocation** - Dawn, Day, Dusk, Night
5. **Leadership Charge** - Council speaks charge to new leaders
6. **Leadership Oath** - Spoken together by all
7. **Anointing of Roles** - Specific assignments given
8. **Passing of Flame** - Symbolic flame passed to new leaders
9. **Closing** - Circle closes with unity gesture

**Setting:**
- Circle formation
- Flame symbol (candle, projection, or fire pit)
- Dominion symbols visible
- Intentional environment (quiet, focused)

**Leadership Oath (Recited):**
> "I carry the flame. I rise in identity, mastery, creation, and leadership. I serve my community. I protect our unity. I build our dominion. I lead with culture, purpose, and sovereignty."

**Can be held:**
- Physical circles
- Digital gatherings
- Retreats
- Community spaces

---

## Database Implementation

### User Roles (from schema.prisma)

```prisma
enum UserRole {
  YOUTH
  YOUTH_CAPTAIN
  AMBASSADOR
  CREATOR
  EDUCATOR
  REGIONAL_DIRECTOR
  COUNCIL
  ADMIN
}
```

### Role-Based Access

Leadership roles determine system access:
- **YOUTH** - Circle members, mission participants
- **YOUTH_CAPTAIN** - Circle leadership, session management
- **AMBASSADOR** - Public outreach, school partnerships
- **CREATOR** - Artifact creation, challenge submissions
- **EDUCATOR** - Curriculum support, mentorship
- **REGIONAL_DIRECTOR** - Multi-circle oversight
- **COUNCIL** - Strategic governance, cultural authority
- **ADMIN** - System administration

---

## References

- [Identity Architecture](IDENTITY_ARCHITECTURE.md) - Foundation for leadership roles
- [Cultural Core](CULTURAL_CORE.md) - Symbols and rituals used in ceremonies
- [Operational Engine](OPERATIONAL_ENGINE.md) - Systems leaders manage
- [schema.prisma](../../schema.prisma) - User and role data models
