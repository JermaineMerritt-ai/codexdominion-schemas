"""
AI Services
OpenAI and Anthropic API integrations for content generation
"""
import os
import json
from typing import Dict, List, Optional
import ai_prompts

# AI Provider Configuration
AI_PROVIDER = os.environ.get('AI_PROVIDER', 'openai')  # 'openai' or 'anthropic'
AI_MODEL = os.environ.get('AI_MODEL', 'gpt-4o-mini')
OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
ANTHROPIC_API_KEY = os.environ.get('ANTHROPIC_API_KEY')

# Lazy import AI clients
_openai_client = None
_anthropic_client = None

def get_openai_client():
    """Get or create OpenAI client"""
    global _openai_client
    if _openai_client is None:
        if not OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY environment variable not set")
        try:
            from openai import OpenAI
            _openai_client = OpenAI(api_key=OPENAI_API_KEY)
        except ImportError:
            raise ImportError("openai package not installed. Run: pip install openai")
    return _openai_client

def get_anthropic_client():
    """Get or create Anthropic client"""
    global _anthropic_client
    if _anthropic_client is None:
        if not ANTHROPIC_API_KEY:
            raise ValueError("ANTHROPIC_API_KEY environment variable not set")
        try:
            import anthropic
            _anthropic_client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
        except ImportError:
            raise ImportError("anthropic package not installed. Run: pip install anthropic")
    return _anthropic_client

def call_ai_model(prompt: str, system_prompt: Optional[str] = None, model: Optional[str] = None) -> str:
    """
    Call AI model (OpenAI or Anthropic) with prompt

    Args:
        prompt (str): User prompt
        system_prompt (str): Optional system prompt
        model (str): Model name override

    Returns:
        str: AI-generated response
    """
    provider = AI_PROVIDER
    model = model or AI_MODEL

    try:
        if provider == 'openai':
            client = get_openai_client()

            messages = []
            if system_prompt:
                messages.append({"role": "system", "content": system_prompt})
            messages.append({"role": "user", "content": prompt})

            response = client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=0.7,
                max_tokens=2000
            )

            return response.choices[0].message.content

        elif provider == 'anthropic':
            client = get_anthropic_client()

            response = client.messages.create(
                model=model or "claude-3-5-sonnet-20241022",
                max_tokens=2000,
                temperature=0.7,
                system=system_prompt or "",
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )

            return response.content[0].text

        else:
            raise ValueError(f"Unknown AI provider: {provider}")

    except Exception as e:
        print(f"AI API error: {e}")
        return f"AI analysis unavailable: {str(e)}"

# Stock Analysis
def run_stock_analysis(ticker: str, company_name: str, metrics: Dict) -> str:
    """
    Generate AI stock analysis

    Args:
        ticker (str): Stock ticker
        company_name (str): Company name
        metrics (dict): Stock metrics (price, sector, fundamentals, volatility, risk_profile)

    Returns:
        str: AI-generated analysis
    """
    # Load prompt template
    prompt_template = ai_prompts.load_prompt('stock_analyst')

    # Format prompt with data
    prompt = f"""Analyze this stock using the following framework:

STOCK: {ticker} - {company_name}
PRICE: ${metrics.get('price', 0):.2f}
SECTOR: {metrics.get('sector', 'Unknown')}
MARKET CAP: ${metrics.get('market_cap', 0):,.0f}
P/E RATIO: {metrics.get('pe_ratio', 'N/A')}

FUNDAMENTALS:
- Revenue Trend: {metrics.get('revenue_trend', 'unknown')}
- Net Income Trend: {metrics.get('net_income_trend', 'unknown')}
- Debt Level: {metrics.get('debt_level', 'unknown')}
- Profit Margins: {metrics.get('profit_margin_strength', 'unknown')}

VOLATILITY: {metrics.get('volatility', 'medium')}
USER RISK PROFILE: {metrics.get('user_risk_profile', 'moderate')}

Follow the analysis framework in the template and provide:
1. Company description (2-3 sentences)
2. Financial trends analysis
3. 2 bullish reasons
4. 2 bearish concerns
5. Risk classification
6. Portfolio fit guidance
7. Plain-English summary
8. Disclaimer

CRITICAL: No financial advice, no price targets, no buy/sell directives."""

    # Get compliance system prompt
    compliance_prompt = """You are an educational investment analysis assistant.
Your role is to TEACH and INFORM, never to ADVISE or PREDICT.

NEVER:
- Give financial advice
- Provide price targets
- Tell users to buy or sell
- Make guarantees about returns

ALWAYS:
- Focus on education
- Present multiple perspectives
- Highlight risks
- Use self-directed language ("consider whether...")
- Include disclaimers"""

    return call_ai_model(prompt, system_prompt=compliance_prompt)

