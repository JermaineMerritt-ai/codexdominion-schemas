"""
AI Service for Portfolio Insights
==================================
OpenAI GPT-4 integration with compliance filtering.
"""

import os
from typing import Dict, List
import openai

# Configure OpenAI (use environment variable or config)
openai.api_key = os.getenv("OPENAI_API_KEY", "")


def generate_portfolio_summary(
    portfolio: Dict,
    holdings: List[Dict],
    sector_breakdown: List[Dict],
    identity_type: str = "general"
) -> str:
    """
    Generate identity-aware portfolio summary with strict compliance guardrails.
    
    Args:
        portfolio: Portfolio dict with name, total_value, etc.
        holdings: List of holding dicts with symbol, shares, current_value, etc.
        sector_breakdown: List of sector allocation dicts
        identity_type: One of: diaspora, youth, creator, legacy-builder, general
    
    Returns:
        Compliance-filtered summary text
    """
    
    # Identity-specific prompt additions
    identity_contexts = {
        "diaspora": "This investor is part of the global diaspora, building wealth across borders. Highlight diversification and global exposure.",
        "youth": "This is a younger investor starting their financial journey. Use beginner-friendly language and emphasize long-term growth.",
        "creator": "This investor is a content creator or entrepreneur. Connect insights to creative capital and business growth.",
        "legacy-builder": "This investor is focused on generational wealth. Emphasize preservation, growth, and legacy planning.",
        "general": "Provide balanced, descriptive portfolio insights."
    }
    
    identity_context = identity_contexts.get(identity_type, identity_contexts["general"])
    
    # Build prompt with holdings data
    holdings_text = "\n".join([
        f"- {h['symbol']}: {h['shares']} shares, ${h['current_value']:.2f} value, {h.get('sector', 'Unknown')} sector"
        for h in holdings[:20]  # Limit to top 20 for token efficiency
    ])
    
    sectors_text = "\n".join([
        f"- {s['sector']}: {s['percentage']:.1f}% (${s['value']:.2f})"
        for s in sorted(sector_breakdown, key=lambda x: x['percentage'], reverse=True)
    ])
    
    prompt = f"""You are a financial data analyst for DominionMarkets, a descriptive stock data platform.

CRITICAL COMPLIANCE RULES:
1. NEVER give financial advice, predictions, or recommendations
2. ONLY provide descriptive analysis of current holdings
3. Use past tense or present tense descriptions only
4. NO words like "should", "recommend", "suggest", "predict", "will", "expect"
5. NO target prices, future performance estimates, or action items
6. Frame everything as "Your portfolio currently shows..." or "Historical data indicates..."

PORTFOLIO DETAILS:
Name: {portfolio.get('name', 'Portfolio')}
Total Value: ${portfolio.get('total_value', 0):.2f}
Number of Holdings: {len(holdings)}
All-Time P&L: ${portfolio.get('total_gain_loss', 0):.2f}

HOLDINGS:
{holdings_text}

SECTOR ALLOCATION:
{sectors_text}

IDENTITY CONTEXT:
{identity_context}

Generate a 3-paragraph summary (150-200 words) that:
1. Describes current portfolio composition and sector distribution
2. Notes diversification level and concentration patterns
3. Provides identity-aware observations about portfolio characteristics

Use descriptive, compliance-approved language only. Start with "Your portfolio currently..."
"""

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a compliance-focused financial data analyst. You NEVER give advice or predictions, only descriptive analysis."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=400,
            temperature=0.7
        )
        
        summary = response.choices[0].message.content.strip()
        
        # Post-processing compliance filter
        summary = apply_compliance_filter(summary)
        
        return summary
        
    except Exception as e:
        raise Exception(f"OpenAI API error: {str(e)}")


def apply_compliance_filter(text: str) -> str:
    """
    Remove non-compliant language from AI-generated text.
    """
    # Forbidden words that imply advice/predictions
    forbidden_patterns = [
        ("should", "currently shows"),
        ("recommend", "notes"),
        ("suggest", "indicates"),
        ("will likely", "has historically"),
        ("expect", "observes"),
        ("predict", "shows"),
        ("buy", "holds"),
        ("sell", "contains"),
        ("target price", "current price"),
    ]
    
    filtered = text
    for forbidden, replacement in forbidden_patterns:
        filtered = filtered.replace(forbidden, replacement)
        filtered = filtered.replace(forbidden.capitalize(), replacement.capitalize())
    
    return filtered
