# Content Governance System

**Version:** 1.0  
**Last Updated:** December 24, 2025  
**Status:** Active  

## Purpose

This document defines how we maintain consistent voice, components, and content as the CodexDominion platform grows. It ensures every word on the platform aligns with our brand promise and serves our community.

---

## 1. ROLES & RESPONSIBILITIES

### Content Owner
**Primary:** You (Founder) or designated PM  
**Responsibilities:**
- Approves all public copy changes
- Ensures brand voice consistency
- Final say on messaging alignment
- Guards cultural authenticity

### Design Owner
**Primary:** Creative Director  
**Responsibilities:**
- Ensures design system cohesion
- Validates copy fits within layouts
- Maintains visual-content harmony
- Approves component state variations

### Tech Owner
**Primary:** Engineering Lead  
**Responsibilities:**
- Ensures implementation feasibility
- Validates string lengths for UI
- Checks i18n compatibility
- Reviews technical accuracy

**Note:** In early stages, one person may wear multiple hats. The roles still apply.

---

## 2. SINGLE SOURCE OF TRUTH

### Content Repository Structure

```
content-library/
├── pages/
│   ├── homepage/
│   │   ├── hero-section.md
│   │   ├── creator-section.md
│   │   └── youth-section.md
│   ├── marketplace/
│   ├── leaderboard/
│   └── onboarding/
├── components/
│   ├── buttons/
│   ├── forms/
│   ├── cards/
│   └── tooltips/
├── system-messages/
│   ├── errors.md
│   ├── success-toasts.md
│   ├── validation-messages.md
│   └── tooltips.md
└── templates/
    ├── email-sequences/
    ├── sms-flows/
    └── social-content/
```

### Content Block Format

Each content file uses this structure:

```markdown
## [Component Name]

**Context:** Where/when this appears  
**Audience:** Who sees this  
**Version:** 1.0  
**Date:** 2025-12-24  

### Primary Copy
[Main text]

### States
- **Default:** [Text]
- **Hover:** [Text]
- **Loading:** [Text]
- **Success:** [Text]
- **Error:** [Text]

### Character Limits
- Desktop: 120 chars
- Mobile: 80 chars

### Accessibility
- Screen reader text: [Text]
- ARIA label: [Text]

### Notes
[Any context for future maintainers]
```

---

## 3. CHANGE PROCESS

### Step 1: PROPOSE

**Who:** Anyone on the team  
**Action:**
1. Identify need for change (new feature, tweak, bug fix)
2. Log in "Content Changes" board (Notion/Confluence/GitHub Issues)
3. Include:
   - Current copy (if updating existing)
   - Reason for change
   - Affected pages/components
   - Priority (P0-critical, P1-high, P2-medium, P3-low)

**Template:**
```
Title: [Component] - [Brief Description]
Priority: P1
Affected Pages: Homepage Hero, Marketplace CTA
Current Copy: "Join the movement"
Proposed Copy: "Start earning today"
Reason: More direct CTA, better conversion hypothesis
Requestor: @username
Date: 2025-12-24
```

### Step 2: DRAFT

**Who:** Content Owner or designated writer  
**Action:**
1. Write draft using established tone (see Brand Voice)
2. Link to affected page/component in design system
3. Check against content rules:
   - ✅ Short sentences
   - ✅ Clear CTA
   - ✅ No jargon
   - ✅ Human tone
   - ✅ Culturally grounded
4. Add to "Draft" column in board

### Step 3: REVIEW

**Who:** Content Owner + Design Owner + Tech Owner  
**Action:**

**Content Owner:**
- ✅ Clarity and brand alignment
- ✅ Voice consistency
- ✅ Cultural authenticity
- ✅ Messaging hierarchy

**Design Owner:**
- ✅ Layout impact (does it fit?)
- ✅ Character count within limits
- ✅ Visual-content harmony
- ✅ Responsive behavior

**Tech Owner:**
- ✅ Implementation feasibility
- ✅ String length constraints
- ✅ i18n considerations
- ✅ API/data availability

