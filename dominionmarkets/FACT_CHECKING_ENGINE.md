# DOMINIONMARKETS — FACT-CHECKING ENGINE BLUEPRINT

> **Purpose:** Multi-source verification system for financial news  
> **Goal:** Build trust through transparency and cross-verification  
> **Status:** Technical specification for development

---

## 🎯 SYSTEM OVERVIEW

### The Problem
Financial news is fragmented, sometimes contradictory, and occasionally misleading. Users need a way to verify information before making decisions.

### The Solution
A fact-checking engine that:
1. Aggregates news from multiple reputable sources
2. Compares stories for consistency
3. Flags discrepancies and conflicts
4. Shows verification status with transparency
5. Provides source attribution and timestamps

### Core Principle
**"We don't determine truth. We show you what multiple sources say."**

---

## 🏗️ ARCHITECTURE

### Component 1: News Aggregator

**Function:** Pull financial news headlines from multiple sources

**Data Sources (Prioritized):**
1. **Tier 1 (Most Trusted):**
   - Bloomberg API
   - Reuters API
   - Associated Press (AP)
   - Wall Street Journal API

2. **Tier 2 (Major Outlets):**
   - CNBC API
   - Yahoo Finance API
   - MarketWatch
   - Financial Times

3. **Tier 3 (Caribbean Sources):**
   - Jamaica Observer (Business section)
   - Trinidad Guardian (Business)
   - Caribbean Business Report
   - Regional stock exchange announcements

**Technical Implementation:**
```python
class NewsAggregator:
    def __init__(self):
        self.sources = {
            'bloomberg': BloombergAPI(),
            'reuters': ReutersAPI(),
            'cnbc': CNBCAPI(),
            'yahoo': YahooFinanceAPI(),
            'caribbean': CaribbeanNewsAPI()
        }
    
    def fetch_news(self, symbol=None, keywords=None, limit=50):
        """
        Fetch news from all sources
        Returns: List of articles with metadata
        """
        articles = []
        for source_name, api in self.sources.items():
            try:
                results = api.get_news(symbol=symbol, keywords=keywords)
                for article in results:
                    articles.append({
                        'id': generate_id(),
                        'source': source_name,
                        'title': article.title,
                        'summary': article.summary,
                        'url': article.url,
                        'published_at': article.published_at,
                        'author': article.author,
                        'symbol': symbol
                    })
            except Exception as e:
                logger.error(f"Error fetching from {source_name}: {e}")
        
        return articles
```

**Rate Limiting:**
- Bloomberg: 100 calls/day (free tier)
- Reuters: 50 calls/day
- Yahoo Finance: Unlimited (unofficial API, monitor for changes)

**Caching:**
- Cache news for 15 minutes (reduce API calls)
- Background job refreshes cache every 10 minutes

---

### Component 2: Story Clustering

**Function:** Group articles about the same event/topic

**Algorithm:**
1. **Title Similarity:** Levenshtein distance or cosine similarity
2. **Entity Extraction:** Identify companies, people, dates mentioned
3. **Temporal Proximity:** Published within same 4-hour window
4. **Keyword Overlap:** Share 60%+ of keywords

**Technical Implementation:**
```python
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class StoryClustering:
    def __init__(self):
        self.vectorizer = TfidfVectorizer()
    
    def cluster_articles(self, articles):
        """
        Group articles about the same story
        Returns: List of article clusters
        """
        # Extract titles
        titles = [a['title'] for a in articles]
        
        # Vectorize
        tfidf_matrix = self.vectorizer.fit_transform(titles)
        
        # Calculate similarity
        similarity_matrix = cosine_similarity(tfidf_matrix)
        
        # Cluster (threshold: 0.6 similarity)
        clusters = []
        visited = set()
        
        for i, article in enumerate(articles):
            if i in visited:
                continue
            
            cluster = [article]
            visited.add(i)
            
            for j in range(i + 1, len(articles)):
                if similarity_matrix[i][j] >= 0.6:
                    cluster.append(articles[j])
                    visited.add(j)
            
            clusters.append(cluster)
        
        return clusters
```

---

### Component 3: Source Comparison

**Function:** Compare what different sources say about the same story

**Checks:**
1. **Consistency:** Do sources agree on key facts?
2. **Conflicts:** Do sources contradict each other?
3. **Missing Details:** Does one source have info others don't?
4. **Timing:** Which source published first?

