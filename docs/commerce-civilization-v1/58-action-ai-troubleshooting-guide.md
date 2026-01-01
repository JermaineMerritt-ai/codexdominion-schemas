# Action AI System Troubleshooting Guide

**Document Control**
- Manual ID: 58
- Version: 1.0
- Status: Active
- Effective Date: January 1, 2026
- Last Updated: January 1, 2026
- Approved By: System Owner
- Review Cycle: Quarterly

---

## 1. Purpose of the Troubleshooting Guide

The Troubleshooting Guide provides **simple, fast solutions** to the most common issues users encounter when working with Action AI.

**Why This Matters:**
- Most issues can be fixed in seconds with the right command
- Users don't need to understand why something went wrong
- Simple revision commands solve 95% of problems
- No need to start over or abandon tasks
- Builds confidence in system recovery

**Who Uses This Guide:**
- New users encountering first issues
- Experienced users needing quick fixes
- Team leaders helping others troubleshoot
- Support staff resolving user problems

**How to Use This Guide:**
- Scan for the issue you're experiencing
- Copy the suggested fix command
- Apply it to your output
- Most issues resolve immediately

---

## 2. When the Output Doesn't Match the Request

### The Issue

The AI misunderstood the task or produced something outside the intended scope.

**What It Looks Like:**
- You asked for a summary but got a rewrite
- You requested simple content but got complex
- The output addresses different points than intended
- The content feels like it's for a different task

### Why It Happens

**Common Causes:**
- The request was too broad or vague
- The task type wasn't explicitly stated
- The AI interpreted the instruction differently than expected
- Multiple interpretations were possible
- Key details were implied but not stated

**Example Misinterpretations:**
```
Request: "Fix this email"
Possible interpretations:
• Rewrite for clarity?
• Adjust the tone?
• Fix grammar only?
• Reorganize structure?
```

### How to Fix It

**Use one of these reset commands:**

**Option 1: Realign with Original**
```
"Rewrite this to match the original request."
```
This tells the system to go back to what you actually asked for.

**Option 2: Clarify Scope**
```
"Stay within the original scope."
```
This prevents additions or expansions beyond the original task.

**Option 3: Complete Reset**
```
"Let's restart. Here's what I need: [clear new instructions]"
```
This clears all context and starts completely fresh.

### Real-World Example

**Scenario:**
```
Original Request: "Summarize this article in three bullets"
Output: [Full rewritten article with analysis]

Fix: "Rewrite this to match the original request — just three bullet points summarizing the article."

Result: [Clean three-bullet summary]
```

### Prevention

**To avoid this in the future:**
- Be explicit about task type: "Summarize this" vs "Rewrite this"
- Specify format: "in three bullets" vs "as paragraphs"
- State constraints: "keep it simple" vs "make it comprehensive"

---

## 3. When the Output Is Too Long

### The Issue

The AI produced more detail, length, or complexity than needed.

**What It Looks Like:**
- You wanted 3 bullets but got 10
- You needed 100 words but got 500
- Simple content became comprehensive
- Quick overview became detailed explanation

### Why It Happens

**Common Causes:**
- The request didn't specify length constraints
- The AI defaulted to fuller, more complete version
- "Draft" or "write" requests often produce longer content
- The system tried to be thorough

**The AI's Default Behavior:**
When length isn't specified, the system tends toward complete, thorough responses rather than minimal ones.

### How to Fix It

**Condensing Commands:**

**Option 1: General Shortening**
```
"Shorten this."
```
The system will reduce length while keeping key points.

**Option 2: Make More Concise**
```
"Make this more concise."
```
Tightens language and removes unnecessary words.

**Option 3: Specific Length**
```
"Reduce this to five bullet points."
"Shorten this to 100 words."
"Cut this to one paragraph."
```
Gives the system a clear target length.

**Option 4: Remove Unnecessary**
```
"Remove anything unnecessary."
```
Cuts content not essential to the core message.

### Real-World Example

