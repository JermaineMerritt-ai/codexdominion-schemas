# Manual 37: ACTION AI Troubleshooting Guide (v1)

**Version**: 1.0  
**Effective Date**: December 31, 2025  
**Classification**: User Support & Problem Resolution  
**Owner**: Commerce Civilization Council  
**Audience**: All Action AI Users

---

## Guide Purpose

This guide helps you quickly identify and fix common issues when working with the Action AI workforce.

**What This Guide Provides:**
- Fast diagnosis of what feels wrong
- Clear fixes for each issue type
- Simple troubleshooting steps
- When to reset, restart, or escalate

**When to Use This Guide:**
- Output doesn't match your request
- Tone feels off
- Length is wrong
- Structure is unclear
- AI asks too many questions
- AI escalates unnecessarily
- Something just feels misaligned

**Estimated Problem Resolution Time:** 2-5 minutes for most issues

---

## SECTION 1: QUICK DIAGNOSIS TABLE

Use this table to identify your issue type quickly:

| **Symptom** | **Issue Type** | **Quick Fix** | **Section** |
|-------------|---------------|---------------|-------------|
| **"This isn't what I asked for"** | Alignment | "Focus only on [X]" | 3.1, 4.4 |
| **"This is too long"** | Length | "Shorten this to [X] words/bullets" | 3.2 |
| **"This is too short"** | Length | "Expand section [X]" | 3.2 |
| **"Tone feels wrong"** | Tone | "Rewrite in [tone] tone" | 3.3, 4.3 |
| **"This is unclear"** | Clarity | "Make this clearer" | 4.1 |
| **"Missing information"** | Clarity | "Add detail about [X]" | 4.1 |
| **"Too vague"** | Clarity | "Be more specific about [X]" | 4.1 |
| **"Structure is wrong"** | Clarity | "Organize this as [format]" | 4.1 |
| **"AI asking too many questions"** | Request Ambiguity | Provide 1 clarifying detail | 3.4 |
| **"AI refused my task"** | Scope | Remove restricted elements | 4.2 |
| **"AI escalated unnecessarily"** | Escalation | "Proceed without escalation" | 4.5 |
| **"AI didn't escalate when needed"** | Escalation | "Escalate this to human" | 4.5 |
| **"Content drifted off-topic"** | Alignment | "Stay within original request" | 4.4 |
| **"Output is inconsistent"** | Alignment | "Make this consistent with [X]" | 4.4 |
| **"AI seems stuck in loop"** | System Issue | Reset task (Section 5) | 5 |
| **"This feels beyond repair"** | Major Issue | Request fresh draft (Section 6) | 6 |

---

## SECTION 2: THE FOUR MOST COMMON ISSUES

These four issues account for **80% of all troubleshooting scenarios**. Master these fixes and you'll resolve most problems quickly.

---

### Issue 1: "This Isn't What I Asked For"

**Cause:**  
The AI interpreted your request too broadly or misunderstood the focus.

**What Happened:**
- Request was ambiguous about scope
- AI included extra information you didn't need
- Focus shifted to wrong aspect of request
- Output covers too many topics

**The Fix:**

**Restate with Focus:**
```
"Focus only on [specific element]."
"Ignore [unwanted element]."
"This should only cover [X], not [Y]."
```

**Examples:**

❌ **Vague Feedback:** "This is wrong."  
✅ **Focused Feedback:** "Focus only on the marketing benefits, ignore the technical details."

❌ **Vague Feedback:** "Not what I wanted."  
✅ **Focused Feedback:** "This should be about product launch steps, not general marketing strategy."

❌ **Vague Feedback:** "Too much."  
✅ **Focused Feedback:** "Focus only on the first 3 steps. Remove everything after that."

**Preventive Tip:**
Next time, be more specific in your initial request about what to include and what to exclude.

---

### Issue 2: "This Is Too Long" (or Too Short)

**Cause:**  
Length wasn't specified, so AI used default length.

**What Happened:**
- You wanted a summary, AI gave a full explanation
- You wanted detail, AI gave a brief overview
- Output length doesn't match your needs

**The Fix:**

**Specify Exact Length:**
```
"Shorten this to [X] words."
"Condense this to 5 bullet points."
"Expand this to 3 paragraphs."
"Give me only the essentials."
```