**Key Facts Extraction:**
- Company names (using NER - Named Entity Recognition)
- Numbers (stock prices, percentages, dollar amounts)
- Dates (announcement dates, effective dates)
- Quotes (from company executives)

**Technical Implementation:**
```python
import spacy

nlp = spacy.load("en_core_web_sm")

class SourceComparison:
    def compare_stories(self, cluster):
        """
        Compare articles in a cluster
        Returns: Comparison report
        """
        entities_by_source = {}
        numbers_by_source = {}
        
        for article in cluster:
            doc = nlp(article['summary'])
            
            # Extract entities (companies, people, locations)
            entities = [ent.text for ent in doc.ents if ent.label_ in ['ORG', 'PERSON', 'GPE']]
            entities_by_source[article['source']] = entities
            
            # Extract numbers (prices, percentages)
            numbers = self.extract_numbers(article['summary'])
            numbers_by_source[article['source']] = numbers
        
        # Check for conflicts
        conflicts = self.find_conflicts(numbers_by_source)
        
        # Check for consistency
        consistency_score = self.calculate_consistency(entities_by_source, numbers_by_source)
        
        return {
            'entities': entities_by_source,
            'numbers': numbers_by_source,
            'conflicts': conflicts,
            'consistency_score': consistency_score
        }
    
    def extract_numbers(self, text):
        """Extract dollar amounts, percentages, dates"""
        import re
        
        # Match patterns: $1.5B, 5%, etc.
        patterns = {
            'dollar': r'\$\d+\.?\d*[BMK]?',
            'percentage': r'\d+\.?\d*%',
            'date': r'\d{1,2}/\d{1,2}/\d{4}'
        }
        
        extracted = {}
        for key, pattern in patterns.items():
            matches = re.findall(pattern, text)
            extracted[key] = matches
        
        return extracted
    
    def find_conflicts(self, numbers_by_source):
        """Identify numerical conflicts between sources"""
        conflicts = []
        
        # Example: Source A says "$1.5B", Source B says "$1.2B"
        # Flag as conflict if difference > 10%
        
        return conflicts
```

---

### Component 4: Reliability Indicators

**Function:** Show users how verified a story is

**Verification Levels:**

**1. ✅ Confirmed (Green)**
- 3+ Tier 1 sources report same key facts
- No conflicts detected
- Published within 30 minutes of each other

**2. ⚠️ Partially Verified (Yellow)**
- 2 sources report same facts
- OR: 3+ sources but minor discrepancies
- OR: Only 1 Tier 1 source

**3. ⚠️ Unverified (Coral)**
- Only 1 source reports story
- OR: Sources conflict significantly
- OR: Developing story (facts still emerging)

**4. ❌ Conflicting (Red)**
- Sources report contradictory information
- User should wait for more information

**Technical Implementation:**
```python
class ReliabilityIndicator:
    def calculate_reliability(self, cluster, comparison):
        """
        Determine verification level
        Returns: 'confirmed', 'partial', 'unverified', 'conflicting'
        """
        num_sources = len(cluster)
        consistency = comparison['consistency_score']
        conflicts = len(comparison['conflicts'])
        
        # Tier 1 sources count
        tier1_count = sum(1 for a in cluster if a['source'] in ['bloomberg', 'reuters', 'ap'])
        
        # Decision tree
        if conflicts > 2:
            return 'conflicting'
        
        if tier1_count >= 3 and consistency >= 0.8:
            return 'confirmed'
        
        if num_sources >= 2 and consistency >= 0.6:
            return 'partial'
        
        if num_sources == 1:
            return 'unverified'
        
        return 'partial'  # Default
```

---

### Component 5: AI Summary (Safe)

**Function:** Generate human-readable summary of verification status

**GPT-4 System Prompt:**
```
You are a financial news fact-checker. Your role is to summarize what multiple sources say about a news story. You are DESCRIPTIVE ONLY.

Rules:
1. Report how many sources confirm key facts
2. Identify any conflicts between sources
3. Note if story is developing (facts still emerging)
4. Never interpret or judge the news
5. Never predict what will happen next
6. Always cite sources

Example output:
"Three sources confirm Apple announced a new product today. Bloomberg reported at 10:00 AM, Reuters at 10:05 AM, and CNBC at 10:10 AM. All three sources agree on the product name and release date. Bloomberg and Reuters report the price as $999, while CNBC has not yet mentioned price."
```