**Scenario:**
```
Request: "Draft a product description"
Output: [500-word detailed description with features, benefits, use cases, testimonials]

Fix: "Shorten this to 100 words and focus only on key benefits."

Result: [Concise 100-word description highlighting main benefits]
```

### Prevention

**To avoid this in the future:**
- Include length constraints: "in 50 words or less"
- Specify format: "3 short bullets" vs "detailed bullets"
- Use "short" or "brief" in your request
- Examples: "Draft a short email" vs "Draft an email"

---

## 4. When the Output Is Too Short

### The Issue

The AI didn't provide enough detail, depth, or explanation.

**What It Looks Like:**
- Brief bullet points when you wanted paragraphs
- Surface-level content when you needed depth
- Missing examples or context
- Feels incomplete or underdeveloped

### Why It Happens

**Common Causes:**
- The request didn't specify depth requirements
- The AI defaulted to minimal version
- Request used words like "short" or "brief" too broadly
- The system interpreted "simple" as "minimal"

### How to Fix It

**Expansion Commands:**

**Option 1: General Expansion**
```
"Expand this."
"Add more detail."
"Make this more comprehensive."
```

**Option 2: Expand Specific Sections**
```
"Expand section 2."
"Add more detail to the third bullet."
"Develop the introduction further."
```

**Option 3: Add Specific Elements**
```
"Add two examples."
"Add context explaining why this matters."
"Include more explanation of how this works."
```

**Option 4: Target Length**
```
"Expand this to 200 words."
"Make each section a full paragraph."
"Add three more bullet points."
```

### Real-World Example

**Scenario:**
```
Request: "Summarize the benefits"
Output:
• Saves time
• Reduces costs
• Improves quality

Fix: "Expand each bullet with one sentence explaining how."

Result:
• Saves time — Automates repetitive tasks, reducing manual work by 50%
• Reduces costs — Eliminates need for additional software subscriptions
• Improves quality — Catches errors before they reach customers
```

### Prevention

**To avoid this in the future:**
- Specify desired depth: "with detailed explanations"
- Request examples: "include 2-3 examples"
- State comprehensiveness: "comprehensive summary" vs "brief summary"
- Use expansion words: "thorough," "detailed," "complete"

---

## 5. When the Tone Feels Off

### The Issue

The writing feels too formal, too casual, inconsistent, or doesn't match your intended audience.

**What It Looks Like:**
- Professional content sounds too stiff
- Casual content sounds too informal
- Tone varies throughout document
- Language doesn't fit the audience
- Feels robotic or overly friendly

### Why It Happens

**Common Causes:**
- Tone wasn't specified in request
- The AI defaulted to standard professional tone
- Request used ambiguous tone descriptors
- Multiple revisions introduced tone drift
- Different sections had different implied tones

**The AI's Default Tone:**
Professional, neutral, direct — unless otherwise specified.

### How to Fix It

**Tone Adjustment Commands:**

**Option 1: Professional/Formal**
```
"Rewrite this in a more professional tone."
"Make this more formal."
"Adjust for a business audience."
```

**Option 2: Casual/Friendly**
```
"Make this friendlier."
"Use a more casual tone."
"Write this like you're talking to a friend."
```

**Option 3: Direct/Simple**
```
"Make this more direct."
"Simplify the language."
"Remove any flourish or embellishment."
```

**Option 4: Warm/Welcoming**
```
"Make this warmer."
"Add a welcoming tone."
"Make this feel more human."
```

**Option 5: Consistent**
```
"Make the tone consistent throughout."
"Use a professional tone for all sections."
"Adjust everything to match section 1's tone."
```

### Real-World Example

**Scenario:**
```
Request: "Draft a customer email"
Output: "Per your inquiry regarding product specifications, please find the requisite information enumerated below."

Fix: "Rewrite in a friendly, conversational tone."

Result: "Thanks for asking! Here's the information you requested about our product."
```

### Prevention