**Examples:**

**Too Long:**
- "Shorten this to 100 words."
- "Condense this to 3 key points."
- "Give me a one-paragraph summary."

**Too Short:**
- "Expand section 2 with more detail."
- "Add 2-3 examples to illustrate this."
- "Develop this into a full page."

**Length Quick Reference:**
- **Brief:** 50-100 words, 3-5 bullets
- **Medium:** 200-400 words, 5-10 bullets
- **Detailed:** 500-1000 words, 10-20 bullets
- **Comprehensive:** 1000+ words, full structure

**Preventive Tip:**
Always specify desired length in your initial request: "Write a **short** email" or "Create a **detailed** checklist."

---

### Issue 3: "This Feels Off-Tone"

**Cause:**  
Tone wasn't specified, so AI used default professional tone.

**What Happened:**
- Too formal for your audience
- Too casual for your context
- Too technical for general readers
- Too simple for expert audience

**The Fix:**

**Specify Desired Tone:**
```
"Rewrite this in a [tone] tone."
"Make this more [quality]."
"Adjust the tone to be [characteristic]."
```

**Tone Options:**

| **Tone Type** | **When to Use** | **Example Phrase** |
|---------------|-----------------|-------------------|
| **Professional** | Business contexts, formal communication | "Rewrite in professional tone" |
| **Casual** | Social media, friendly emails | "Make this more casual" |
| **Friendly** | Customer-facing, approachable content | "Make this warmer and friendlier" |
| **Direct** | Clear instructions, no-nonsense | "Make this more direct" |
| **Simple** | General audience, easy reading | "Simplify this language" |
| **Technical** | Expert audience, detailed specs | "Use more technical language" |
| **Concise** | Busy readers, quick communication | "Make this more concise" |
| **Formal** | Legal, official documents | "Use formal language" |

**Examples:**

**Too Formal:**
- "Make this more casual and conversational."
- "This is too stiff—loosen the tone."

**Too Casual:**
- "Rewrite in a professional business tone."
- "This is too informal—make it more polished."

**Too Complex:**
- "Simplify this for a general audience."
- "Make this easier to understand."

**Too Simple:**
- "Add more technical detail."
- "This is too basic—add depth."

**Preventive Tip:**
Include tone in your initial request: "Write a **friendly** email" or "Create a **professional** report."

---

### Issue 4: "Why Is the AI Asking Me Questions?"

**Cause:**  
Your request was ambiguous or missing critical information.

**What Happened:**
- Request had multiple valid interpretations
- AI needed clarification to proceed correctly
- Missing details prevented execution
- Context was insufficient

**The Fix:**

**Provide One Clarifying Detail:**
```
"Focus on [specific aspect]."
"Use [specific format]."
"Target [specific audience]."
"Keep it [specific length/tone]."
```

**Common Escalation Questions and Responses:**

**Escalation:** "What should I focus on?"  
**Response:** "Focus on the marketing benefits."

**Escalation:** "What format should I use?"  
**Response:** "Use a numbered list."

**Escalation:** "What tone should I use?"  
**Response:** "Keep it professional."

**Escalation:** "How detailed should this be?"  
**Response:** "Keep it brief—3-5 bullet points."

**Escalation:** "Which option should I follow?"  
**Response:** "Go with option 2."

**Why This Happens:**
- AI prefers to clarify once rather than guess wrong
- Clarification saves revision time
- Ensures output matches your expectations

**Preventive Tip:**
Include key details in your initial request:
- What (content)
- Who (audience)
- Why (purpose)
- How (format/length/tone)

---

## SECTION 3: TROUBLESHOOTING BY CATEGORY

Use these sections for issues not covered in the top 4.

---

### 3.1 Clarity Issues

**Symptoms:**
- Vague or unclear output
- Missing steps or information
- Confusing structure
- Hard to follow logic
- Key points buried in text

**Root Causes:**
- Request was too broad
- Structure wasn't specified
- Output lacks organization
- Information presented without hierarchy

**Fixes:**

**Add Structure:**
```
"Organize this with section headings."
"Break this into numbered steps."
"Add bullet points for key information."
"Create a table to compare these options."
```

**Increase Clarity:**
```
"Make this clearer."
"Explain this more simply."
"Add examples to illustrate."
"Define any unclear terms."
```