**Technical Implementation:**
```python
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class AINewsSummarizer:
    def summarize_verification(self, cluster, comparison, reliability):
        """
        Generate AI summary of verification status
        """
        # Prepare context
        sources_list = [f"{a['source']} ({a['published_at']})" for a in cluster]
        
        prompt = f"""
        Summarize the verification status of this news story:
        
        Sources reporting: {', '.join(sources_list)}
        Reliability level: {reliability}
        Key facts extracted: {comparison['entities']}
        Conflicts detected: {comparison['conflicts']}
        
        Generate a clear, factual summary of what sources say.
        """
        
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": FACT_CHECKER_SYSTEM_PROMPT},
                {"role": "user", "content": prompt}
            ],
            max_tokens=200,
            temperature=0.3  # Low temperature = more factual
        )
        
        summary = response.choices[0].message.content
        
        # Filter for compliance
        if self.contains_prohibited_language(summary):
            return "Summary unavailable (compliance filter triggered)."
        
        return summary
```

---

### Component 6: Transparency Layer

**Function:** Show all sources and let users judge for themselves

**Displayed Information:**
- Source name (with logo)
- Publication timestamp ("2m ago", "15m ago")
- Article headline (linked to original source)
- Snippet (first 2 sentences)
- Author name (if available)

**UI Mockup:**
```
┌────────────────────────────────────────────┐
│ ✅ Confirmed by 3 sources                  │
│                                            │
│ Apple announces new product                │
│                                            │
│ Sources:                                   │
│                                            │
│ 📰 Bloomberg | 10:00 AM | 2 hours ago     │
│    "Apple Inc. announced..."               │
│    By Mark Gurman                          │
│    [Read Full Article ↗]                   │
│                                            │
│ 📰 Reuters | 10:05 AM | 2 hours ago       │
│    "Tech giant Apple unveiled..."          │
│    By Stephen Nellis                       │
│    [Read Full Article ↗]                   │
│                                            │
│ 📰 CNBC | 10:10 AM | 2 hours ago          │
│    "In a surprise announcement..."         │
│    By Kif Leswing                          │
│    [Read Full Article ↗]                   │
│                                            │
│ AI Summary:                                │
│ "Three sources confirm Apple announced..." │
│ [Show More]                                │
└────────────────────────────────────────────┘
```

---

## 📊 DATABASE SCHEMA

### Tables

**1. `articles`**
```sql
CREATE TABLE articles (
    id UUID PRIMARY KEY,
    source VARCHAR(50) NOT NULL,
    title TEXT NOT NULL,
    summary TEXT,
    url TEXT UNIQUE NOT NULL,
    published_at TIMESTAMP NOT NULL,
    fetched_at TIMESTAMP DEFAULT NOW(),
    author VARCHAR(255),
    symbol VARCHAR(10),  -- e.g., 'AAPL'
    keywords TEXT[],
    created_at TIMESTAMP DEFAULT NOW()
);
```

**2. `article_clusters`**
```sql
CREATE TABLE article_clusters (
    id UUID PRIMARY KEY,
    story_title VARCHAR(255),
    reliability_level VARCHAR(20),  -- 'confirmed', 'partial', 'unverified', 'conflicting'
    consistency_score FLOAT,
    num_sources INT,
    first_published TIMESTAMP,
    created_at TIMESTAMP DEFAULT NOW()
);
```

**3. `cluster_articles`** (Junction Table)
```sql
CREATE TABLE cluster_articles (
    cluster_id UUID REFERENCES article_clusters(id),
    article_id UUID REFERENCES articles(id),
    PRIMARY KEY (cluster_id, article_id)
);
```

**4. `verification_reports`**
```sql
CREATE TABLE verification_reports (
    id UUID PRIMARY KEY,
    cluster_id UUID REFERENCES article_clusters(id),
    ai_summary TEXT,
    conflicts JSONB,  -- Store conflicts as JSON
    key_facts JSONB,  -- Extracted entities and numbers
    generated_at TIMESTAMP DEFAULT NOW()
);
```

---

## 🔄 WORKFLOW

### Step-by-Step Process

