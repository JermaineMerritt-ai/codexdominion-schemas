# Identity Architecture

**The Infrastructure Layer That Determines User Experience, Access, and Progression**

Identity is not decoration in CodexDominion—it is infrastructure. It determines how a person moves, what they receive, what they contribute, and how they grow inside the civilization.

---

## The Four Identities

### Diaspora - The Identity of Belonging
The global body of the Dominion representing the collective—the people, culture, and global family.

**Diaspora Receive:**
- Cultural continuity
- Economic elevation pathways
- Community belonging
- Narrative sovereignty

**Diaspora Contribute:**
- Stories and culture
- Participation and support
- Advocacy for youth and creators

### Youth - The Identity of Becoming
The inheritors of the Dominion. Youth are not "the future"—they are the present in training.

**Youth Receive:**
- Leadership development
- Curriculum and mentorship
- Identity progression
- Economic literacy
- Community belonging

**Youth Contribute:**
- Energy and creativity
- Leadership potential
- Cultural continuity

###Creator - The Identity of Building
The architects of culture, commerce, and innovation.

**Creators Receive:**
- Tools and dashboards
- Workflows and revenue pathways
- AI-powered systems
- Community support

**Creators Contribute:**
- Products and content
- Culture and economic growth
- Innovation and leadership

### Legacy-Builder - The Identity of Stewardship
Individuals who think generationally—parents, mentors, leaders, investors, elders, custodians of knowledge.

**Legacy-Builders Receive:**
- Stewardship frameworks
- Leadership pathways
- Governance roles
- Cultural authority

**Legacy-Builders Contribute:**
- Wisdom and stability
- Mentorship and resources
- Continuity

---

## Identity Cycles

Each identity moves through a cycle mirroring the Dominion's seasonal rhythm:

- **Dawn** - Vision
- **Day** - Action
- **Dusk** - Reflection
- **Night** - Renewal

This cycle applies to youth development, creator workflows, diaspora engagement, and leadership progression.

---

## Identity Progression Model

```
Diaspora → Youth (age-eligible) → Creator → Legacy-Builder → Council/Custodian
```

**Progression is based on:**
- Contribution
- Participation
- Leadership
- Mastery
- Stewardship

Identity is a journey, not a label.

---

## Identity-Aware Systems

Every system in the Dominion is identity-aware:
- Dashboards
- Workflows
- Curriculum
- Notifications
- Missions
- Economic tools
- Cultural content

**This means:**
- Youth see youth content
- Creators see creator tools
- Diaspora see cultural content
- Legacy-Builders see stewardship frameworks

Identity determines experience.

---

## The Identity Engine (2.0)

The operational core of the Dominion's personalization system.

### Identity Detection
- Registration and onboarding
- Self-selection
- Age-based logic
- Role-based logic

### Identity Routing
- Dashboard routing
- Curriculum routing
- Mission routing
- Content routing

### Identity Expansion
- Progression tracking
- Seasonal advancement
- Leadership pathways

### Identity Integration
- Connects to governance
- Connects to culture
- Connects to economics
- Connects to operations

The Identity Engine ensures every person receives the experience meant for them—no more, no less.

---

## Database Implementation

See [`schema.prisma`](../../schema.prisma) for the technical implementation:
- `User` model with `UserRole` relationships
- `RoleName` enum: YOUTH, YOUTH_CAPTAIN, AMBASSADOR, CREATOR, EDUCATOR, REGIONAL_DIRECTOR, COUNCIL, ADMIN
- `Profile` model with `risePath` (IDENTITY, MASTERY, CREATION, LEADERSHIP)
- Identity-based access control throughout the schema

---

**Related Documentation:**
- [Governance & Leadership](./GOVERNANCE_LEADERSHIP.md)
- [Youth Empire](./YOUTH_EMPIRE.md)
- [Creator Dominion](./CREATOR_DOMINION.md)
