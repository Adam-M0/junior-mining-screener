import os
import requests
import yfinance as yf
from openai import OpenAI

# Initialize AI Client
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

print("Fetching active TSX Venture list...")

try:
    # We fetch a live, public, open-source master list of TSXV tickers 
    # to find candidates dynamically instead of hardcoding them.
    url = "https://githubusercontent.com"
    response = requests.get(url, timeout=15)
    all_tickers = response.json()  # This provides a broad array of raw tickers (e.g., ["AAG", "NXS"])
except Exception as e:
    print(f"Failed to fetch master exchange directory: {e}")
    # Fallback list just in case the external server fails to respond
    all_tickers = ["NXS", "AAG", "LIO", "AU", "AMX", "PPP", "KLDC", "DRY", "SGD"]

print(f"Discovered {len(all_tickers)} potential listings. Beginning math verification scan...")

filtered_stocks = []
scan_limit = 50  # We limit the initial bulk profile scan to avoid hitting Yahoo speed blocks
scanned_count = 0

for raw_symbol in all_tickers:
    if scanned_count >= scan_limit:
        break
        
    # Standardize format to Yahoo Finance Venture format (Symbol + .V)
    ticker_symbol = f"{raw_symbol.strip()}.V"
    
    try:
        ticker = yf.Ticker(ticker_symbol)
        info = ticker.info
        
        if not info:
            continue
            
        market_cap = info.get("marketCap", 0) or 0
        volume = info.get("volume", 0) or 0
        industry = info.get("industry", "").lower()
        
        # FILTER 1: Target only true Materials/Mining related micro-caps
        if "mining" not in industry and "materials" not in industry and "gold" not in industry:
            continue
            
        # FILTER 2: Target Micro-Caps (Market Cap under $100 Million)
        if market_cap > 100000000 or market_cap == 0:
            continue
            
        # FILTER 3: Basic liquidity buffer to ensure it's actively traded
        if volume < 5000:
            continue
            
        # Safe extraction of latest news headline text
        ticker_news = getattr(ticker, "news", [])
        latest_headline = "No recent news."
        if ticker_news and len(ticker_news) > 0:
            latest_headline = ticker_news[0].get("title", "No headline text available.")
            
        filtered_stocks.append({
            "ticker": ticker_symbol,
            "mcap": f"${market_cap:,}",
            "vol": f"{volume:,}",
            "industry": info.get("industry", "Mining"),
            "headline": latest_headline
        })
        
        scanned_count += 1
        print(f"Added Candidate: {ticker_symbol} | Vol: {volume:,}")
        
    except Exception:
        # Move past any tickers that throw errors or are temporarily halted
        continue

if not filtered_stocks:
    print("No mining stocks met your strict filters during this session's pass.")
    exit()

print(f"Successfully generated a baseline of {len(filtered_stocks)} candidates. Routing to AI agent...")

# The prompt dynamically reviews the raw output list generated above
ai_prompt = f"""
You are an expert junior resource analyst. Audit this list of dynamically generated mining stocks:
{filtered_stocks}

Examine the headlines. Identify if any contain major geological catalyst terms or exploration indicators (e.g., 'assays', 'drill', 'intercept', 'g/t', 'copper', 'gold', 'uranium', 'discovery', or 'strike'). 

Generate a clean Markdown table summarizing the findings. Rank the highest impact geological news at the top. Add a one-sentence warning if a ticker has no recent news.
"""

response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": ai_prompt}]
)

print("\n=== FINAL MORNING DYNAMIC WATCHLIST ===")
print(response.choices[0].message.content)