**1. News Ingestion (Every 10 Minutes)**
```
Background Job:
1. Fetch news from all sources
2. Store in `articles` table
3. Trigger clustering job
```

**2. Story Clustering (Every 15 Minutes)**
```
Background Job:
1. Query all articles from last 24 hours
2. Run clustering algorithm
3. Create entries in `article_clusters`
4. Link articles to clusters in `cluster_articles`
```

**3. Source Comparison (Triggered After Clustering)**
```
Background Job:
1. For each new cluster
2. Extract key facts from all articles
3. Identify conflicts
4. Calculate consistency score
5. Determine reliability level
```

**4. AI Summary Generation (Triggered After Comparison)**
```
Background Job:
1. Generate AI summary using GPT-4
2. Store in `verification_reports`
3. Flag for human review if sensitive
```

**5. User Request (Real-Time)**
```
User clicks "AAPL" news:
1. Query `article_clusters` WHERE symbol='AAPL'
2. Join with `articles` to get all sources
3. Join with `verification_reports` to get AI summary
4. Return formatted response to frontend
```

---

## 🎨 FRONTEND COMPONENTS

### Component 1: News Feed

**Location:** DominionMarkets homepage, stock detail pages

**Features:**
- List of clustered stories (most recent first)
- Verification badge (✅ ⚠️ ❌)
- Snippet preview
- "Show Sources" expandable section

---

### Component 2: Story Detail Modal

**Opens When:** User clicks on a news story

**Content:**
- Full story cluster details
- All sources listed with timestamps
- AI summary (with disclaimer)
- Conflicts highlighted (if any)
- "Still developing?" indicator

---

### Component 3: Source Filter

**Allows User To:**
- Filter by source ("Show only Bloomberg + Reuters")
- Filter by reliability level ("Show only confirmed stories")
- Filter by recency ("Last 24 hours")

---

## 🛡️ COMPLIANCE SAFEGUARDS

### 1. No Editorial Commentary
- AI summaries are descriptive only
- No interpretation of "what this means"
- No predictions based on news

### 2. Source Attribution
- Every headline links to original source
- No hosting of full articles (copyright compliance)
- Clear labeling of source tier

### 3. Disclaimer
> "DominionMarkets aggregates news from multiple sources for informational purposes. We do not verify facts independently. Always consult original sources before making decisions."

---

## 📈 SUCCESS METRICS

### Trust Metrics
- User clicks "View Sources": 60%+ of story views
- User report of "misleading summary": <1%
- User satisfaction score (survey): 4.5+/5

### Engagement Metrics
- News stories clicked: 10,000+/month
- Average stories viewed per session: 5+
- Time spent reading news: 3+ minutes/session

### Technical Metrics
- Story clustering accuracy: 85%+
- Source fetch uptime: 99%+
- AI summary generation time: <3 seconds

---

## 🚀 ROLLOUT PLAN

### Phase 1: MVP (Month 1-2)
- 5 news sources (Bloomberg, Reuters, CNBC, Yahoo, 1 Caribbean source)
- Basic clustering (title similarity only)
- Simple verification badges (confirmed/unverified)
- No AI summaries (just source list)

### Phase 2: Enhanced (Month 3-4)
- 10+ news sources
- Advanced clustering (entity extraction)
- AI summaries (GPT-4 integration)
- Conflict detection

### Phase 3: Full Feature (Month 5-6)
- All planned sources
- Real-time clustering
- User reporting system
- Mobile app integration

---

## 💰 COST ESTIMATE

### API Costs (Monthly)
- Bloomberg API: $500-1,000 (depending on tier)
- Reuters API: $300-600
- OpenAI GPT-4: $200-500 (based on 10K summaries/month)
- Infrastructure (AWS/GCP): $100-200

**Total: $1,100-2,300/month**

### Break-Even
- Need 110-230 premium subscribers ($9.99/month)
- Or 55-115 pro subscribers ($19.99/month)
- Achievable by Month 6 based on roadmap projections

---

**🔥 Trust is built one verified fact at a time. The fact-checking engine is the cornerstone of DominionMarkets credibility.** ✅

**Status:** BLUEPRINT COMPLETE ✅  
**Next Steps:** Technical spec review, API vendor selection, MVP development  
**Launch Target:** Phase 1 in Q2 2025