**Specify Structure:**
```
"Structure this as: intro, 3 main points, conclusion."
"Format as: problem, solution, action steps."
"Organize by priority: high, medium, low."
```

**Examples:**

**Before Clarification:**
"Create a product launch plan."

**After Clarification:**
"Create a product launch plan with these sections: 1. Pre-launch (tasks), 2. Launch day (timeline), 3. Post-launch (follow-up). Use bullet points for each section."

**Preventive Tip:**
Specify structure in your initial request: "Create a **step-by-step** checklist" or "Write this as **intro + 3 sections + conclusion**."

---

### 3.2 Scope Issues

**Symptoms:**
- AI refuses to complete task
- AI escalates unnecessarily
- AI avoids answering directly
- AI cites boundary or compliance concern

**Root Causes:**
- Request approached restricted domain (legal, medical, financial advice)
- Request required strategic decision
- Request involved sensitive content
- Request unclear about boundaries

**Fixes:**

**Restate Without Restricted Elements:**
```
"Create a checklist of questions to ask [professional]."
"Provide general information about [topic], not advice."
"Focus on process documentation, not decision-making."
```

**Clarify Intent:**
```
"I'm asking for information, not advice."
"This is for educational purposes."
"I need a template, not specific guidance."
```

**Remove Decision Elements:**
```
"Compare these options objectively."
"List pros and cons without recommending."
"Provide framework for decision, not the decision itself."
```

**Examples:**

❌ **Restricted:** "Should I price my product at $97 or $197?"  
✅ **Allowed:** "Compare pros and cons of pricing at $97 vs $197."

❌ **Restricted:** "Tell me the best legal structure for my business."  
✅ **Allowed:** "Create a list of questions to ask my lawyer about business structures."

❌ **Restricted:** "Diagnose why my sales are down."  
✅ **Allowed:** "List common reasons why sales decline and data to check for each."

**Reference:**
See Manual 25 (Safety & Compliance Addendum) for complete list of restricted domains.

**Preventive Tip:**
Frame requests as information-gathering, comparison, or framework creation—not decision-making or advice-giving.

---

### 3.3 Tone Issues

**Symptoms:**
- Too casual or too formal
- Too complex or too simple
- Doesn't match brand voice
- Inconsistent throughout document
- Wrong level for audience

**Root Causes:**
- Tone not specified in request
- Multiple tones mixed in output
- Default tone doesn't match needs
- Audience level unclear

**Fixes:**

**Specify Exact Tone:**
```
"Rewrite in a professional tone."
"Make this more conversational."
"Simplify the language."
"Use a direct, no-nonsense tone."
```

**Adjust for Audience:**
```
"Write this for a general audience."
"Make this more technical for experts."
"Simplify this for beginners."
"Keep this accessible to non-specialists."
```

**Consistency Fix:**
```
"Make the tone consistent throughout."
"Match the tone of section 1."
"Keep the same voice from start to finish."
```

**Tone Spectrum:**

```
Formal ←→ Professional ←→ Friendly ←→ Casual

Complex ←→ Clear ←→ Simple

Technical ←→ Accessible ←→ General
```

**Quick Tone Phrases:**
- **More professional:** "Rewrite with business-appropriate language."
- **More casual:** "Make this sound like a conversation."
- **Simpler:** "Use everyday language."
- **More direct:** "Cut unnecessary words, get to the point."
- **Warmer:** "Add friendly, welcoming language."
- **More authoritative:** "Use confident, expert tone."

**Preventive Tip:**
Include tone and audience in initial request: "Write a **friendly, conversational** email for **small business owners**."

---

### 3.4 Alignment Issues

**Symptoms:**
- Output doesn't match original request
- Content drifts into unrelated topics
- Structure inconsistent with instructions
- Focus shifted from stated goal
- Extra information not requested

**Root Causes:**
- Initial request interpreted broadly
- AI expanded scope beyond boundaries
- Context accumulated incorrectly over revisions
- Multiple revision cycles caused drift

**Fixes:**

**Refocus on Original Request:**
```
"Stay within the original request."
"Focus only on what I asked for."
"Remove anything not directly related to [X]."
```

**Realign Content:**
```
"This should be about [X], not [Y]."
"Go back to the original instructions."
"Match the scope I specified."
```