# Portfolio Analysis
def run_portfolio_analysis(
    portfolio_name: str,
    risk_profile: str,
    holdings: List[Dict],
    summary_metrics: Dict
) -> str:
    """
    Generate AI portfolio health analysis

    Args:
        portfolio_name (str): Portfolio name
        risk_profile (str): Risk profile (conservative/moderate/aggressive)
        holdings (list): List of holding dicts
        summary_metrics (dict): Summary metrics

    Returns:
        str: AI-generated analysis
    """
    # Load prompt template
    prompt_template = ai_prompts.load_prompt('portfolio_analyst')

    # Format holdings data
    holdings_text = "\n".join([
        f"- {h['ticker']}: {h['shares']} shares @ ${h['price']:.2f} = ${h['value']:,.2f} ({h['weight']:.1f}%)"
        for h in holdings
    ])

    # Format sector breakdown
    sectors = summary_metrics.get('sector_concentration', {})
    sector_text = "\n".join([f"- {sector}: {weight:.1f}%" for sector, weight in sectors.items()])

    prompt = f"""Analyze this portfolio using the following framework:

PORTFOLIO: {portfolio_name}
RISK PROFILE: {risk_profile}
TOTAL VALUE: ${summary_metrics.get('total_value', 0):,.2f}
NUMBER OF HOLDINGS: {summary_metrics.get('num_holdings', 0)}

HOLDINGS:
{holdings_text}

SECTOR BREAKDOWN:
{sector_text}

LARGEST POSITION: {summary_metrics.get('largest_position', 'N/A')}
OVERALL VOLATILITY: {summary_metrics.get('overall_volatility', 'medium')}

Follow the analysis framework and provide:
1. Portfolio summary (1 paragraph)
2. Overconcentration risks
3. Volatility classification
4. Missing elements/gaps
5. 2-3 recommendations (hold/trim/diversify language)
6. Plain-English guidance
7. Disclaimer

CRITICAL: No financial advice, no specific buy/sell directives, educational only."""

    compliance_prompt = """You are a portfolio education assistant.
Help users UNDERSTAND their portfolio structure, never tell them what to do.
Focus on: diversification principles, risk awareness, sector balance, educational insights."""

    return call_ai_model(prompt, system_prompt=compliance_prompt)

# Day Trade Ideas
def run_day_trade_ideas(candidates: List[Dict], limit: int = 3) -> str:
    """
    Generate AI day-trade candidate analysis

    Args:
        candidates (list): List of high-volatility stock dicts
        limit (int): Number of candidates to analyze

    Returns:
        str: AI-generated trading ideas
    """
    # Load prompt template
    prompt_template = ai_prompts.load_prompt('day_trade_ideas')

    # Format candidates
    candidates_text = "\n\n".join([
        f"CANDIDATE {i+1}: {c['ticker']}\n"
        f"Price: ${c['price']:.2f}\n"
        f"Volatility: {c['volatility_score']}\n"
        f"Volume vs Avg: {c.get('volume_vs_avg', 'N/A')}\n"
        f"Reason: {c['reason']}\n"
        f"Tags: {', '.join(c.get('tags', []))}"
        for i, c in enumerate(candidates[:limit])
    ])

    prompt = f"""Identify day-trade candidates from these high-volatility stocks:

{candidates_text}

Follow the framework and provide:
1. Select top {limit} candidates
2. Explain catalysts (news/volume/volatility)
3. Trader watchpoints
4. Risk warnings (2-3 sentences each)
5. No entry/exit prices

CRITICAL: Substantial risk warning, not a recommendation, DYOR emphasis."""

    compliance_prompt = """You are a trading education assistant.
Day trading is HIGH RISK. Your role is to explain market signals, not recommend trades.
Always emphasize: substantial risk, research required, not personalized advice."""

    return call_ai_model(prompt, system_prompt=compliance_prompt)

# Daily Email Newsletter
def run_daily_email(market_data: Dict, top_picks: List[Dict]) -> str:
    """
    Generate daily market brief email

    Args:
        market_data (dict): Market snapshot (indexes, sentiment, volatility)
        top_picks (list): 3 stock picks

    Returns:
        str: AI-generated email content
    """
    prompt_template = ai_prompts.load_prompt('daily_email')

    picks_text = "\n\n".join([
        f"Stock {i+1}: {p['ticker']} - ${p['price']:.2f}\n"
        f"Volatility: {p.get('volatility', 'N/A')}\n"
        f"Catalyst: {p.get('catalyst', 'N/A')}"
        for i, p in enumerate(top_picks[:3])
    ])

    prompt = f"""Generate a daily market brief email:

MARKET SNAPSHOT:
{json.dumps(market_data, indent=2)}

TODAY'S PICKS:
{picks_text}

Format: Market paragraph + 3 stock picks + disclaimer
Tone: Concise, data-driven
Length: 200-300 words"""

    return call_ai_model(prompt)

