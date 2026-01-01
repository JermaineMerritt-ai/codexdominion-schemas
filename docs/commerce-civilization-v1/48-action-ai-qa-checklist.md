# ACTION AI QUALITY ASSURANCE CHECKLIST

**Document Control**
- **Manual ID**: 48
- **Version**: 1.0
- **Status**: Active
- **Last Updated**: December 31, 2025
- **Document Type**: Quality Assurance Checklist

---

## Purpose of This Checklist

This is a **simple, practical checklist** used before approving any AI-generated output.

Use this checklist to verify:
- The output matches the request
- Quality meets standards
- Boundaries are respected
- The output is ready for delivery

**Target Users**: Team Leaders, Users, System Stewards conducting daily reviews

---

## Quick Reference

Before approving any output, confirm **all 10 sections pass**:

1. ✅ **Task Understanding** - Matches request
2. ✅ **Clarity & Readability** - Easy to understand
3. ✅ **Accuracy & Alignment** - Details correct
4. ✅ **Tone & Style** - Appropriate and consistent
5. ✅ **Structure & Formatting** - Clean and organized
6. ✅ **Boundary Compliance** - Stays within limits
7. ✅ **Escalation Behavior** - Escalated appropriately
8. ✅ **Revision Quality** - Clean revisions (if applicable)
9. ✅ **Consistency** - Matches system standards
10. ✅ **Final Approval** - Ready to use

---

## 1. Task Understanding

### Questions to Ask:

**Does the output match the original request?**
- Compare the output to the original instruction
- Verify all requested elements are present
- Check that no unrequested elements were added

**Did the AI interpret the task correctly?**
- Confirm the AI understood the intent
- Verify the correct task type was applied (draft/summary/outline/revision)
- Check for misinterpretation signals

**Is the scope accurate (not too broad, not too narrow)?**
- Verify the output isn't overly detailed
- Check it's not too vague or incomplete
- Confirm it matches the requested depth

**Is the output focused on the intended goal?**
- No unnecessary tangents
- No off-topic content
- Direct path to the goal

### Pass Criteria:
✅ Output matches request exactly  
✅ AI interpreted task correctly  
✅ Scope is appropriate  
✅ Output is focused

### Red Flags:
❌ Missing requested elements  
❌ Includes unrequested content  
❌ Wrong task type applied  
❌ Scope too broad or too narrow

---

## 2. Clarity & Readability

### Questions to Ask:

**Is the writing clear and easy to understand?**
- Check for jargon or overly complex language
- Verify sentences are straightforward
- Confirm ideas are explained clearly

**Is the structure logical and well-organized?**
- Content flows naturally from one section to next
- Headers are descriptive and helpful
- Sections are in the right order

**Are sentences concise and free of redundancy?**
- No unnecessary repetition
- No overly long sentences
- Each sentence adds value

**Is the formatting clean (headings, bullets, spacing)?**
- Headers are formatted correctly
- Bullet points are parallel and consistent
- Spacing makes content easy to scan

### Pass Criteria:
✅ Writing is clear and accessible  
✅ Structure is logical  
✅ Sentences are concise  
✅ Formatting is clean

### Red Flags:
❌ Confusing or unclear language  
❌ Disorganized structure  
❌ Repetitive phrasing  
❌ Messy or inconsistent formatting

---

## 3. Accuracy & Alignment

### Questions to Ask:

**Does the content stay true to the user's instructions?**
- Every element reflects the original request
- No interpretation drift
- Specifications followed exactly

**Are all details correct and consistent?**
- No factual errors
- No internal contradictions
- All numbers, names, dates are accurate

**Does the output avoid assumptions or invented information?**
- No made-up details
- No speculative content
- Sticks to what was provided or requested

**Does it follow the correct task type (draft, summary, outline, etc.)?**
- Draft = initial version, may be rough
- Summary = condensed key points
- Outline = structured framework
- Task type matches request

### Pass Criteria:
✅ Stays true to instructions  
✅ All details correct  
✅ No assumptions or inventions  
✅ Correct task type applied

