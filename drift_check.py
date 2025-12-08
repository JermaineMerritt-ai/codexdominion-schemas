#!/usr/bin/env python3
import argparse
import requests
import logging
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed
from requests.adapters import HTTPAdapter, Retry
from typing import Optional

MARKET_APIS = [
    "https://api.example1.com/quote/",
    "https://api.example2.com/quote/"
]


def get_session(
    retries: int = 3,
    backoff_factor: float = 0.5
) -> requests.Session:
    session = requests.Session()
    retry = Retry(
        total=retries,
        backoff_factor=backoff_factor,
        status_forcelist=[500, 502, 503, 504],
        allowed_methods=["HEAD", "GET", "OPTIONS"]
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    return session

def check_market_ticker(
    ticker: str,
    retries: int = 3,
    logger: Optional[logging.Logger] = None
) -> Optional[str]:
    prices = []
    session = get_session(retries=retries)
    for api in MARKET_APIS:
        try:
            r = session.get(api + ticker, timeout=5)
            if r.ok:
                prices.append(r.json().get("price"))
        except Exception as e:
            if logger:
                logger.error(f"Market API error for {ticker} at {api}: {e}")
    if len(set(prices)) > 1:
        return f"{ticker}: price drift {prices}"
    return None

def check_site_timestamp(
    site_url: str,
    retries: int = 3,
    logger: Optional[logging.Logger] = None
) -> Optional[str]:
    session = get_session(retries=retries)
    try:
        r = session.get(site_url, timeout=5)
        if r.ok and "Last verified" not in r.text:
            return f"{site_url}: missing verification stamp"
    except Exception as e:
        if logger:
            logger.error(f"Site check error for {site_url}: {e}")
        return f"{site_url}: error {e}"
    return None


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--markets", action="store_true",
        help="Check market tickers for drift."
    )
    parser.add_argument(
        "--sites", action="store_true",
        help="Check sites for verification stamp."
    )
    parser.add_argument(
        "--hourly", action="store_true",
        help="Run hourly checks."
    )
    parser.add_argument(
        "--daily", action="store_true",
        help="Run daily checks."
    )
    parser.add_argument(
        "--logfile", type=str, default=None,
        help="Log errors to file."
    )
    parser.add_argument(
        "--retries", type=int, default=3,
        help="Number of retries for requests."
    )
    args = parser.parse_args()

    logger = None
    if args.logfile:
        logging.basicConfig(
            filename=args.logfile,
            level=logging.ERROR,
            format='%(asctime)s %(levelname)s %(message)s'
        )
        logger = logging.getLogger("drift_check")

    issues = []
    market_tickers = ["AAPL", "MSFT", "GOOG"]  # extend list as needed
    site_urls = [
        "https://faith.codexdominion.app",
        "https://kids.codexdominion.app",
        "https://lifestyle.codexdominion.app",
        "https://academy.codexdominion.app"
    ]

    with ThreadPoolExecutor() as executor:
        futures = []
        if args.markets:
            for ticker in market_tickers:
                futures.append(
                    executor.submit(
                        check_market_ticker, ticker, args.retries, logger
                    )
                )
        if args.sites:
            for url in site_urls:
                futures.append(
                    executor.submit(
                        check_site_timestamp, url, args.retries, logger
                    )
                )
        for future in as_completed(futures):
            drift = future.result()
            if drift:
                issues.append(drift)

    if issues:
        print("Drift detected at", datetime.utcnow().isoformat())
        for i in issues:
            print(" -", i)
        print("⚠️  Drift logged for monitoring, continuing workflow")
    else:
        print("No drift detected at", datetime.utcnow().isoformat())
