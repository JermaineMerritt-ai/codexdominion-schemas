# DOMINIONMARKETS — COMPLIANCE & SAFETY GUIDE

> **Priority:** Legal compliance and user safety  
> **Jurisdiction:** U.S. SEC regulations (primary), Caribbean markets (secondary)  
> **Review Status:** Requires legal counsel sign-off before launch  
> **Last Updated:** December 24, 2025

---

## ⚖️ REGULATORY LANDSCAPE

### Key Regulations

#### 1. **Securities Exchange Act of 1934 (U.S.)**
- Governs broker-dealers and market data providers
- **Our Position:** We are NOT a broker-dealer (no trades executed)
- **Implication:** We can provide data without broker-dealer registration

#### 2. **Investment Advisers Act of 1940 (U.S.)**
- Governs investment advisory services
- **Our Position:** We do NOT provide investment advice
- **Implication:** We do not require RIA (Registered Investment Adviser) registration

#### 3. **Securities Act of 1933 (U.S.)**
- Governs securities offerings
- **Our Position:** We do not sell securities
- **Implication:** No securities registration required

#### 4. **FINRA Rules (Financial Industry Regulatory Authority)**
- Governs communications about securities
- **Our Position:** We provide factual information, not recommendations
- **Implication:** Must avoid language that could be deemed advisory

#### 5. **Caribbean Financial Regulations**
- Varies by country (Jamaica FSC, Trinidad SEC, etc.)
- **Our Position:** Informational content only
- **Implication:** Monitor as we expand to Caribbean markets

---

## 🚨 WHAT REQUIRES REGISTRATION

### Requires SEC Registration (We AVOID These)
- ❌ **Broker-Dealer:** Executing trades, holding customer funds
- ❌ **Investment Adviser:** Providing personalized investment advice for compensation
- ❌ **Investment Company:** Pooling investor money to buy securities
- ❌ **Transfer Agent:** Maintaining shareholder records

### Does NOT Require Registration (What We Do)
- ✅ **Data Provider:** Aggregating and displaying publicly available market data
- ✅ **Educational Platform:** Teaching about investing concepts
- ✅ **Portfolio Tracker:** Allowing users to manually track their own holdings
- ✅ **News Aggregator:** Displaying news from licensed sources

---

## 🛡️ THE SAFE ZONE — ALLOWED FEATURES

### Category 1: Descriptive Analytics ✅

**What This Means:**
Reporting facts about past and current data without interpretation or recommendations.

**Examples:**

✅ **Allowed:**
- "Your portfolio is 45% technology stocks."
- "Apple increased 3% today."
- "Your largest holding is Microsoft."
- "The S&P 500 is up 1.2% this week."
- "Your portfolio gained $500 this month."
- "You added 3 positions in December."

❌ **Not Allowed:**
- "Your portfolio is too heavy in tech." (Judgment)
- "Apple is a good buy at this price." (Advice)
- "You should reduce your Microsoft position." (Recommendation)
- "The S&P 500 will continue rising." (Prediction)
- "Your portfolio is underperforming. Rebalance." (Advisory)
- "You should add more positions." (Recommendation)

---

### Category 2: Visualization ✅

**What This Means:**
Presenting data in charts, graphs, and visual formats without editorial commentary.

**Allowed:**
- Pie charts showing sector allocation
- Line charts showing price history
- Bar charts comparing performance
- Heatmaps showing sector movements
- Tables listing holdings

**Key Rule:**
Charts must be labeled factually, not prescriptively.

✅ "Your Sector Allocation"  
❌ "Your Sector Allocation is Unbalanced"

✅ "Apple Price History (6 Months)"  
❌ "Apple is Trending Upward"

---

### Category 3: Alerts ✅

**What This Means:**
Notifying users of factual events based on criteria they set.

**Allowed:**
- Price crosses threshold: "AAPL crossed $200"
- Volume spike: "AAPL volume exceeded 100M shares"
- News event: "News published mentioning AAPL"
- Earnings date: "AAPL earnings announced tomorrow"
- Percentage change: "AAPL moved 5% today"

**Not Allowed:**
- "Buy AAPL now, price is low"
- "Sell AAPL before it drops"
- "AAPL is about to break out"
- "AAPL is overvalued"

**Key Rule:**
Alerts report events, they don't suggest actions.

---

### Category 4: AI Summaries (Safe) ✅

**What This Means:**
Using GPT-4 or similar models to generate text summaries of user data.

**Safe AI Use Cases:**

✅ **Portfolio Summary:**
> "Your portfolio has 15 holdings across 8 sectors. Technology is your largest sector at 40%. Your portfolio value increased 2% this week. You made 2 trades this month."

✅ **Market Summary:**
> "The S&P 500 gained 1.5% today. Technology led gains at 2.3%. Energy declined 0.8%. 350 stocks advanced, 150 declined."