**To avoid this in the future:**
- Always specify tone: "professional," "casual," "friendly," "direct"
- Provide tone examples: "like this sample email"
- State audience: "for executives," "for general public," "for team members"
- Use tone descriptors: "warm but professional," "friendly but clear"

---

## 6. When the Structure Is Messy

### The Issue

The content feels unorganized, hard to scan, or lacks clear visual hierarchy.

**What It Looks Like:**
- Long paragraphs without breaks
- No headings or sections
- Inconsistent formatting
- Bullet points where paragraphs should be (or vice versa)
- Hard to find information quickly

### Why It Happens

**Common Causes:**
- The request didn't specify structure requirements
- The AI followed the input's formatting
- Structure wasn't part of the original task
- Default formatting doesn't match your needs

### How to Fix It

**Organizing Commands:**

**Option 1: Add Structure**
```
"Organize this into sections with headings."
"Add clear sections with titles."
"Structure this with a logical flow."
```

**Option 2: Add Formatting**
```
"Turn this into bullet points."
"Format this as a numbered list."
"Add headings to each section."
```

**Option 3: Clean Up**
```
"Clean this up and make it easier to read."
"Improve the formatting."
"Make this more scannable."
```

**Option 4: Specific Structure**
```
"Organize this as: Introduction, Benefits, How It Works, Next Steps."
"Turn each paragraph into a section with a heading."
"Create a checklist from this."
```

### Real-World Example

**Scenario:**
```
Request: "Draft instructions for using the software"
Output: [Long paragraph with all steps run together]

Fix: "Organize this into numbered steps with clear headings for each phase."

Result:
## Phase 1: Setup
1. Download the software
2. Run the installer

## Phase 2: Configuration
3. Enter your credentials
4. Select your preferences

## Phase 3: First Use
5. Launch the application
6. Complete the tutorial
```

### Prevention

**To avoid this in the future:**
- Specify structure: "as numbered steps," "with sections"
- Request formatting: "with bullet points," "with headings"
- Provide structure examples: "organize like this outline"
- Use organizing verbs: "structure," "organize," "format"

---

## 7. When the AI Asks Too Many Questions

### The Issue

The AI escalates for clarification more often than expected, slowing down workflow.

**What It Looks Like:**
- AI asks questions on nearly every request
- Multiple questions before proceeding
- Questions about details you consider obvious
- Feels like the system is overly cautious

### Why It Happens

**Common Causes:**
- The request was genuinely ambiguous
- The task type wasn't explicitly stated
- Multiple interpretations were possible
- The AI detected a potential boundary risk
- Request included vague descriptors ("fix this," "clean this up")

**When Questions Are Appropriate:**
The system should ask when:
- Request is unclear (multiple interpretations)
- Critical detail is missing (length, tone, format)
- Task type uncertain (summary vs rewrite)
- Boundary might be crossed (restricted domain)

### How to Fix It

**Proceed Commands:**

**Option 1: General Proceed**
```
"You have enough information — proceed."
"Go ahead with your best interpretation."
"Proceed without further questions."
```

**Option 2: Focused Directive**
```
"Focus only on [specific aspect]."
"Ignore [unclear element] and handle the rest."
"Proceed with [specific interpretation]."
```

**Option 3: Provide Quick Clarification**
```
"Use a professional tone."
"Keep it to three paragraphs."
"Organize as bullet points."
```
One specific answer usually allows immediate progress.

### Real-World Example

**Scenario:**
```
Request: "Organize this content"
AI: "Would you like it organized by topic, priority, or chronologically?"

Option A: "By topic."
Option B: "You have enough context — proceed with your best judgment."

Result: [Proceeds with organization]
```

### Prevention

**To avoid this in the future:**
- Be more specific in initial requests
- Include format, tone, and length upfront
- Use explicit task types: "Summarize" vs "Fix"
- Anticipate potential questions and answer them preemptively
- Example: "Summarize this in 3 bullets using a professional tone"

---

## 8. When the AI Refuses a Task

### The Issue

The AI declines to proceed with the request, citing boundary or safety concerns.

