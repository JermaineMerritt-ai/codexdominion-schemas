# Community Transition Kit

## Overview

The Community Transition Kit guides new members from discovery to active participation in the Dominion. It's the structured 7-day "Rise Path" for welcoming people into the Civilization Era.

## The Rise Path (7-Day Onboarding)

### Day 1-2: Identity Discovery

**Goal:** Understand who you are in the Dominion

**Activities:**
- Complete identity assessment
- Learn about the four identities (Youth, Creator, Diaspora, Legacy-Builder)
- Explore cultural foundations (Flame, Circle, Crown, Seasons)
- Read origin story

**Deliverables:**
- Identity confirmed
- Profile created
- First cultural story read

**Messages:**
- Welcome email with Dominion story
- Identity assessment link
- Cultural foundations video

### Day 3-4: Mission Overview

**Goal:** Understand how the Dominion operates

**Activities:**
- Learn about missions (what, why, how)
- Understand seasonal rhythm (Dawn, Day, Dusk, Night)
- Explore your identity-specific dashboard
- See sample mission

**Deliverables:**
- Seasonal rhythm understood
- Mission system clear
- Dashboard explored

**Messages:**
- Mission overview video
- Seasonal rhythm explainer
- Dashboard tour

### Day 5-6: Circle Joining

**Goal:** Connect with community

**Activities:**
- Join circle (Youth) or creator group
- Meet circle captain/leader
- Attend first gathering (or watch recording)
- Share first reflection

**Deliverables:**
- Circle joined
- Captain/leader met
- First gathering attended

**Messages:**
- Circle invitation
- Captain introduction
- Gathering schedule

### Day 7: Citizen's Oath

**Goal:** Commit to the Dominion

**Ritual:**
- Read and recite Citizen's Oath
- Mark commitment in system
- Receive welcome from community
- Start first mission

**Citizen's Oath:**
> "I rise with my identity. I honor my community. I carry the flame. I build with purpose. I walk with unity. I grow with the seasons. I am part of the Dominion."

**Deliverables:**
- Oath recited
- First mission assigned
- Full member status

**Messages:**
- Oath ceremony invitation
- Welcome from Council
- First mission assignment

## Orientation Experience

20-minute introduction covering story, identities, seasonal rhythm, and first steps.

### Structure

**Part 1: The Story (5 minutes)**
- Why the Dominion exists
- What we're building together
- Your place in the civilization

**Part 2: The Four Identities (5 minutes)**
- Diaspora: Belonging
- Youth: Becoming
- Creator: Building
- Legacy-Builder: Stewarding
- Which one are you?

**Part 3: The Seasonal Rhythm (5 minutes)**
- Dawn: Vision
- Day: Action
- Dusk: Reflection
- Night: Renewal
- How seasons shape everything

**Part 4: Your First Steps (5 minutes)**
- Complete profile
- Join circle
- Receive first mission
- Explore dashboard

### Delivery Formats

**Video Orientation:**
- Founder/Custodian speaking
- Visual storytelling
- Cultural symbols present
- Closed captions

**Interactive Walkthrough:**
- Step-by-step dashboard tour
- Click-through guide
- Tooltips and explanations
- Progress tracking

**Live Orientation:**
- Ambassador-led session
- Q&A opportunity
- Community connection
- Personal welcome

**Written Guide:**
- PDF or web page
- Illustrated with graphics
- Printable version
- Translation-ready

## Mission Structure

Missions follow a 4-week cycle aligned with seasonal rhythm.

### Week 1: Story + Lesson
**Focus:** Learn the context and principles

**Components:**
- Cultural story relevant to season
- Lesson explaining concepts
- Reflection prompts

**Deliverable:**
- Short written reflection (200-300 words)
- Answer: What did this story teach you?

### Week 2: Action
**Focus:** Apply the lesson

**Components:**
- Specific task or challenge
- Resources and tools provided
- Clear success criteria

**Deliverable:**
- Completed task (photo, video, document, or description)
- Evidence of action taken

### Week 3: Circle Dialogue
**Focus:** Share and learn from community

**Components:**
- Circle gathering focused on mission
- Peer sharing and feedback
- Captain guidance
- Group reflection

**Deliverable:**
- Attendance at gathering
- Contribution to discussion
- Peer feedback given

### Week 4: Showcase + Reflection
**Focus:** Celebrate and integrate learning

**Components:**
- Showcase work to circle
- Receive feedback
- Write final reflection
- Update portfolio

**Deliverable:**
- Final reflection (300-500 words)
- Portfolio updated
- Feedback received