**Review Criteria:**
- [ ] Aligns with brand voice
- [ ] Fits within layout constraints
- [ ] Technically feasible
- [ ] Accessible (WCAG 2.1 AA)
- [ ] No blockers

### Step 4: APPROVE

**Who:** Content Owner (final authority)  
**Action:**
1. Mark as "Approved" in board
2. Add version tag + date
3. Move to "Approved" section in content library
4. Update version history

**Approval Format:**
```
Status: Approved ✅
Version: 1.1
Date Approved: 2025-12-24
Approved By: @founder
Next Action: Dev ticket created (#456)
```

### Step 5: IMPLEMENT

**Who:** Engineering team  
**Action:**
1. Dev ticket references exact approved copy
2. Pull from content library (single source of truth)
3. Implement with exact wording (no paraphrasing)
4. Update Figma if layout shifts
5. QA validates copy matches approved version
6. Deploy

### Step 6: ARCHIVE

**Who:** Content Owner  
**Action:**
1. Move old version to archive
2. Keep date + reason for reference
3. Link to new version

**Archive Format:**
```
Version: 1.0 (Deprecated)
Date: 2025-11-15 to 2025-12-24
Replaced By: Version 1.1
Reason: Improved conversion hypothesis
Old Copy: "Join the movement"
New Copy: "Start earning today"
Impact: Homepage Hero, Marketplace CTA
```

---

## 4. VERSIONING SYSTEM

### Version Tags

**Format:** `v[Major].[Minor]`

**Examples:**
- `v1.0` — Launch
- `v1.1` — Post-launch polish
- `v1.2` — First big feature wave
- `v2.0` — Major rebrand or platform shift

### Change Types

| Change Type | Version Impact | Example |
|-------------|----------------|---------|
| Typo fix | No version change | "teh" → "the" |
| Micro-copy tweak | Patch (v1.1 → v1.1.1) | Button text refinement |
| New feature copy | Minor (v1.1 → v1.2) | Add leaderboard page |
| Brand voice shift | Major (v1.0 → v2.0) | Complete messaging overhaul |

### Change Log Entry Template

```markdown
## v1.2 — Feature Wave: Leaderboard Launch
**Date:** 2025-12-24  
**Scope:** Major feature addition

### Added
- Leaderboard page (all copy)
- Rank-up animation messages
- Badge tooltips (5 types)
- Leaderboard onboarding flow

### Changed
- Homepage Hero CTA: "Join" → "Start earning today"
- Marketplace: Added leaderboard link in nav

### Removed
- N/A

### Reason
Launch of competitive leaderboard feature to drive engagement.

### Impact
- **Pages:** Homepage, Leaderboard (new), Navigation
- **Components:** Hero CTA, Nav Menu, Badge Card, Rank Card
- **Tickets:** #456, #457, #458
```

---

## 5. CONTENT RULES

### Universal Principles

1. **Short Sentences**
   - Target: 15-20 words max
   - Break complex ideas into multiple sentences
   - One idea per sentence

2. **Clear CTAs**
   - Action verbs: Start, Create, Share, Earn
   - Specific outcomes: "Start earning today" > "Get started"
   - No ambiguity

3. **No Jargon**
   - Avoid: "Leverage your digital assets"
   - Use: "Sell your products"
   - If technical term needed, explain in tooltip

4. **Always Human**
   - Write like you're talking to a friend
   - Avoid corporate speak
   - Use "you" and "your"

5. **Culturally Grounded**
   - Caribbean voice: warm, confident, direct
   - Celebrate heritage without stereotypes
   - Global-ready but locally authentic

### Voice by Audience

**For Creators:**
- Tone: Empowering, supportive
- Message: "Your creativity deserves income"
- Example: "Upload your first product and start earning today"

**For Youth:**
- Tone: Hype + actionable
- Message: "Earn for real. Rise with your culture."
- Example: "Share your first link and watch the earnings roll in"

