"""
AI Prompts for portfolio analysis and recommendations
"""

PORTFOLIO_ANALYSIS_PROMPT = """
Analyze the following portfolio and provide insights:

Portfolio: {portfolio_name}
Risk Profile: {risk_profile}
Total Value: ${total_value:,.2f}
Number of Holdings: {num_holdings}

Holdings:
{holdings_list}

Sector Breakdown:
{sector_breakdown}

Performance:
- Total Return: ${total_return:,.2f} ({total_return_pct:.2f}%)
- Daily Change: ${daily_change:,.2f} ({daily_change_pct:.2f}%)

Please provide:
1. Risk assessment summary
2. Diversification analysis
3. Concentration risks
4. Sector exposure analysis
5. Three key strengths
6. Three key risks
7. Three actionable recommendations
"""

STOCK_ANALYSIS_PROMPT = """
Provide a brief investment thesis for {ticker}:

Current Price: ${current_price:.2f}
Sector: {sector}
Portfolio Weight: {weight:.1f}%

Include:
1. Brief company overview (2-3 sentences)
2. Investment recommendation (Buy/Hold/Sell)
3. Target price
4. Key catalysts or risks
"""

TRADING_PICK_PROMPT = """
Analyze this trading opportunity:

Ticker: {ticker}
Entry Price: ${entry_price:.2f}
Current Technical Setup: {technical_setup}
Sector Momentum: {sector_momentum}

Provide:
1. Trade rationale (2-3 sentences)
2. Trade type (day/swing/position)
3. Target price
4. Stop loss
5. Confidence level (low/medium/high)
"""

NEWSLETTER_CONTENT_PROMPT = """
Generate newsletter content for {segment} segment:

Subscriber Risk Profile: {risk_profile}
Recent Portfolio Performance: {performance_summary}
Active Trading Picks: {active_picks_count}

Content Type: {content_type}

Include:
1. Personalized greeting
2. Market overview relevant to risk profile
3. Portfolio highlights
4. Active picks summary
5. Educational tip
6. Call to action
"""

RISK_ASSESSMENT_PROMPT = """
Assess portfolio risk based on:

Risk Profile Target: {target_risk_profile}
Current Holdings: {num_holdings}
Largest Position: {largest_position_pct:.1f}%
Sector Concentration: {top_sector} ({top_sector_pct:.1f}%)
Portfolio Volatility: {volatility_estimate}

Provide risk score (0-100) and categorization:
- 0-30: Conservative (well-diversified, low volatility)
- 31-60: Moderate (balanced risk/reward)
- 61-100: Aggressive (concentrated, high volatility)
"""