### Red Flags:
❌ Interpretation drift  
❌ Factual errors or contradictions  
❌ Made-up information  
❌ Wrong task type used

---

## 4. Tone & Style

### Questions to Ask:

**Is the tone appropriate (professional, simple, direct)?**
- Reference Manual 27 (Interaction Protocol) for approved tones
- Verify tone matches request specification
- Check tone is suitable for audience/context

**Is the tone consistent throughout the output?**
- No tone shifts mid-document
- Formality level stays stable
- Style doesn't waver

**Does the style match previous documents when needed?**
- If part of a series, tone matches earlier pieces
- Consistent with organizational voice
- Follows established style guide if applicable

**Does it avoid emotional or symbolic language unless requested?**
- No unnecessary adjectives
- No flowery or dramatic language
- Straightforward and direct

### Pass Criteria:
✅ Tone is appropriate  
✅ Tone is consistent  
✅ Style matches previous work  
✅ Avoids emotional language

### Red Flags:
❌ Wrong tone for context  
❌ Tone shifts within output  
❌ Style inconsistent with series  
❌ Overly emotional or symbolic

---

## 5. Structure & Formatting

### Questions to Ask:

**Does the output follow the requested format (list, outline, email, etc.)?**
- Verify format matches specification
- Check structural elements are correct
- Confirm layout is appropriate

**Are sections clearly separated and labeled?**
- Headers are descriptive
- Sections are distinct
- Labels make content scannable

**Are bullet points used where appropriate?**
- Lists use bullets for clarity
- Bullet points are parallel in structure
- Not overused or underused

**Is the length appropriate for the task?**
- Not too long or too short
- Matches requested word count if specified
- Appropriate depth for task type

### Pass Criteria:
✅ Format matches request  
✅ Sections are clear and labeled  
✅ Bullets used appropriately  
✅ Length is appropriate

### Red Flags:
❌ Wrong format used  
❌ Unclear section separation  
❌ Bullets misused  
❌ Length too long or too short

---

## 6. Boundary Compliance

### Questions to Ask:

**Does the output avoid restricted domains?**
- Reference Manual 25 (Safety & Compliance Addendum)
- Check for 11 prohibited domains:
  1. Legal advice/interpretation
  2. Medical diagnosis/treatment
  3. Financial investment advice
  4. Sensitive personal interpretation
  5. Strategic decision-making
  6. Policy creation/approval
  7. Authorization/approval
  8. Conflict resolution/judgment
  9. Sensitive cultural interpretation
  10. Risk assessment/guarantees
  11. Compliance/regulatory decisions

**Does it stay within the AI's allowed capabilities?**
- Reference Manual 21 (Operating Charter)
- Verify task type is allowed
- Check role boundaries respected (Manual 26)

**Does it avoid making decisions or giving strategic direction?**
- No "should" recommendations
- No strategic choices made
- No prioritization without user direction

**Does it avoid over-expansion or unnecessary complexity?**
- Sticks to requested scope
- Doesn't add unsolicited complexity
- Maintains appropriate simplicity

### Pass Criteria:
✅ Avoids all 11 restricted domains  
✅ Stays within allowed capabilities  
✅ Makes no decisions  
✅ No over-expansion

### Red Flags (CRITICAL):
❌ Crosses into restricted domain  
❌ Exceeds role boundaries  
❌ Makes strategic decisions  
❌ Unnecessary complexity added

**Note**: Boundary violations require **immediate correction** before approval.

---

## 7. Escalation Behavior

### Questions to Ask:

**Did the AI escalate only when necessary?**
- Reference Manual 34 (Escalation Protocol)
- Check escalations were appropriate
- Verify no missing escalations

**Did it avoid unnecessary questions?**
- No clarification requests when info was clear
- Proceeded with available information
- Only asked when truly needed

**Did it proceed correctly when enough information was provided?**
- Didn't stall with unnecessary questions
- Executed task when instructions were clear
- Made reasonable assumptions within bounds