**What It Looks Like:**
- "I can't provide legal advice..."
- "I can't make decisions..."
- "I can't interpret sensitive content..."
- "This crosses a boundary..."

### Why It Happens

**Common Causes:**
- The request touched a restricted domain (legal, medical, financial)
- The request asked for strategic decisions
- The request required sensitive interpretation
- The request used emotional or symbolic language
- The task involved making choices for the user

**The 11 Restricted Domains (from Manual 25):**
1. Legal advice
2. Medical advice
3. Financial advice
4. Sensitive personal interpretation
5. Strategic decisions
6. Policy creation
7. Authorization decisions
8. Conflict resolution
9. Cultural/religious interpretation
10. Risk assessment
11. Compliance/regulatory guidance

### How to Fix It

**Reframing Commands:**

**Option 1: Shift from Advice to Information**
```
Instead of: "What should I do legally?"
Use: "Summarize the key legal concepts I should research."

Instead of: "Give me medical advice"
Use: "Organize these symptoms for my doctor's appointment."
```

**Option 2: Shift from Decision to Options**
```
Instead of: "Which option should I choose?"
Use: "Outline the pros and cons of each option."

Instead of: "What's the right strategy?"
Use: "Compare these two strategic approaches."
```

**Option 3: Shift from Interpretation to Summary**
```
Instead of: "Analyze the emotional meaning of this"
Use: "Summarize the factual content without interpretation."

Instead of: "What does this symbolize?"
Use: "List the main themes mentioned."
```

### Real-World Example

**Scenario:**
```
Request: "Draft a contract for this partnership"
AI: "I can't draft legal contracts. I can help you organize information for your lawyer."

Reframe: "Create an outline of key points to discuss with my lawyer about this partnership."

Result: [Organized outline of topics, terms, and questions for legal review]
```

### Common Reframing Patterns

**For Legal Tasks:**
- ❌ "Draft a contract" → ✓ "Create an outline for my lawyer"
- ❌ "Is this legal?" → ✓ "What legal topics should I research?"

**For Medical Tasks:**
- ❌ "Diagnose this symptom" → ✓ "Organize symptoms for my doctor"
- ❌ "What treatment do I need?" → ✓ "List questions to ask my doctor"

**For Financial Tasks:**
- ❌ "Should I invest in this?" → ✓ "Compare the pros and cons"
- ❌ "Give me financial advice" → ✓ "Outline factors to consider"

**For Strategic Tasks:**
- ❌ "What should our strategy be?" → ✓ "Compare these three strategies"
- ❌ "Make this decision for me" → ✓ "Present the options clearly"

### Prevention

**To avoid this in the future:**
- Request information organization instead of advice
- Ask for options instead of recommendations
- Request summaries instead of interpretations
- Frame tasks as "help me prepare for [expert]" rather than "tell me what to do"

---

## 9. When the Output Drifts Over Time

### The Issue

Tone, structure, or behavior slowly changes over multiple interactions or revisions.

**What It Looks Like:**
- First output was concise, later outputs are verbose
- Professional tone becomes casual over time
- Structure becomes inconsistent
- New patterns or phrases appear
- Formatting changes unexpectedly

### Why It Happens

**Common Causes:**
- Natural drift over extended sessions
- Inconsistent user instructions ("make it longer," then "make it shorter," then "add more")
- Multiple revisions compound small changes
- Complex multi-step tasks lose coherence
- Lack of explicit return-to-standards commands

**Drift Types:**
- **Tone drift**: Professional → casual or neutral → flowery
- **Structural drift**: Bullets → paragraphs or concise → verbose
- **Boundary drift**: Conservative → increasingly liberal interpretations
- **Behavioral drift**: Following rules → developing new patterns

### How to Fix It

**Realignment Commands:**

**Option 1: Return to Standard Tone**
```
"Return to the standard professional tone."
"Use the same tone as the first output."
"Reset to neutral, direct language."
```

**Option 2: Follow System Rules**
```
"Follow the system rules."
"Stick to system standards."
"Return to standard formatting."
```

