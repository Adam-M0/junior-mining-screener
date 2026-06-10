import os
import yfinance as yf
from openai import OpenAI

# Initialize our ultra-cheap AI agent
client = OpenAI(api_key=os.environ.get("Openai_API_Key"))

# Add the specific junior mining tickers you want to monitor daily.
# Yahoo Finance format: Canadian Ventuer uses '.V', Australian uses '.AX'
WATCHLIST = [
    "NXS.V", "AAG.V", "AU.V", "LIO.V",  # Examples of TSX-V tickers
    "LTR.AX", "CHN.AX", "DEG.AX"         # Examples of ASX tickers
]

print("Starting Morning Mining Screen...")
filtered_stocks = []

for ticker_symbol in WATCHLIST:
    try:
        ticker = yf.Ticker(ticker_symbol)
        info = ticker.info
        
        # Pull required hard numbers
        market_cap = info.get("marketCap", 0)
        volume = info.get("volume", 0)
        
        # CRITERIA 1: Keep only micro-caps under $150 Million
        if market_cap > 150000000 or market_cap == 0:
            continue
            
        # CRITERIA 2: Ensure basic liquidity (Volume > 20,000 shares today)
        if volume < 20000:
            continue
            
        # Get the latest news headline for AI to audit
        news = ticker.news
        latest_headline = news[0]['title'] if news else "No recent news."
        
        filtered_stocks.append({
            "ticker": ticker_symbol,
            "mcap": f"${market_cap:,}",
            "vol": f"{volume:,}",
            "headline": latest_headline
        })
    except Exception as e:
        print(f"Skipping {ticker_symbol} due to a temporary data error.")

# If no stocks met the math baseline, exit early
if not filtered_stocks:
    print("No junior stocks met the math volume/mcap parameters today.")
    exit()

# Pass the final candidates to our cheap AI model to check for exploration catalysts
ai_prompt = f"""
You are an expert junior resource analyst. Audit this list of filtered mining stocks and their headlines:
{filtered_stocks}

Identify if any headlines contain major geological catalyst keywords like 'assays', 'drill', 'intercept', 'g/t', 'copper', 'gold', 'uranium', or 'discovery'. 
Output a crisp Markdown summary table ranking the top results. Keep your descriptions to one short sentence.
"""

response = client.chat.completions.create(
    model="gpt-4o-mini", # Tiny model costs roughly $0.002 to execute this
    messages=[{"role": "user", "content": ai_prompt}]
)

# Print out the final watchlist report to our dashboard
print("\n=== FINAL MORNING WATCHLIST ===")
print(response.choices[0].message.content)