## Identity-Specific Onboarding

### Youth Onboarding
**Focus:** Growth, learning, leadership development

**Unique Elements:**
- Simplified language
- Visual storytelling
- Interactive elements
- Circle captain introduction
- Parent/guardian resources

**First Mission:**
"Introduce yourself: Share your name, where you're from, and one thing you want to learn this season."

### Creator Onboarding
**Focus:** Tools, revenue, community

**Unique Elements:**
- Creator tools overview
- Revenue pathway explanation
- Product templates access
- Creator circle invitation

**First Mission:**
"Create and publish one artifact: Share something you've built with the community."

### Diaspora Onboarding
**Focus:** Cultural connection, global community

**Unique Elements:**
- Cultural heritage exploration
- Global network map
- Regional circle connection
- Diaspora stories

**First Mission:**
"Share your story: Tell us about your cultural heritage and what brought you to the Dominion."

### Legacy-Builder Onboarding
**Focus:** Stewardship, mentorship, continuity

**Unique Elements:**
- Leadership opportunities
- Mentorship pathways
- Governance introduction
- Council connection

**First Mission:**
"Mentor someone: Connect with one Youth or Creator and share one lesson you've learned."

## Support Systems

### Ambassador Support
- Ambassadors guide new members
- Answer questions
- Facilitate connections
- Monitor progress
- Celebrate milestones

### Circle Captain Support
- Captains welcome circle members
- Facilitate first gathering
- Review first mission submission
- Provide encouragement

### Peer Support
- Buddy system for new members
- Peer mentors assigned
- Community forum access
- Slack/Discord channels

### Resource Library
- Video tutorials
- Written guides
- FAQs
- Community stories
- Template library

## Transition Milestones

### Milestone 1: Identity Confirmed (Day 2)
- Profile complete
- Identity selected
- Cultural foundations understood

### Milestone 2: Circle Joined (Day 6)
- Circle membership active
- Captain/leader met
- First gathering attended

### Milestone 3: Citizen's Oath (Day 7)
- Oath recited
- Commitment made
- Full member status

### Milestone 4: First Mission Complete (Week 4)
- Mission submitted
- Feedback received
- Portfolio updated

### Milestone 5: Seasonal Completion (Month 3)
- 3 missions completed
- Circle participation consistent
- Seasonal reflection written

## Retention Strategies

### Week 1 Check-In
- Email: "How's your first week going?"
- Survey: Quick feedback on onboarding
- Support: Offer help if needed

### Week 2 Engagement
- Highlight: Showcase other members' work
- Challenge: Encourage mission submission
- Connection: Introduce to peer mentor

### Week 4 Celebration
- Recognize: First mission completed
- Reward: Badge or acknowledgment
- Invite: To next seasonal event

### Month 3 Review
- Assess: Progress and engagement
- Feedback: Gather insights
- Plan: Next season goals

## Off-Ramps (If Needed)

### Pause Membership
- Life circumstances change
- Can return anytime
- No judgment or penalty

### Alumni Status
- Remain connected to community
- Receive updates
- Access resources
- No active participation required

### Exit with Honor
- Thank member for participation
- Request feedback
- Leave door open
- Archive contributions

---

## Database Implementation

### User Status Tracking

```prisma
enum UserStatus {
  ACTIVE       // Full member
  ONBOARDING   // Days 1-7
  PAUSED       // Temporary break
  ALUMNI       // Former member, connected
  ARCHIVED     // Inactive
}
```

### Onboarding Progress

Track completion of Rise Path steps:
- Identity confirmed
- Circle joined
- Oath recited
- First mission submitted

## Phase 1 Implementation

### Included in Phase 1
✅ Basic registration and profile creation  
✅ Identity selection  
✅ Circle joining  
✅ First mission assignment

### Deferred to Phase 2+
❌ Full 7-day Rise Path automation  
❌ Orientation video production  
❌ Interactive walkthrough  
❌ Citizen's Oath ceremony system  
❌ Milestone tracking and badges  
❌ Retention automation  
❌ Peer mentor assignment

---

## References

- [Identity Architecture](IDENTITY_ARCHITECTURE.md) - Four identities explained
- [Youth Empire](YOUTH_EMPIRE.md) - Youth onboarding and missions
- [Creator Dominion](CREATOR_DOMINION.md) - Creator onboarding
- [Cultural Core](CULTURAL_CORE.md) - Citizen's Oath and rituals
- [Governance & Leadership](GOVERNANCE_LEADERSHIP.md) - Ambassador and captain roles
- [schema.prisma](../../schema.prisma) - User and profile models