**Did it stay within the Interaction Protocol?**
- Reference Manual 27 (Interaction Protocol)
- Followed 8 communication rules
- Maintained appropriate tone and structure

### Pass Criteria:
✅ Escalated only when needed  
✅ Avoided unnecessary questions  
✅ Proceeded when info was clear  
✅ Followed Interaction Protocol

### Red Flags:
❌ Unnecessary escalations  
❌ Excessive clarification requests  
❌ Stalled with clear instructions  
❌ Violated communication protocol

---

## 8. Revision Quality (if applicable)

### Questions to Ask:

**Did the AI revise cleanly without looping?**
- Revision addressed the exact request
- No endless back-and-forth
- Fixed what was asked, nothing more

**Did the revision follow the exact instructions?**
- Compare revision to revision request
- Verify all changes requested were made
- Check no unrequested changes occurred

**Did it avoid introducing new issues?**
- No new errors added
- No regression from previous version
- Maintained quality from draft

**Is the final version better than the draft?**
- Improvements are clear
- Original strengths preserved
- Revision added value

### Pass Criteria:
✅ Revision was clean  
✅ Followed exact instructions  
✅ No new issues introduced  
✅ Final version is improved

### Red Flags:
❌ Revision loop (3+ cycles)  
❌ Didn't follow revision request  
❌ New errors introduced  
❌ Final version worse than draft

**Note**: If output requires more than **3 revision cycles**, use the **reset command** (reference Manual 37, Troubleshooting Guide).

---

## 9. Consistency Across Outputs

### Questions to Ask:

**Does the output match the tone and structure of similar documents?**
- Compare to previous outputs of same type
- Check tone consistency with past work
- Verify structural patterns match

**Does it follow system standards?**
- Reference Manual 21 (Operating Charter)
- Reference Manual 27 (Interaction Protocol)
- Reference Manual 24 (Output Standards)
- Check adherence to approved patterns

**Does it avoid drift from previous patterns?**
- No gradual tone changes
- No structural format changes
- No new phrasing conventions without approval

**Is the formatting consistent with organizational norms?**
- Matches internal style guide
- Consistent with brand voice
- Follows organizational formatting standards

### Pass Criteria:
✅ Matches similar documents  
✅ Follows system standards  
✅ No drift detected  
✅ Consistent with org norms

### Red Flags:
❌ Inconsistent with previous work  
❌ Violates system standards  
❌ Shows drift patterns  
❌ Doesn't match org formatting

**Note**: Drift detection is critical. If consistency issues appear across multiple outputs, conduct a **Drift Audit** (reference Manual 47, Audit Framework).

---

## 10. Final Approval Questions

Before approving, confirm **all four criteria pass**:

### 1. Is this clear?
- **Yes**: Easy to understand, well-organized, no confusion
- **No**: Request revision for clarity

### 2. Is this aligned?
- **Yes**: Matches request, correct details, appropriate scope
- **No**: Request revision for alignment

### 3. Is this compliant?
- **Yes**: Stays within boundaries, no restricted domains, escalates correctly
- **No**: **STOP** - Correct boundary violation immediately

### 4. Is this ready to use without further edits?
- **Yes**: Approve and deliver
- **No**: Request revision or reset task

---

## Approval Decision Matrix

| Clear | Aligned | Compliant | Ready | **Decision** |
|-------|---------|-----------|-------|--------------|
| ✅ | ✅ | ✅ | ✅ | **APPROVE** |
| ❌ | ✅ | ✅ | ❌ | Request revision for clarity |
| ✅ | ❌ | ✅ | ❌ | Request revision for alignment |
| ✅ | ✅ | ❌ | ❌ | **STOP** - Fix boundary issue |
| ❌ | ❌ | ✅ | ❌ | Request revision for clarity + alignment |
| Any | Any | ❌ | ❌ | **STOP** - Fix compliance issue first |

**If all answers are YES**, the output is ready for delivery.

---

## Using This Checklist

### Daily Use (Team Leaders)

**When to Use**:
- Before approving any output for delivery
- During weekly spot checks (Manual 47)
- When quality concerns arise