**Remove Drift:**
```
"Remove sections on [unrelated topic]."
"Cut everything after [specific point]."
"Narrow this to only [specific scope]."
```

**Reset Context:**
```
"Let's restart. Here's what I need: [clear request]."
"Ignore previous revisions. Focus on this: [original goal]."
```

**Examples:**

**Request:** "Create a social media posting schedule."  
**Drifted Output:** Includes content strategy, brand voice guidelines, analytics setup  
**Realignment:** "Focus only on the posting schedule—days, times, platforms. Remove everything else."

**Request:** "Summarize this article in 5 bullets."  
**Drifted Output:** Includes analysis, commentary, additional context  
**Realignment:** "Give me only the 5 main points from the article. No analysis or extra context."

**Preventive Tip:**
After 2-3 revisions, if drift continues, request a fresh draft (see Section 6).

---

### 3.5 Escalation Issues

**Symptoms:**
- AI asks questions when it shouldn't
- AI doesn't escalate when it should
- AI escalates too frequently
- Clarification requests feel unnecessary

**Root Causes:**
- Request clarity threshold miscalibrated
- Boundary detection overly cautious
- Context should have been sufficient
- Escalation protocol misapplied

**Fixes:**

**Bypass Unnecessary Escalation:**
```
"You have enough information—proceed."
"Continue without asking."
"Make a reasonable assumption and execute."
```

**Force Escalation When Needed:**
```
"Escalate this to human review."
"I need a decision on this—escalate."
"This requires human judgment—escalate."
```

**Clarify Once and Move Forward:**
```
"[Provide clarification] Now proceed without further questions."
"Here's the detail you need: [info]. Complete the task now."
```

**Examples:**

**Unnecessary Escalation:**
- AI: "What tone should I use?"
- You: "Use your default professional tone and proceed."

**Missing Escalation:**
- You: "This requires a decision I need to make—escalate rather than providing options."

**Repeated Escalation:**
- You: "I've clarified this twice. Proceed with best judgment."

**When to Override Escalation:**
- Request is straightforward
- Context is sufficient
- Default approach acceptable
- Time-sensitive execution needed

**When to Force Escalation:**
- Strategic decision required
- Multiple valid approaches
- Risk of incorrect assumption
- Human judgment necessary

**Preventive Tip:**
If you notice frequent escalations, requests may be consistently under-specified. Add more detail to initial requests.

---

## SECTION 4: WHEN TO RESET THE TASK

**Reset the task** when the current direction is unrecoverable through revisions.

### Reset Triggers

**Trigger 1: Repeated Misalignment**
- Output misses the mark 2-3 times
- Revisions aren't improving alignment
- Core misunderstanding persists

**Trigger 2: Stuck in Loop**
- Same issue appearing repeatedly
- Revisions cycling without progress
- Output deteriorating instead of improving

**Trigger 3: Complexity Overload**
- Too many revisions accumulated
- Context has become cluttered
- Original intent lost in iterations

**Trigger 4: Context Drift**
- Output drifted far from original goal
- Multiple topics mixed together
- Scope expanded beyond control

**Trigger 5: Structural Mismatch**
- Format fundamentally wrong
- Structure can't be fixed through revision
- Need to start with different approach

### How to Reset

**Reset Phrase:**
```
"Let's restart. Here's what I need: [clear, specific request]."
```

**Reset Best Practices:**
1. **Acknowledge the reset:** "Let's start fresh."
2. **State clear request:** Be more specific than first attempt
3. **Include key details:** Format, length, tone, focus
4. **Remove ambiguity:** Eliminate what caused original confusion
5. **Confirm understanding:** Ask AI to acknowledge before proceeding

**Reset Example:**

**Instead of continuing revisions:**
"This still isn't right. Let's reset."

**Provide clear restart:**
"Let's restart. Create a 7-day social media posting schedule. Include: day of week, time, platform, post type. Format as a table. Keep it simple—no extra strategy or analysis."

### When NOT to Reset

Don't reset if:
- Issue is minor (tone, length adjustments)
- Single revision will fix it
- Only small section needs change
- Core content is correct

**Reset costs time—use it when revisions won't work.**

---

## SECTION 5: WHEN TO ASK FOR A FRESH DRAFT

**Ask for a fresh draft** when the current output is fundamentally wrong but the task is clear.