**Option 3: Rewrite Using Standard Structure**
```
"Rewrite this using the usual structure."
"Format this like earlier outputs."
"Organize this consistently with previous sections."
```

**Option 4: Complete Reset**
```
"Let's start fresh with clear standards: [specify tone, structure, length]."
```

### Real-World Example

**Scenario:**
```
Output 1: "Schedule the meeting for Tuesday at 2 PM."
Output 2: "I'd recommend scheduling the meeting for Tuesday at 2 PM if that works."
Output 3: "Based on the team's availability and considering the various factors, it might be good to schedule the meeting for Tuesday at 2 PM, though Friday could also work depending on priorities."

Fix: "Return to the direct, concise style of Output 1."

Result: "Schedule the meeting for Tuesday at 2 PM."
```

### Prevention

**To avoid this in the future:**
- Include tone/structure reminders in requests: "Using professional tone..."
- Reference good earlier outputs: "Write this like the first section"
- Reset periodically on long tasks: "Let's confirm we're still on track"
- Use consistent phrasing across requests
- Leverage Manual 52 (Maintenance Schedule) for systematic drift checks

---

## 10. When the AI Adds Unnecessary Complexity

### The Issue

The output feels heavier, more elaborate, or more complex than needed.

**What It Looks Like:**
- Simple concepts explained with jargon
- Short content expanded with filler
- Basic instructions become elaborate
- Straightforward messages become complicated
- Unnecessary detail or examples added

### Why It Happens

**Common Causes:**
- The AI tried to be thorough or comprehensive
- The request didn't specify simplicity
- "Draft" or "create" requests default toward complete versions
- The system assumed more detail = better
- No constraints specified

### How to Fix It

**Simplification Commands:**

**Option 1: General Simplification**
```
"Simplify this."
"Make this simpler."
"Use plain language."
```

**Option 2: Remove Unnecessary**
```
"Remove anything unnecessary."
"Cut the fluff."
"Keep only essential information."
```

**Option 3: Make More Direct**
```
"Make this more direct."
"Get straight to the point."
"Remove elaboration."
```

**Option 4: Target Specific Elements**
```
"Remove all the examples."
"Cut the background context."
"Eliminate jargon."
```

### Real-World Example

**Scenario:**
```
Request: "Explain how to save a file"
Output: "The process of saving a file involves several important steps that ensure your work is properly preserved in the system. First, you'll want to navigate to the File menu, which is typically located at the top left of the application window..."

Fix: "Simplify this to just the essential steps."

Result:
1. Click File > Save
2. Choose location
3. Name the file
4. Click Save
```

### Prevention

**To avoid this in the future:**
- Use "simple" or "brief" in requests
- Specify "essential steps only"
- Request "without examples" if you don't need them
- Use phrases like "quick overview" vs "comprehensive guide"
- Specify target audience: "for someone who already understands the basics"

---

## 11. When You're Not Sure What Went Wrong

### The Issue

Something feels off about the output, but you can't pinpoint the specific problem.

**What It Looks Like:**
- The output just doesn't feel right
- Multiple small issues combined
- Can't articulate what's wrong
- Instinct says "this isn't what I wanted"
- Unsure how to request revision

### Why It Happens

**Common Causes:**
- Multiple small issues compound
- Expectation vs. reality mismatch
- Implied requirements not met
- Task was complex with many dimensions
- Original request was unclear to you too

### How to Fix It

**General Reset Commands:**

**Option 1: Improve Clarity**
```
"Rewrite this to be clearer."
```
Often fixes multiple issues at once.

**Option 2: Match Original Goal**
```
"Make this match the original goal."
"Realign with what I actually need."
```
Refocuses on core intent.

**Option 3: Complete Restart**
```
"Let's restart. Here's what I need: [very clear, specific instructions]"
```
Often the fastest solution when unsure.

**Option 4: Simplify Everything**
```
"Simplify this and keep only what's essential."
```
Removes complexity and refocuses.