✅ **News Summary:**
> "Three sources report Apple announced new product. Bloomberg and Reuters published within 5 minutes. CNBC followed 10 minutes later. All sources confirm product launch date."

**Not Allowed:**

❌ **Predictive AI:**
> "AI predicts AAPL will reach $250 by year-end."

❌ **Advisory AI:**
> "AI recommends rebalancing your portfolio to reduce risk."

❌ **Evaluative AI:**
> "AI rates AAPL as a 'strong buy' based on fundamentals."

**Implementation Safety:**
1. **System Prompt Constraints:**
   - "You are a descriptive financial data summarizer."
   - "Never make predictions about future performance."
   - "Never recommend buy, sell, or hold actions."
   - "Only report factual data and calculations."

2. **Template-Based Responses:**
   - Pre-write 50+ safe summary templates
   - AI fills in variables (percentages, dollar amounts)
   - Less open-ended = more control

3. **Output Filtering:**
   - Regex filters block advisory keywords
   - Flag outputs containing: "should," "recommend," "will," "predict," "buy," "sell"
   - Human review flagged outputs

4. **Regular Audits:**
   - Sample 100 AI outputs weekly
   - Legal review quarterly
   - User reporting system for inappropriate responses

---

## 🚫 THE DANGER ZONE — PROHIBITED FEATURES

### Category 1: Recommendations ❌

**What This Means:**
Suggesting specific buy, sell, or hold actions.

**Examples:**

❌ "You should buy AAPL."  
❌ "Consider selling TSLA."  
❌ "Now is a good time to invest in tech."  
❌ "Rebalance your portfolio."  
❌ "Increase your cash position."  
❌ "Reduce exposure to this sector."

**Why Prohibited:**
This is investment advice. Requires RIA registration.

---

### Category 2: Predictions ❌

**What This Means:**
Forecasting future stock prices, market movements, or outcomes.

**Examples:**

❌ "AAPL will reach $250 by Q4."  
❌ "Tech stocks are about to rally."  
❌ "The market will decline next week."  
❌ "This stock is undervalued and will rise."  
❌ "Expect a correction in the next month."

**Why Prohibited:**
Creates liability if prediction is wrong. Can be construed as advice.

---

### Category 3: Evaluations ❌

**What This Means:**
Judging whether a stock is "good," "bad," "overvalued," "undervalued," etc.

**Examples:**

❌ "AAPL is a great investment."  
❌ "TSLA is overpriced."  
❌ "This stock is undervalued."  
❌ "Strong buy on this position."  
❌ "Avoid this sector."

**Why Prohibited:**
Evaluation implies recommendation. Crosses into advisory territory.

---

### Category 4: Personalized Advice ❌

**What This Means:**
Tailoring recommendations to an individual user's situation.

**Examples:**

❌ "Based on your risk tolerance, buy bonds."  
❌ "You're young, so invest aggressively."  
❌ "Your portfolio needs more diversification."  
❌ "Consider your tax situation before selling."

**Why Prohibited:**
This is the definition of investment advice. Absolutely requires RIA registration.

---

### Category 5: Performance Guarantees ❌

**What This Means:**
Implying or promising future returns.

**Examples:**

❌ "Earn 15% annual returns with this portfolio."  
❌ "Beat the market using our strategies."  
❌ "Guaranteed safe investments."  
❌ "This approach will make you rich."

**Why Prohibited:**
Illegal under SEC rules. No one can guarantee investment returns.

---

## 📋 COMPLIANCE CHECKLIST

Every feature must pass all 10 checks before launch:

### 1. ✅ Language Review
- [ ] No words: "should," "must," "recommend," "advise," "will," "predict," "buy," "sell," "hold"
- [ ] All text is descriptive, not prescriptive
- [ ] Past tense or present tense only (not future tense)

### 2. ✅ Disclaimer Visibility
- [ ] Footer disclaimer on every page
- [ ] Disclaimer above any AI-generated content
- [ ] First-time user sees full disclaimer and must acknowledge

### 3. ✅ Data Attribution
- [ ] Source clearly visible on all data
- [ ] Timestamp shown for all prices/data
- [ ] "As of [timestamp]" label on all metrics

### 4. ✅ No Personalization
- [ ] Features work the same for everyone
- [ ] No "based on your profile" language
- [ ] No tailored recommendations

### 5. ✅ Educational Context
- [ ] Tooltips explain what metrics mean
- [ ] Glossary available for financial terms
- [ ] "Learn more" links for complex concepts

