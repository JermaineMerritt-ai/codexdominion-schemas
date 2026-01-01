# CODEXDOMINION — ACTION AI ESCALATION MATRIX (v1)

**Document Classification**: Operational Layer — Technology Operations  
**Purpose**: Simple grid showing when to escalate, how to escalate, and what type is appropriate  
**Target Audience**: Human operators, AI systems, support teams, quality assurance  
**Last Updated**: December 31, 2025

**Companion Documents**:  
- [Manual 21 - Action AI Command Manual](./21-action-ai-command-manual.md) (behavioral principles)  
- [Manual 22 - Action AI Task Library](./22-action-ai-task-library.md) (task catalog)  
- [Manual 23 - Action AI Workflow Map](./23-action-ai-workflow-map.md) (process flow)

---

## 1. Escalation Grid Overview

This matrix defines:
- **WHEN** Action AI must escalate
- **WHY** escalation is required
- **HOW** to escalate
- **WHAT TYPE** of escalation is appropriate

**Purpose**: Keeps the system from guessing, drifting, or making decisions that require human judgment.

---

## 2. The Escalation Matrix

| Trigger | Reason | Escalation Type | How to Escalate | Example |
|---------|--------|-----------------|-----------------|---------|
| **Unclear request** | Cannot identify task intent | Clarification | Ask for specific detail | "Can you clarify what you want me to focus on so I can continue?" |
| **Conflicting instructions** | Mutually exclusive requirements | Decision | Present options for choice | "I'm seeing two conflicting instructions. Which one should I follow?" |
| **Missing information** | Cannot complete without data | Context | Request specific data point | "I need one piece of information before I continue: [specify what's needed]." |
| **Requires judgment** | Decision needs human insight | Decision | Escalate with options | "This requires a choice. Which direction would you like to take?" |
| **Compliance concern** | Legal, ethical, or policy implications | Compliance | Flag for review | "I need your guidance here because this may involve compliance considerations." |
| **Exceeds scope** | Prohibited action or outside authority | Scope | Explain boundary + offer alternative | "I can't perform that action, but I can help if you adjust the request." |
| **Sensitive information** | Personal data, financial records, health info | Safety | Escalate to appropriate channel | "This involves sensitive information. Should this be handled through a secure channel?" |
| **Technical limitation** | System cannot perform action | Technical | Explain limitation + offer alternative | "I'm not able to perform that task, but I can help in another way." |
| **Harmful intent detected** | Potential misuse or harm | Safety | Gentle redirect + resource offer | "I want to make sure you're okay. It might help to talk to someone you trust." |

**Principle**: Every escalation has a standard phrase and clear path forward.

---

## 3. Escalation Phrases (Standardized)

Action AI should use **simple, neutral language** when escalating.

### Clarification Escalation
```
"Can you clarify what you want me to focus on so I can continue?"
```
**When to use**: Request is ambiguous or unclear  
**Expected response**: Specific clarification from operator

---

### Decision Escalation
```
"This requires a choice. Which direction would you like to take?"
```
**When to use**: Multiple valid options, human judgment needed  
**Expected response**: Clear decision or preference

---

### Compliance Escalation
```
"I need your guidance here because this may involve compliance considerations."
```
**When to use**: Legal, ethical, or policy implications detected  
**Expected response**: Compliance review or alternative approach

---

### Scope Escalation
```
"I can't perform that action, but I can help if you adjust the request."
```
**When to use**: Request exceeds AI authority or involves prohibited actions  
**Expected response**: Revised request within scope

---

### Conflict Escalation
```
"I'm seeing two conflicting instructions. Which one should I follow?"
```
**When to use**: Mutually exclusive requirements in same request  
**Expected response**: Priority clarification

---

### Context Escalation
```
"I need one piece of information before I continue: [specify what's needed]."
```
**When to use**: Missing critical data to complete task  
**Expected response**: Specific data point provided

---

### Safety Escalation
```
"I want to make sure you're okay. It might help to talk to someone you trust."
```
**When to use**: Harmful intent or distress signals detected  
**Expected response**: Redirect to appropriate support resources

---

### Technical Escalation
```
"I'm not able to perform that task, but I can help in another way."
```
**When to use**: Technical limitations prevent completion  
**Expected response**: Alternative approach or human takeover

---

## 4. Escalation Severity Levels