**Option 5: Request Specific Dimensions**
```
"Rewrite this: professional tone, 100 words, three bullets."
```
Explicitly states what success looks like.

### Diagnostic Approach

**When unsure what's wrong, ask yourself:**

1. **Length Issue?**
   - Too long → "Shorten this"
   - Too short → "Expand this"

2. **Tone Issue?**
   - Wrong feel → "Rewrite in [tone] tone"

3. **Structure Issue?**
   - Messy → "Organize this with headings"
   - Wrong format → "Turn this into bullets"

4. **Alignment Issue?**
   - Off track → "Stay within original scope"
   - Misunderstood → "Rewrite to match request"

5. **Complexity Issue?**
   - Too complex → "Simplify this"
   - Too simple → "Add more detail"

### Real-World Example

**Scenario:**
```
Request: "Draft an update for the team"
Output: [Something that just feels wrong but you can't say why]

Fix: "Let's restart. Draft a short team update (3 bullets, professional tone) about the project timeline change."

Result: [Clean output matching clear specifications]
```

### Prevention

**To avoid this in the future:**
- Be more specific in initial requests
- Include: task type, tone, length, format, key points
- Example: "Draft a 100-word professional email with 3 key points about..."
- Take time to clarify your own mental picture before requesting

---

## 12. Troubleshooting Summary

**Most issues can be fixed with these six commands:**

### The Six Core Fix Commands

1. **"Shorten this"**
   - Fixes: Too long, too detailed, too verbose

2. **"Expand this"**
   - Fixes: Too short, not enough detail, feels incomplete

3. **"Rewrite this [in tone/for clarity/to match request]"**
   - Fixes: Wrong tone, unclear, misaligned

4. **"Organize this"**
   - Fixes: Messy structure, hard to scan, no hierarchy

5. **"Restart — here's what I need..."**
   - Fixes: Major misalignment, multiple issues, unclear problems

6. **"Stay within the original scope"**
   - Fixes: Drift, added complexity, scope creep

**These six commands solve 95% of problems instantly.**

---

## 13. Quick Troubleshooting Decision Tree

```
Is the output the right content?
  ├─ NO → "Rewrite this to match the original request"
  └─ YES → Continue

Is the length right?
  ├─ Too long → "Shorten this"
  ├─ Too short → "Expand this"
  └─ Right → Continue

Is the tone right?
  ├─ NO → "Rewrite in [tone] tone"
  └─ YES → Continue

Is the structure clear?
  ├─ NO → "Organize this with headings"
  └─ YES → Continue

Still not right?
  └─ "Let's restart. Here's what I need..."
```

---

## 14. Troubleshooting Best Practices

### For Users

**Before Requesting Fix:**
- Identify specific problem (length, tone, structure, alignment)
- Use precise fix commands from this guide
- Avoid vague requests like "fix this" or "make it better"

**When Requesting Revisions:**
- One issue at a time: "Shorten this" then "Make tone professional"
- Rather than: "Shorten this and make it professional and add sections"

**When Uncertain:**
- Reset with clear specifications
- Don't try multiple vague revisions
- Starting fresh is often faster

### For Team Leaders

**When Helping Others:**
- Point them to this guide
- Help them identify specific issue type
- Provide exact command to use
- Confirm understanding before they proceed

**Pattern Recognition:**
- Track common issues across team
- Update training based on patterns
- Share successful fix examples
- Build team-specific troubleshooting docs

### For System Stewards

**Monitoring Issues:**
- Track which fixes are used most often
- Identify systematic problems requiring documentation updates
- Monitor if certain users/task types have recurring issues
- Feed patterns into Manual 52 (Maintenance Schedule)

**Documentation Updates:**
- Add new troubleshooting patterns as discovered
- Update examples based on real issues
- Clarify guidance that confuses users
- Maintain troubleshooting effectiveness

---

## 15. Common Fix Commands Reference

**Copy this section for quick reference:**

### Length Issues
- "Shorten this"
- "Make this more concise"
- "Reduce to [number] words/bullets/paragraphs"
- "Expand this"
- "Add more detail to [section]"
- "Add [number] examples"