### 6. ✅ User Control
- [ ] User manually enters portfolio data (no auto-import from brokerages)
- [ ] User sets alert criteria (we don't suggest thresholds)
- [ ] User builds watchlists (we don't recommend stocks to watch)

### 7. ✅ AI Output Safety
- [ ] System prompts enforce neutral tone
- [ ] Output filtering blocks advisory keywords
- [ ] Human review samples weekly

### 8. ✅ External Links
- [ ] News links to original source (not our editorialized version)
- [ ] "You are leaving DominionMarkets" notice for external links
- [ ] No affiliate links to brokerages

### 9. ✅ No Trade Execution
- [ ] Platform cannot execute trades
- [ ] No integrations with brokerages for trading
- [ ] Clear statement: "We are not a broker"

### 10. ✅ Legal Review
- [ ] SEC attorney reviews feature before launch
- [ ] Quarterly compliance audits
- [ ] User agreement includes arbitration clause

---

## 🛠️ IMPLEMENTATION SAFEGUARDS

### 1. System-Level Blocks

**Keyword Blocklist:**
Automatically reject any text (user-generated or AI) containing:
- "buy," "sell," "hold," "trade," "invest in"
- "should," "must," "recommend," "advise," "suggest"
- "will," "going to," "expect," "predict," "forecast"
- "good investment," "bad investment," "undervalued," "overvalued"
- "strong buy," "weak buy," "strong sell"

**Regex Filters:**
```python
PROHIBITED_PATTERNS = [
    r"\b(should|must|need to)\s+(buy|sell|hold|trade)",
    r"\b(will|going to|expect)\s+\w+\s+(rise|fall|increase|decrease)",
    r"\b(recommend|advise|suggest)\s+\w+",
    r"\b(good|great|excellent|poor|bad)\s+(investment|stock|buy)",
]
```

---

### 2. Human Review Workflow

**Pre-Launch:**
- Every feature reviewed by in-house compliance officer
- External SEC attorney provides written approval
- User flows tested for unintended advisory language

**Post-Launch:**
- Weekly random sample of 100 AI outputs
- Monthly review of user feedback/reports
- Quarterly external legal audit

---

### 3. User Reporting System

**How It Works:**
- "Report a problem" button on every page
- Users can flag content they believe is advisory
- Reported content reviewed within 24 hours
- Immediate removal if advisory language confirmed

---

### 4. Disclaimer System

**Mandatory Disclaimers:**

**Site-Wide Footer (Every Page):**
> "DominionMarkets provides financial information for educational purposes only. We do not provide investment advice, recommendations, or predictions. All investment decisions are your responsibility. Past performance does not guarantee future results. Consult a licensed financial advisor before making investment decisions."

**First Login (One-Time Acknowledgment):**
> "Welcome to DominionMarkets. Before you continue, please acknowledge:
> 
> ✓ I understand DominionMarkets is not a financial advisor.
> ✓ I understand all information is for educational purposes only.
> ✓ I understand I am responsible for my own investment decisions.
> ✓ I understand I should consult a licensed advisor before investing.
> 
> [I Agree] [Cancel]"

**AI-Generated Content (Appears Above Every AI Summary):**
> "⚠️ AI-generated summary. For informational purposes only. Not investment advice."

**Portfolio Tracker (Appears on Portfolio Page):**
> "This tracker is for informational purposes only. We do not store brokerage credentials. We do not provide investment advice."

---

## 🌍 INTERNATIONAL COMPLIANCE

### Caribbean Markets

**Jamaica (FSC - Financial Services Commission):**
- Similar regulations to U.S.
- Information providers generally do not require licensing
- Monitor for changes as we expand

**Trinidad & Tobago (SEC):**
- Must register if providing "investment advice"
- Our purely informational model likely exempt
- Consult local attorney before launch

**Barbados (FSC):**
- Similar framework to Jamaica
- Informational platforms typically exempt

**Action Plan:**
- Engage local legal counsel in each Caribbean market
- Register only if required (likely not for informational platform)
- Adapt disclaimers to local regulatory language

---

### European Union (GDPR)

**If Serving EU Users:**
- Data privacy compliance (GDPR)
- Right to be forgotten
- Explicit consent for data collection
- MiFID II regulations for investment services (we're exempt if purely informational)

**Action Plan:**
- Cookie consent banner
- Privacy policy aligned with GDPR
- Data deletion workflow
- Geo-block EU if compliance cost too high initially

---

## 📞 WHEN TO CONSULT LEGAL COUNSEL

**Immediate Legal Review Required For:**
1. Any new feature involving recommendations or advice
2. Any AI model generating open-ended text about stocks
3. Any partnership with brokerages or financial institutions
4. Any paid promotions or sponsored content about stocks
5. Any user-generated content marketplace (creator courses)
6. Any expansion into new geographic markets
7. Any regulatory inquiry or complaint

**Annual Legal Audit Required For:**
- Full platform feature review
- Disclaimer updates (regulations change)
- Terms of service updates
- Privacy policy compliance

---

## 🚨 INCIDENT RESPONSE PLAN

### If We Receive Regulatory Inquiry

**Step 1: Immediate Response (Same Day)**
- Notify CEO and legal counsel immediately
- Do not respond to regulator without attorney present
- Preserve all relevant documents and communications

**Step 2: Investigation (Within 3 Days)**
- Identify feature or content in question
- Review compliance checklist for that feature
- Assess if violation occurred

**Step 3: Remediation (Within 7 Days)**
- If violation confirmed, disable feature immediately
- Draft response with attorney
- Implement corrective measures

**Step 4: Prevention (Within 30 Days)**
- Update compliance checklist
- Retrain team on prohibited language
- Implement additional safeguards

---

## 🎓 TEAM TRAINING

### Mandatory Compliance Training (All Team Members)

**Module 1: Understanding Advice vs. Information**
- 30 examples of allowed vs. prohibited language
- Quiz: 20 questions (must score 90%+)

**Module 2: AI Safety**
- How to write system prompts that enforce compliance
- How to review AI outputs for advisory language
- When to escalate to legal

**Module 3: User Interactions**
- How to respond to user questions without giving advice
- How to redirect users to licensed advisors
- How to document interactions

**Frequency:**
- Initial training before platform access
- Quarterly refresher
- Immediate re-training if incident occurs

---

## ✅ SAFE LANGUAGE CHEAT SHEET

### Replace Advisory Language With Descriptive Language

| ❌ Don't Say | ✅ Do Say |
|-------------|----------|
| "You should buy this stock." | "This stock increased 5% today." |
| "Your portfolio needs diversification." | "Your portfolio has 3 holdings." |
| "This is a good investment." | "This stock's P/E ratio is 15." |
| "Sell before it drops." | "This stock declined 10% this week." |
| "Rebalance to reduce risk." | "Your tech allocation is 60%." |
| "This stock will rise." | "This stock rose 20% this year." |
| "Undervalued opportunity." | "P/E ratio is below sector average." |
| "Strong buy rating." | "10 analysts rate 'buy', 5 rate 'hold'." |
| "Avoid this sector." | "This sector declined 5% this month." |
| "Perfect time to invest." | "Market is at 52-week high." |

---

## 📜 LEGAL DOCUMENTS REQUIRED

### 1. Terms of Service
- User agreement to all disclaimers
- Arbitration clause (avoid class action lawsuits)
- Limitation of liability
- Intellectual property rights

### 2. Privacy Policy
- Data collection practices
- How data is used
- Third-party data sharing (APIs)
- User rights (deletion, export)

### 3. Disclaimer Notice
- Full legal disclaimer (expanded version of footer)
- Risks of investing
- Our non-advisory status

### 4. Cookie Policy
- What cookies we use
- How to opt out
- Third-party cookies (analytics)

---

## 🔒 DATA SECURITY & PRIVACY

### What We Store
- User account information (email, password hash)
- Portfolio data (manually entered by user)
- Watchlists
- Alertpreferences
- Usage analytics (anonymized)

### What We DON'T Store
- Brokerage login credentials (we don't integrate with brokerages)
- Social Security Numbers
- Bank account information
- Payment card numbers (Stripe handles payments)

### Security Measures
- Encryption at rest (AES-256)
- Encryption in transit (TLS 1.3)
- Regular security audits
- Penetration testing annually
- SOC 2 compliance (if handling sensitive data)

---

## 💰 ADVERTISING & SPONSORSHIPS (HIGH RISK)

### Prohibited
- ❌ Paid stock promotions
- ❌ "Featured stock" for payment
- ❌ Sponsored "buy" recommendations
- ❌ Affiliate links to brokerages based on stock picks

### Allowed (With Disclosure)
- ✅ Display ads (Google AdSense) - generic, not stock-specific
- ✅ Course sponsorships (creator-funded, not stock-related)
- ✅ Platform tool sponsorships (e.g., "Powered by [Data Provider]")

**Key Rule:**
If money changes hands related to a specific stock, it's prohibited.

---

## 📊 COMPLIANCE METRICS TO TRACK

### Monthly Dashboard
- Number of AI outputs flagged for review: Target <1%
- User reports of advisory language: Target 0
- Features requiring legal review: Track all
- Disclaimer acknowledgment rate: Target 100%
- Terms of service acceptance rate: Target 100%

### Quarterly Review
- External legal audit results
- Regulatory landscape changes
- Team compliance training completion: Target 100%
- Incident count: Target 0

---

**🔥 Compliance is not optional. It's the foundation of trust. Build safe, or don't build at all.** ⚖️

**Status:** DRAFT — Requires SEC attorney review before implementation  
**Next Steps:** Engage legal counsel, finalize disclaimers, implement safeguards  
**Launch Blocker:** Yes — Cannot launch without legal sign-off