### Fresh Draft Triggers

**Trigger 1: Wrong Structure**
- Format completely mismatched
- Organization doesn't work
- Need different approach

**Trigger 2: Tone Completely Off**
- Voice is wrong throughout
- Can't be fixed with adjustments
- Need complete rewrite

**Trigger 3: Content Cluttered**
- Too much extraneous information
- Simplification revisions insufficient
- Easier to start over than cut down

**Trigger 4: Beyond Repair**
- Multiple issues compounding
- Revision would take longer than fresh start
- Cleaner to rebuild than fix

### How to Request Fresh Draft

**Fresh Draft Phrase:**
```
"Create a fresh draft focusing on [X]."
"Start over with this approach: [details]."
"New draft needed. This time: [specifications]."
```

**Fresh Draft Best Practices:**
1. **Acknowledge starting over:** "Let's try a fresh draft."
2. **Specify what to change:** "This time, focus on [X]."
3. **Clarify what to keep:** "Keep the same [topic/scope/goal]."
4. **Add missing details:** Include what was missing before
5. **Set clear expectations:** Format, length, tone, structure

**Fresh Draft Examples:**

**Example 1: Wrong Structure**
"Create a fresh draft. This time, organize as: Problem → Solution → Action Steps. 3 sections, bullet points, 200 words max."

**Example 2: Tone Off**
"Start over with a more professional tone. Same content, but rewrite for business audience."

**Example 3: Too Cluttered**
"Fresh draft needed. Include only the 5 core steps. Remove all background, context, and examples."

### Fresh Draft vs Reset

| **Fresh Draft** | **Reset** |
|-----------------|-----------|
| Task clear, execution wrong | Task unclear, need clarification |
| Keep same goal, change approach | Redefine goal from scratch |
| Structure/tone/content issue | Misalignment or scope issue |
| "Try again differently" | "Start completely over" |

---

## SECTION 6: WHEN TO ESCALATE TO SYSTEM RULES

**Escalate to system rules** when fundamental misalignment with operating principles occurs.

### System Escalation Triggers

**Trigger 1: Boundary Violation**
- AI operating outside defined role
- Safety compliance ignored
- Restricted domain entered

**Trigger 2: Protocol Breach**
- Interaction rules not followed
- Escalation protocol misapplied
- Communication standards violated

**Trigger 3: Quality Gate Failure**
- Output didn't pass quality checks
- Standards not maintained
- Consistency lost

**Trigger 4: Persistent Drift**
- Maintenance needed
- Systematic alignment issue
- Performance declining

**Trigger 5: Governance Concern**
- Strategic misalignment
- Authority confusion
- Systemic issue requiring review

### How to Escalate to System Rules

**Reference Specific Manual:**
```
"Align this with [Manual Name]."
"Review [Manual Name] and correct this output."
"This violates [Manual Name]—fix accordingly."
```

**Manual Quick Reference:**

| **Issue Type** | **Reference Manual** | **Manual Number** |
|---------------|---------------------|------------------|
| Role confusion | Role Definitions | Manual 27 |
| Boundary violation | Safety & Compliance | Manual 25 |
| Communication issue | Interaction Protocol | Manual 28 |
| Escalation problem | Escalation Matrix | Manual 24 |
| Quality concern | QA Checklist | Manual 31 |
| Performance issue | Performance Metrics | Manual 32 |
| Process confusion | Workflow Map | Manual 23 |
| Constitutional issue | Operating Charter | Manual 26 |
| Lifecycle error | Lifecycle Model | Manual 30 |
| Governance concern | Governance Framework | Manual 29 |

**Escalation Examples:**

**Boundary Issue:**
"This approaches a restricted domain. Review Manual 25 (Safety & Compliance) and revise accordingly."

**Role Issue:**
"You're operating outside your role boundaries. Reference Manual 27 (Role Definitions) and correct this."

**Communication Issue:**
"This violates the Interaction Protocol. Review Manual 28 and apply the correct tone standards."

**Quality Issue:**
"This didn't pass the quality gate. Apply Manual 31 (QA Checklist) before re-delivering."

### When to Contact Human Oversight

If system-level issues persist after referencing manuals:
1. Document the issue clearly
2. Note which manual was referenced
3. Describe what correction was attempted
4. Escalate to Operations Manager or Governance Team