**How to Use**:
1. Read through output once
2. Go through checklist sections 1-10
3. Mark pass (✅) or fail (❌) for each
4. If any section fails, request revision
5. If Section 6 (Boundary Compliance) fails, **stop immediately** and correct

**Time**: 2-5 minutes per output

### Weekly Reviews (Implementation Lead)

**When to Use**:
- Weekly team check-ins (Manual 33)
- Sampling 5-10 outputs for quality

**How to Use**:
1. Select 5-10 recent outputs randomly
2. Apply full checklist to each
3. Track pass/fail rates per section
4. Identify patterns (recurring issues)
5. Document findings in weekly summary

**Time**: 30-45 minutes per week

### Monthly Audits (System Steward)

**When to Use**:
- Monthly role-level audits (Manual 33)
- Performance metrics review (Manual 32)

**How to Use**:
1. Sample 20-30 outputs across teams/users/task types
2. Apply full checklist to each
3. Score outputs using Performance Metrics Framework (Manual 32)
4. Identify drift patterns (Manual 47, Section 3)
5. Document in Monthly Performance Report

**Time**: 60-90 minutes per month

---

## Integration with Other Manuals

This checklist works with:

**Manual 31: QA Checklist** - Foundational 8-step quality gate  
**Manual 32: Performance Metrics Framework** - 6-category scoring system  
**Manual 47: Audit Framework** - Comprehensive audit process  
**Manual 21: Operating Charter** - System purpose and boundaries  
**Manual 25: Safety & Compliance** - 11 restricted domains  
**Manual 27: Interaction Protocol** - 8 communication rules  
**Manual 34: Escalation Protocol** - When to redirect  
**Manual 37: Troubleshooting Guide** - How to fix issues  

---

## Quick Start Guide

### For Beginners (First Week)

**Focus on these 4 sections only**:
1. Task Understanding - Does it match?
2. Clarity & Readability - Is it clear?
3. Boundary Compliance - Is it safe?
4. Final Approval - Is it ready?

**Pass these 4 → Approve**  
**Fail any of these 4 → Request revision**

### For Intermediate Users (After 1 Month)

**Add these 3 sections**:
5. Structure & Formatting - Is it organized?
6. Accuracy & Alignment - Are details correct?
7. Tone & Style - Is tone appropriate?

**Total: 7 sections to check**

### For Advanced Users (After 3 Months)

**Use full checklist (all 10 sections)**:
1. Task Understanding
2. Clarity & Readability
3. Accuracy & Alignment
4. Tone & Style
5. Structure & Formatting
6. Boundary Compliance
7. Escalation Behavior
8. Revision Quality
9. Consistency
10. Final Approval

---

## Checklist Summary

This Quality Assurance Checklist ensures:
- **Clarity** - Output is easy to understand
- **Alignment** - Output matches request
- **Compliance** - Boundaries are respected
- **Quality** - Standards are maintained
- **Consistency** - Patterns are stable
- **Safety** - No violations occur

**Use this checklist every time before approving an output.**

---

## Related Manuals

**Quality & Evaluation**:
- Manual 31: QA Checklist (foundational quality gate)
- Manual 32: Performance Metrics Framework (scoring system)
- Manual 47: Audit Framework (comprehensive audits)

**Governance & Standards**:
- Manual 21: Operating Charter (system purpose and scope)
- Manual 25: Safety & Compliance Addendum (restricted domains)
- Manual 27: Interaction Protocol (communication rules)
- Manual 46: Governance Charter (authority and decision-making)

**Support & Training**:
- Manual 37: Troubleshooting Guide (how to fix issues)
- Manual 38: Command Glossary (how to give clear instructions)

**Complete Framework**: This checklist is part of the 48-manual Action AI framework.

---

## Document History

**v1.0** - December 31, 2025 - Initial release
- Created 10-section practical checklist
- Defined pass criteria and red flags for each section
- Integrated with Performance Metrics (Manual 32) and Audit Framework (Manual 47)
- Provided quick start guide for different user levels
- Established approval decision matrix