# Weekly Portfolio Email
def run_weekly_email(
    portfolio_summary: Dict,
    stock_ideas: List[Dict],
    upcoming_events: List[str]
) -> str:
    """
    Generate weekly portfolio health email

    Args:
        portfolio_summary (dict): Portfolio metrics
        stock_ideas (list): 2 stock ideas (conservative + growth)
        upcoming_events (list): Economic events

    Returns:
        str: AI-generated email content
    """
    prompt_template = ai_prompts.load_prompt('weekly_email')

    prompt = f"""Generate a weekly portfolio health email:

PORTFOLIO SUMMARY:
{json.dumps(portfolio_summary, indent=2)}

STOCK IDEAS:
{json.dumps(stock_ideas, indent=2)}

UPCOMING EVENTS:
{chr(10).join(['- ' + e for e in upcoming_events])}

Format: Market recap + portfolio metrics + 2 ideas + events + tip
Tone: Calm, helpful
Length: 400-500 words"""

    return call_ai_model(prompt)

# Monthly Deep Dive
def run_monthly_email(
    macro_theme: str,
    sector_focus: str,
    featured_stocks: List[Dict],
    educational_topic: str
) -> str:
    """
    Generate monthly deep dive newsletter

    Args:
        macro_theme (str): Macro economic theme
        sector_focus (str): Sector spotlight
        featured_stocks (list): 3-5 stocks to analyze
        educational_topic (str): Educational concept

    Returns:
        str: AI-generated email content
    """
    prompt_template = ai_prompts.load_prompt('monthly_email')

    prompt = f"""Generate a monthly deep dive newsletter:

MACRO THEME: {macro_theme}
SECTOR FOCUS: {sector_focus}
EDUCATIONAL TOPIC: {educational_topic}

FEATURED STOCKS:
{json.dumps(featured_stocks, indent=2)}

Format: Macro theme (2-3 paragraphs) + sector analysis + allocations +
        stock deep dives + learning corner (3-4 paragraphs)
Tone: Thoughtful, educational
Length: 800-1000 words"""

    return call_ai_model(prompt)

# Risk Profile Translator
def run_risk_profile_analysis(investment: Dict, risk_profiles: List[str]) -> str:
    """
    Translate investment to risk profile suitability

    Args:
        investment (dict): Stock or portfolio data
        risk_profiles (list): Profiles to analyze (conservative/moderate/aggressive)

    Returns:
        str: AI-generated risk analysis
    """
    prompt_template = ai_prompts.load_prompt('risk_translator')

    prompt = f"""Analyze investment suitability across risk profiles:

INVESTMENT DATA:
{json.dumps(investment, indent=2)}

PROFILES TO ANALYZE: {', '.join(risk_profiles)}

Provide:
1. Overall risk classification
2. Fit for each profile (✅/❌ with 3 reasons)
3. Investor types (best for / not ideal for)
4. Top 3 risks
5. Mitigation strategies"""

    return call_ai_model(prompt)

# Concept Explainer
def run_concept_explanation(concept_name: str) -> str:
    """
    Explain investment concept in simple language

    Args:
        concept_name (str): Concept to explain

    Returns:
        str: AI-generated explanation
    """
    prompt_template = ai_prompts.load_prompt('concept_explainer')

    prompt = f"""Explain this investment concept in beginner-friendly language:

CONCEPT: {concept_name}

Format:
- Plain English definition (1-2 sentences)
- Relatable analogy
- Why it matters (practical impact)
- Real-world example with numbers
- Bottom line (1 sentence)

Tone: Conversational, warm, no jargon
Length: 150-250 words"""

    return call_ai_model(prompt)

# Utility: Check if AI is configured
def is_ai_configured() -> bool:
    """Check if AI service is properly configured"""
    if AI_PROVIDER == 'openai':
        return OPENAI_API_KEY is not None
    elif AI_PROVIDER == 'anthropic':
        return ANTHROPIC_API_KEY is not None
    return False

# Utility: Get AI status
def get_ai_status() -> Dict:
    """Get AI service configuration status"""
    return {
        "configured": is_ai_configured(),
        "provider": AI_PROVIDER,
        "model": AI_MODEL,
        "openai_key_set": OPENAI_API_KEY is not None,
        "anthropic_key_set": ANTHROPIC_API_KEY is not None
    }