**For Diaspora:**
- Tone: Emotional + purposeful
- Message: "Support home through commerce, not charity"
- Example: "Every purchase supports a Caribbean creator building their future"

**For Press:**
- Tone: Visionary + credible
- Message: "A digital economy built by us, for us"
- Example: "CodexDominion is the Caribbean's first culture-driven digital marketplace"

---

## 6. REVIEW CADENCE

### Weekly Content Sync (15 min)
- Review pending proposals
- Prioritize changes
- Assign drafters

### Monthly Content Audit (30 min)
- Review usage analytics
- Identify drop-off points
- Plan improvements

### Quarterly Voice Check (60 min)
- Read all public copy aloud
- Check for drift from brand voice
- Update content library

---

## 7. ESCALATION

### When to Escalate

- Copy impacts brand positioning
- Legal/compliance concerns
- Cultural sensitivity issues
- Cross-team dependencies (design + eng + marketing)

### Escalation Path

1. Content Owner → Creative Director
2. Creative Director → Founder
3. Founder = final decision

---

## 8. TOOLS & SYSTEMS

### Recommended Stack

**Content Management:**
- Notion (flexible, collaborative)
- Confluence (enterprise teams)
- GitHub Issues + Markdown (dev-centric)

**Design Handoff:**
- Figma (design tokens + copy layers)
- Zeplin (developer handoff)

**Version Control:**
- Git for content files (if using Markdown)
- Notion version history
- Change log in docs/

**Collaboration:**
- Slack channel: #content-changes
- Weekly async check-in
- Tagged reviews: @content-owner, @design-owner, @tech-owner

---

## 9. LAUNCH CHECKLIST

Before any major feature launch:

- [ ] All new copy drafted and approved
- [ ] Content library updated
- [ ] Figma reflects approved copy
- [ ] Dev tickets reference exact copy blocks
- [ ] QA validates against approved version
- [ ] Change log updated
- [ ] Team trained on new messaging
- [ ] Press materials aligned (if public-facing)

---

## 10. EXAMPLES

### Example 1: Homepage Hero CTA Change

**Current Copy:** "Join the movement"  
**Proposed Copy:** "Start earning today"  
**Reason:** More direct, outcome-focused  
**Review:**
- Content Owner: ✅ Approved (clearer value prop)
- Design Owner: ✅ Fits layout (13 chars vs 17 chars)
- Tech Owner: ✅ No technical blockers  
**Status:** Approved v1.1 (2025-12-24)  
**Ticket:** #456  
**Deployed:** 2025-12-26  

### Example 2: Error Message Consistency

**Component:** Upload form validation  
**Current (inconsistent):**
- "File too big"
- "Maximum file size is 10MB"
- "Your file exceeds the limit"

**Approved (consistent):**
- "File exceeds 10MB limit. Please choose a smaller file."

**Voice Check:** ✅ Clear, actionable, no jargon  
**Length Check:** ✅ 55 characters (within limit)  
**Version:** v1.2 (2025-12-24)  

---

## APPENDIX: Content Change Board Template

### Notion Board Structure

**Columns:**
1. **Proposed** (New requests)
2. **In Draft** (Being written)
3. **In Review** (Awaiting approvals)
4. **Approved** (Ready for dev)
5. **Implemented** (Live on platform)
6. **Archived** (Old versions)

**Card Template:**
```
Title: [Component] - [Brief]
Priority: P1
Status: Proposed
Affected Pages: [List]
Current Copy: [Text]
Proposed Copy: [Text]
Reason: [Explanation]
Requestor: @user
Content Owner: @user
Design Owner: @user
Tech Owner: @user
Approvals: [ ] Content [ ] Design [ ] Tech
Version: [After approval]
Ticket: [After approval]
```

---

**End of Content Governance System**  
**Next:** See [BRAND_CONTENT_BIBLE.md](BRAND_CONTENT_BIBLE.md) for brand voice and messaging architecture.