**This is rare—most issues resolve through manual reference.**

---

## SECTION 7: QUICK TROUBLESHOOTING CHECKLIST

**Before giving up on a task, try these 8 steps in order:**

```
□ Step 1: Clarify the Request
   "Focus on [specific element]."

□ Step 2: Specify Tone
   "Rewrite in [tone] tone."

□ Step 3: Specify Length
   "Shorten this to [X] words/bullets."

□ Step 4: Specify Structure
   "Organize this as [format]."

□ Step 5: Ask for Rewrite
   "Rewrite this focusing on [X]."

□ Step 6: Ask for Summary
   "Summarize the key points in 3-5 bullets."

□ Step 7: Ask for Fresh Draft
   "Create a fresh draft with this approach: [details]."

□ Step 8: Reset the Task
   "Let's restart. Here's what I need: [clear request]."
```

**This sequence solves 95% of issues.**

---

## SECTION 8: TROUBLESHOOTING FLOWCHART

```
                    START: Issue Detected
                             |
                             v
                  ┌──────────────────────┐
                  │ Is it one of the     │
                  │ Top 4 Issues?        │
                  └──────┬───────────────┘
                         |
              ┌──────────┴─────────┐
              |                    |
             YES                   NO
              |                    |
              v                    v
     ┌────────────────┐   ┌──────────────────┐
     │ Apply Quick    │   │ Identify Category│
     │ Fix from       │   │ (Clarity, Scope, │
     │ Section 2      │   │ Tone, Alignment, │
     └────────┬───────┘   │ Escalation)      │
              |            └──────┬───────────┘
              v                   v
     ┌────────────────┐   ┌──────────────────┐
     │ Did it work?   │   │ Apply Category   │
     └────┬───────────┘   │ Fix from Sec 3   │
          |                └──────┬───────────┘
     ┌────┴────┐                  v
    YES       NO          ┌──────────────────┐
     |         |          │ Did it work?     │
     v         |          └────┬─────────────┘
  ┌──────┐    |               |
  │ DONE │    |          ┌────┴────┐
  └──────┘    |         YES       NO
              |          |         |
              v          v         v
     ┌────────────────┐ ┌──────┐ ┌──────────────┐
     │ Try Checklist  │ │ DONE │ │ 3+ revisions?│
     │ Steps 1-4      │ └──────┘ └────┬─────────┘
     └────────┬───────┘               |
              v                  ┌────┴────┐
     ┌────────────────┐         YES       NO
     │ Did it work?   │          |         |
     └────┬───────────┘          v         v
          |              ┌──────────────┐ ┌────────────┐
     ┌────┴────┐        │ Fresh Draft  │ │ Continue   │
    YES       NO        │ (Section 5)  │ │ Revisions  │
     |         |        └──────┬───────┘ └────────────┘
     v         v               v
  ┌──────┐ ┌──────────────┐ ┌──────────────┐
  │ DONE │ │ Try Fresh    │ │ Did it work? │
  └──────┘ │ Draft or     │ └────┬─────────┘
           │ Reset        │      |
           │ (Sec 5-6)    │ ┌────┴────┐
           └──────┬───────┘ YES       NO
                  v          |         |
          ┌──────────────┐  v         v
          │ Did it work? │ ┌──────┐ ┌─────────────┐
          └────┬─────────┘ │ DONE │ │ Escalate to │
               |            └──────┘ │ System Rules│
          ┌────┴────┐                │ (Section 6) │
         YES       NO                └─────────────┘
          |         |
          v         v
       ┌──────┐ ┌──────────────┐
       │ DONE │ │ Escalate to  │
       └──────┘ │ Human        │
                │ Oversight    │
                └──────────────┘
```

---

## SECTION 9: COMMON MISTAKE PATTERNS

Learn to recognize and avoid these frequent user errors:

### Mistake 1: Vague Feedback
❌ **Vague:** "This is wrong."  
✅ **Specific:** "This focuses on features, but I need benefits."

### Mistake 2: No Length Specification
❌ **Unclear:** "Write an email."  
✅ **Clear:** "Write a short, 3-sentence email."

### Mistake 3: Tone Assumptions
❌ **Assumed:** "Write a post." (expects casual, gets professional)  
✅ **Explicit:** "Write a casual, friendly social media post."