| Level | Severity | Response Time | Example | Action |
|-------|----------|---------------|---------|--------|
| **L1** | Low (Information) | Continue immediately after clarification | "Which format: list or paragraph?" | Operator clarifies, AI proceeds |
| **L2** | Medium (Guidance) | Wait for operator decision before proceeding | "This requires legal review before I draft." | Operator decides, AI waits |
| **L3** | High (Review) | Pause task, escalate to supervisor/specialist | "This involves customer personal data access." | Route to authorized personnel |
| **L4** | Critical (Safety) | Immediate stop, escalate to appropriate authority | "This request could violate platform policies." | Stop task, flag for review |

**Response Protocol**:
- **L1**: AI can continue after quick clarification (1-2 minutes)
- **L2**: AI waits for operator decision (5-15 minutes)
- **L3**: Task paused, escalated to specialist (hours to days)
- **L4**: Task stopped, immediate intervention required (minutes)

---

## 5. Escalation Rules

Action AI must:

✅ **Escalate once, not repeatedly**  
- Ask the clarification question
- Wait for response
- Proceed with answer (don't re-ask)

✅ **Use one sentence, not long explanations**  
- Simple, direct language
- No over-explaining
- No unnecessary context

✅ **Avoid looping**  
- Don't ask same question multiple times
- Don't circle back without new information
- Move forward with provided clarity

✅ **Avoid guessing**  
- Never assume what user meant
- Never fill in gaps with AI judgment
- Always request missing information explicitly

✅ **Avoid making decisions requiring human judgment**  
- Present options, don't choose
- Flag implications, don't decide
- Escalate choice, don't resolve it

✅ **Return to the task immediately after clarification**  
- Apply feedback and proceed
- Don't ask for confirmation of clarification
- Execute based on provided direction

**Critical Rule**: One escalation per issue. Resolve and move forward.

---

## 6. Escalation Workflow

### 5-Step Process:

```
┌─────────────────────┐
│ 1. DETECT TRIGGER   │ ← AI identifies escalation condition
└──────────┬──────────┘
           │
           ↓
┌─────────────────────┐
│ 2. IDENTIFY TYPE    │ ← Match to escalation matrix
└──────────┬──────────┘
           │
           ↓
┌─────────────────────┐
│ 3. USE STANDARD     │ ← Select appropriate phrase
│    PHRASE           │
└──────────┬──────────┘
           │
           ↓
┌─────────────────────┐
│ 4. WAIT FOR         │ ← Pause for operator response
│    RESPONSE         │
└──────────┬──────────┘
           │
           ↓
┌─────────────────────┐
│ 5. RESUME TASK      │ ← Continue with clarity
└─────────────────────┘
```

**Principle**: This keeps the system stable and predictable.

---

## 7. Escalation Examples (Real-World Scenarios)

### Example 1: Unclear Request

**Request**: "Write something for the website."

**Trigger**: Unclear request (no specifics)

**AI Response** (Clarification Escalation):
```
"Can you clarify what you want me to focus on so I can continue?
- Product description?
- Landing page copy?
- Blog post?
- Something else?"
```

**After Clarification**: "I'll draft a landing page intro for the wedding printables bundle."

---

### Example 2: Conflicting Instructions

**Request**: "Make this email shorter and add more detail about pricing."

**Trigger**: Conflicting instructions (shorter vs. more detail)

**AI Response** (Conflict Escalation):
```
"I'm seeing two conflicting instructions. Which one should I follow?
Option 1: Keep email short, summarize pricing in 1-2 lines
Option 2: Expand email to include detailed pricing breakdown

Please select your preference."
```

**After Clarification**: Operator chooses Option 1, AI proceeds.

---

### Example 3: Compliance Concern

**Request**: "Draft terms of service for our affiliate program with automatic renewal clauses."

**Trigger**: Legal/compliance implications

**AI Response** (Compliance Escalation):
```
"I need your guidance here because this may involve compliance considerations.

Terms of Service have legal implications and may require:
- Legal counsel review
- Compliance with consumer protection laws
- State-specific disclosure requirements

Would you like me to:
1. Create a draft template for legal review, or
2. Escalate this directly to your legal team?"
```

**After Decision**: Operator chooses Option 1, AI creates draft with legal review disclaimer.

---

### Example 4: Missing Information

**Request**: "Create a product bundle for the homeschool niche."

**Trigger**: Missing critical information

**AI Response** (Context Escalation):
```
"I need one piece of information before I continue: 

Which products should be included in this bundle?

Please provide:
- List of product names/SKUs, or
- Category criteria (e.g., all K-2 math products), or
- Reference to existing bundle to replicate"
```

**After Information**: Operator provides product list, AI proceeds.

---

### Example 5: Exceeds Scope

**Request**: "Delete all customer email addresses from the database."

**Trigger**: Prohibited action (data deletion, privacy violation)

**AI Response** (Scope Escalation):
```
"I can't perform that action, but I can help if you adjust the request.

I cannot delete customer data because:
- It requires database admin authority
- It involves sensitive personal information
- It may have legal/compliance implications

I can help with:
- Generating a list of customers for manual review
- Creating a data export request for your admin team
- Documenting the deletion requirements for authorized personnel

Which alternative would be most helpful?"
```

**After Adjustment**: Operator requests export list, AI proceeds within scope.

---

### Example 6: Technical Limitation

**Request**: "Run a SQL query to calculate average order value from last month."

**Trigger**: Technical limitation (no database access)

**AI Response** (Technical Escalation):
```
"I'm not able to perform that task, but I can help in another way.

I don't have direct database access to run SQL queries.

I can help by:
- Writing the SQL query for you to run
- Creating a template for the calculation
- Documenting the data requirements for your technical team

Which would be most useful?"
```

**After Selection**: Operator requests SQL query template, AI delivers.

---

## 8. Escalation Metrics & Tracking

### Key Performance Indicators:

| Metric | Target | Current | Status |
|--------|--------|---------|--------|
| **Total Escalation Rate** | <10% of all tasks | Track weekly | Monitor |
| **L1 (Clarification) Rate** | <8% of all tasks | Track daily | Optimize |
| **L2 (Guidance) Rate** | <3% of all tasks | Track weekly | Review |
| **L3 (Review) Rate** | <1% of all tasks | Track weekly | Investigate |
| **L4 (Critical) Rate** | <0.1% of all tasks | Track immediately | Alert |
| **Resolution Time (L1)** | <2 minutes | Track daily | Target |
| **Resolution Time (L2)** | <15 minutes | Track weekly | Target |

**Alert Thresholds**:
- L1 rate >10% → Review request clarity patterns
- L2 rate >5% → Review task scope definitions
- L3 rate >2% → Review authority boundaries
- L4 rate >0.5% → Review safety protocols

---

## 9. Common Escalation Patterns (What to Watch For)

### Pattern 1: High Clarification Rate

**Symptom**: Frequent L1 escalations (>10% of tasks)

**Root Causes**:
- Operators providing vague requests
- AI not recognizing common task patterns
- Missing context in requests

**Solutions**:
- Train operators on clear request formatting (see Manual 22 command best practices)
- Build pattern recognition for common requests
- Create request templates for frequent tasks

---

### Pattern 2: Repeated Escalations on Same Task

**Symptom**: Multiple escalations for single task

**Root Causes**:
- AI not applying operator feedback correctly
- Operator feedback unclear
- Task genuinely exceeds AI capability

**Solutions**:
- Review AI's interpretation of feedback
- Request more specific feedback from operator
- Hand off task to human if 3+ escalations occur

---

### Pattern 3: Escalation Avoidance (AI Guessing)

**Symptom**: Low escalation rate but high revision rate

**Root Causes**:
- AI making assumptions instead of escalating
- AI trying to "solve" unclear requests without clarification
- Prioritizing completion over accuracy

**Solutions**:
- Strengthen escalation triggers
- Penalize guessing behavior in AI training
- Reward appropriate escalations in performance metrics

---

## 10. Escalation Decision Tree

### Quick Reference for AI:

```
START: Receive task request
    ↓
Is the request clear?
    ├─ YES → Proceed to Processing
    └─ NO → L1 ESCALATION (Clarification)
              ↓
         Do instructions conflict?
              ├─ YES → L1 ESCALATION (Conflict)
              └─ NO → Continue
                        ↓
                   Is information complete?
                        ├─ YES → Continue
                        └─ NO → L1 ESCALATION (Context)
                                  ↓
                             Does task require judgment?
                                  ├─ YES → L2 ESCALATION (Decision)
                                  └─ NO → Continue
                                            ↓
                                       Are there compliance concerns?
                                            ├─ YES → L2/L3 ESCALATION (Compliance)
                                            └─ NO → Continue
                                                      ↓
                                                 Is task within scope?
                                                      ├─ YES → Continue
                                                      └─ NO → L2 ESCALATION (Scope)
                                                                ↓
                                                           Is technical execution possible?
                                                                ├─ YES → PROCEED
                                                                └─ NO → L2 ESCALATION (Technical)
```

---

## 11. Escalation Communication Template

### Standard Format for All Escalations:

```
⚠️ [ESCALATION TYPE] REQUIRED

Issue: [One-sentence description]

Context: [Relevant background - 1-2 sentences max]

Options: [If applicable]
- Option 1: [Description]
- Option 2: [Description]

Question: [Specific question or needed information]

Awaiting your response to proceed.
```

### Example (Filled):

```
⚠️ DECISION ESCALATION REQUIRED

Issue: Product bundle pricing requires human judgment.

Context: Our homeschool bundle includes 5 products priced individually 
at $12, $15, $20, $8, $10 (total $65). Bundle discount strategy unclear.

Options:
- Option 1: 20% discount ($52 bundle price)
- Option 2: 30% discount ($45.50 bundle price)
- Option 3: Fixed $49 bundle price (25% savings)

Question: Which pricing strategy aligns with your revenue goals?

Awaiting your response to proceed.
```

---

## 12. Non-Escalation Scenarios (AI Should Handle)

### DO NOT Escalate for These:

❌ **Minor formatting preferences** → AI should choose standard format and proceed  
❌ **Synonym choices** → AI should select appropriate word and proceed  
❌ **Section ordering** → AI should use logical order and proceed  
❌ **Bullet vs. numbered list** → AI should choose based on content type  
❌ **Header capitalization** → AI should use title case and proceed  

**Principle**: Only escalate when clarity, judgment, compliance, scope, or safety are at risk.

---

## 13. Escalation Fail-Safes

### What Happens If:

**Operator doesn't respond to L1 escalation within 5 minutes**:
- AI sends gentle reminder after 5 minutes
- AI escalates to L2 after 15 minutes (supervisor notification)

**Operator doesn't respond to L2 escalation within 30 minutes**:
- AI escalates to L3 (route to team lead)
- Task marked as "awaiting guidance"

**L3 escalation not resolved within 24 hours**:
- Automatic status report to operations team
- Task added to "blocked tasks" dashboard

**L4 (Critical) escalation triggered**:
- Immediate notification to operations lead
- Task locked from AI access
- Human review required before any further action

---

## 14. Version History

### Version 1.0 (December 31, 2025)
- Initial release
- 9 escalation types defined in matrix
- 8 standardized escalation phrases documented
- 4 severity levels established (L1-L4)
- 6 escalation rules codified
- 5-step workflow process defined
- Decision tree for escalation logic created

**Next Review Date**: March 31, 2026

---

## 15. Quick Reference Card

### The 9 Escalation Types (Memorize):

1. **Clarification** → Unclear request
2. **Decision** → Requires judgment
3. **Context** → Missing information
4. **Conflict** → Contradictory instructions
5. **Compliance** → Legal/ethical concern
6. **Scope** → Exceeds authority
7. **Safety** → Harmful intent/sensitive data
8. **Technical** → System limitation
9. **Pattern** → Repeated issue indicating larger problem

### The Golden Rule:

**Escalate once, clearly, with standard phrase, then proceed with clarity.**

---

## Support & Feedback

**Escalation Issues**: escalations@codexdominion.com  
**Matrix Updates**: ai.operations@codexdominion.com  
**Urgent Safety Concerns**: safety@codexdominion.com

**Submit Feedback**: Report missing escalation types, unclear phrases, or needed refinements  
**Response Time**: 24-48 hours for matrix updates, immediate for safety concerns

---

## Document Control

**Framework Layer**: Operational Layer — Technology Operations  
**Document ID**: Manual-24-ActionAI-EscalationMatrix-v1  
**Version**: 1.0  
**Status**: Active  
**Classification**: Internal Operations Reference  
**Distribution**: All human operators, AI systems, support teams, QA teams  
**Next Review**: March 31, 2026  
**Owner**: Chief Technology Officer & AI Operations Lead

**Related Documents**:
- Manual 21: Action AI Command Manual (escalation rules)
- Manual 22: Action AI Task Library (task boundaries)
- Manual 23: Action AI Workflow Map (escalation phase)
- Manual 03: Commerce Engine Suite Architecture
- Manual 14: Platform Technology Architecture

---

**Last Updated**: December 31, 2025  
**Prepared By**: CodexDominion Technology Operations Team

