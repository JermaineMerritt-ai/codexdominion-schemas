import drift_check


def check_drift() -> list:
    # Run both market and site checks, return list of drift issues
    market_tickers = ["AAPL", "MSFT", "GOOG"]
    site_urls = [
        "https://faith.codexdominion.app",
        "https://kids.codexdominion.app",
        "https://lifestyle.codexdominion.app",
        "https://academy.codexdominion.app"
    ]
    issues = []
    for ticker in market_tickers:
        drift = drift_check.check_market_ticker(ticker)
        if drift:
            issues.append(drift)
    for url in site_urls:
        drift = drift_check.check_site_timestamp(url)
        if drift:
            issues.append(drift)
    return issues