### Mistake 4: Over-Revising
❌ **Loop:** Request → Revise → Revise → Revise → Revise...  
✅ **Better:** Request → Revise (1-2x) → Fresh Draft or Reset

### Mistake 5: Giving Up Too Soon
❌ **Premature:** "This doesn't work." [stops]  
✅ **Systematic:** Try checklist steps 1-8 before stopping

### Mistake 6: Not Clarifying Ambiguity
❌ **Ignore:** AI asks question → User ignores → Output wrong  
✅ **Respond:** AI asks question → User clarifies once → Output correct

### Mistake 7: Scope Creep in Revisions
❌ **Expanding:** "Also add X, Y, Z..." [new requirements each revision]  
✅ **Focused:** State all requirements upfront or reset with full scope

### Mistake 8: Blaming AI for Unclear Requests
❌ **Blame:** "AI is wrong" [but request was ambiguous]  
✅ **Own It:** "Let me clarify my request" [take responsibility for clarity]

---

## SECTION 10: TROUBLESHOOTING QUICK WINS

**Fast fixes for the busiest users:**

### 10-Second Fixes
- **Too long:** "Shorten to 3 bullets."
- **Too short:** "Expand section 2."
- **Wrong tone:** "More professional."
- **Unclear:** "Make this clearer."

### 30-Second Fixes
- **Wrong focus:** "Focus only on [X], remove [Y]."
- **Bad structure:** "Organize as: [format]."
- **Off-brand:** "Match the tone of [example]."
- **Too complex:** "Simplify for general audience."

### 60-Second Fixes
- **Major alignment issue:** "Let's restart. [Clear request with details]."
- **Fundamental misunderstanding:** "Fresh draft. This time: [specific approach]."
- **Persistent problem:** "Reference Manual [X] and correct this."

**Most issues resolve in under 60 seconds with the right fix.**

---

## SECTION 11: WHEN TO CONTACT SUPPORT

**Contact human oversight when:**

1. **System-Level Issues:**
   - AI consistently violates operating principles
   - Multiple manual references don't resolve issue
   - Fundamental misalignment persists
   - Quality standards systematically failing

2. **Capability Gaps:**
   - AI cannot perform required task type
   - Task should be allowed but triggers escalation
   - Role boundaries unclear or misaligned
   - Workflow doesn't support your use case

3. **Documentation Issues:**
   - Manual guidance contradictory or unclear
   - Need clarification on boundaries
   - Process documentation insufficient
   - Rule interpretation needed

4. **Improvement Opportunities:**
   - Recurring issue affecting multiple users
   - System could be more efficient
   - Workflow could be streamlined
   - Documentation could be clearer

**Support Process:**
1. Document the issue clearly (what happened, what you expected)
2. Note troubleshooting steps already attempted
3. Reference relevant manuals consulted
4. Describe impact (time lost, task blocked, etc.)
5. Submit to Operations Manager or Governance Team

**Response Time Expectations:**
- Urgent issues (work blocked): 2-4 hours
- Normal issues: 1-2 business days
- Improvement suggestions: Next quarterly review

---

## Document Control

### Version History
| Version | Date | Changes | Author |
|---------|------|---------|--------|
| 1.0 | Dec 31, 2025 | Initial troubleshooting guide | Commerce Civilization Council |

### Review Schedule
- **Quarterly**: Update based on user feedback and recurring issues
- **Annually**: Comprehensive review and reorganization
- **Event-Triggered**: Update when new issue patterns identified or system changes

### Ownership & Approval
- **Guide Owner**: Commerce Civilization Council
- **Maintainer**: Operations Manager + User Support Team
- **Review Board**: Governance Team + User Experience Team
- **Approval Authority**: Council

### Related Documentation
- **Manual 36**: Onboarding Guide (how to use system)
- **Manual 35**: Master Handbook (complete system reference)
- **Manual 31**: QA Checklist (quality standards)
- **Manual 26**: Operating Charter (system foundation)
- **Manuals 21-34**: Individual operational manuals (detailed rules)

---

**End of Manual 37: ACTION AI Troubleshooting Guide**

**Most issues resolve in 2-5 minutes. Use the checklist. Reference the manuals. Ask clearly.**

**When in doubt: Clarify → Specify → Rewrite → Reset → Escalate**