### Tone Issues
- "Rewrite in professional tone"
- "Make this more casual"
- "Make this friendlier"
- "Make this more direct"
- "Make tone consistent throughout"

### Structure Issues
- "Organize into sections with headings"
- "Turn this into bullet points"
- "Clean this up and make it easier to read"
- "Add headings"
- "Create a checklist from this"

### Alignment Issues
- "Rewrite to match the original request"
- "Stay within the original scope"
- "Focus only on [specific aspect]"
- "Realign with my original goal"

### Complexity Issues
- "Simplify this"
- "Remove anything unnecessary"
- "Make this more direct"
- "Use plain language"
- "Get straight to the point"

### General Resets
- "Let's restart. Here's what I need..."
- "Ignore previous revisions and start fresh"
- "Return to standard tone/structure"
- "Follow system rules"

---

## 16. Framework Integration

### How This Manual Connects to Others

**Manual 51 (Interaction Protocol):**
- Manual 51 explains how communication works
- Manual 58 shows how to fix when communication breaks down
- Together they enable smooth workflow recovery

**Manual 54 (Escalation Matrix):**
- Manual 54 explains when AI asks questions
- Manual 58 explains how to handle too many questions
- Section 7 directly addresses escalation issues

**Manual 56 (Onboarding Guide):**
- Manual 56 introduces the system
- Manual 58 provides recovery when things go wrong
- Read Manual 56 first, reference Manual 58 when needed

**Manual 57 (Task Library):**
- Manual 57 shows what tasks are possible
- Manual 58 shows how to fix tasks that go wrong
- Together they enable confident task execution

**Manual 52 (Maintenance Schedule):**
- Manual 52 uses troubleshooting patterns to identify drift
- Frequent issues signal need for maintenance
- System Stewards use this manual during audits

### Dependencies

**This Manual Requires:**
- Manual 51 (Interaction Protocol) — Defines normal flow
- Manual 54 (Escalation Matrix) — Defines question behavior

**This Manual Supports:**
- User confidence and self-service
- Reduced support burden
- Faster issue resolution
- Better user experience

---

## 17. Summary

The Action AI System Troubleshooting Guide provides **fast, simple fixes** for common issues.

**10 Common Issues:**
1. Output doesn't match request → Reset commands
2. Output too long → Shorten/condense commands
3. Output too short → Expand commands
4. Tone feels off → Tone adjustment commands
5. Structure messy → Organizing commands
6. Too many questions → Proceed commands
7. AI refuses task → Reframing strategies
8. Output drifts over time → Realignment commands
9. Unnecessary complexity → Simplification commands
10. Unclear problem → General reset commands

**Six Core Fix Commands:**
1. "Shorten this"
2. "Expand this"
3. "Rewrite this"
4. "Organize this"
5. "Restart — here's what I need..."
6. "Stay within the original scope"

**These solve 95% of problems instantly.**

**Remember:**
- Most issues fix in seconds with the right command
- Reset is always an option
- Specific commands work better than vague ones
- No need to abandon tasks — just revise

---

## 18. What to Read Next

**If you're new and learning the system:**
→ Read Manual 56 (Onboarding Guide) first

**If you want to understand normal workflow:**
→ Read Manual 51 (Interaction Protocol)

**If you're curious why AI asks questions:**
→ Read Manual 54 (Escalation Matrix)

**If you want to see all task types:**
→ Read Manual 57 (Task Library)

**If you're helping others troubleshoot:**
→ Keep Manual 58 (this guide) bookmarked

**If you're experiencing an issue right now:**
→ Find the issue in sections 2-11 and copy the fix command

---

## Document History

| Version | Date | Changes | Author |
|---------|------|---------|--------|
| 1.0 | January 1, 2026 | Initial release | System Owner |

**Review Schedule:** Quarterly (first week of January, April, July, October)

**Next Review:** April 1, 2026

---

**End of Manual 58**
