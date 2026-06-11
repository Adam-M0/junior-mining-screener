import os
import re
import requests
from openai import OpenAI

# Initialize AI Client
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

# Comprehensive list of mining and wire endpoints to guarantee data extraction
FEED_SOURCES = [
    "https://news-distribution.com", # Dedicated mining stream mirror
    "https://globenewswire.com", # Global raw materials channel
    "https://news-distribution.com" # Fallback raw metals loop
]

articles = []
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"}

print("Connecting to Unblocked Mining Press Release Wire Network...")

# Attempt extraction down the channel tree until valid data hits
for feed_url in FEED_SOURCES:
    try:
        print(f"Pinging active pipeline node: {feed_url}")
        response = requests.get(feed_url, headers=headers, timeout=12)
        
        if response.status_code != 200:
            print(f"Node returned structural code {response.status_code}, routing to next pool...")
            continue
            
        raw_text = response.text
        items = re.findall(r'<item>(.*?)</item>', raw_text, re.DOTALL)
        
        if not items:
            continue
            
        # Target up to 80 raw titles to capture a thorough 3-day history window
        for item in items[:80]:
            title_match = re.search(r'<title>(.*?)</title>', item, re.DOTALL)
            link_match = re.search(r'<link>(.*?)</link>', item, re.DOTALL)
            desc_match = re.search(r'<description>(.*?)</description>', item, re.DOTALL)
            
            title = title_match.group(1).strip() if title_match else "Unknown Title"
            link = link_match.group(1).strip() if link_match else ""
            desc = desc_match.group(1).strip() if desc_match else ""
            
            # Clean out unneeded HTML wrapper code tags to reduce OpenAI token size
            title = re.sub(r'<!\[CDATA\[(.*?)\]\]>', r'\1', title)
            desc = re.sub(r'<!\[CDATA\[(.*?)\]\]>', r'\1', desc)
            desc = re.sub(r'<[^>]*>', '', desc) 
            
            articles.append({
                "title": title,
                "summary": desc[:300], # Pull short abstract summaries to stay ultra economic on inputs
                "link": link
            })
            
        if articles:
            print(f"Successfully processed {len(articles)} fresh industry updates from active data pipe.")
            break # Exit the loop early once a feed successfully streams down raw files
            
    except Exception as e:
        print(f"Connection timed out or dropped on this server node: {e}")
        continue

# Hard exit safeguard if entire system framework fails to touch any data endpoints
if not articles:
    print("\n[SYSTEM ERROR]: All dynamic news mirrors returned 0 items. Checking framework filters.")
    exit()

print("Routing mining stream data to AI geological analysis agent...")

# Economic prompt instructing model to cut unrelated clutter processing instantly
ai_prompt = f"""
You are an expert economic geologist and junior mining analyst. Review these industry wire releases spanning the past 3 days:
{articles}

CRITICAL FILTER RULE: Quickly skim the titles. If a headline does not explicitly mention drill results, assays, intercepts, grading metrics, or exploration discoveries, discard it immediately. Ignore generic private placements, options trading updates, and corporate management changes.

For each passing junior mining discovery catalyst, use your geological knowledge base to verify if their asset sits within a prolific mining district, structural trend, greenstone belt, or has proven multi-million ounce/ton deposit mines nearby.

Output a clean Markdown report with the exact structure below:
### ⛏️ Top Drilling & Discovery Catalysts (Past 3 Days)
Create a Markdown table with columns: [Company / Project] | [Commodity] | [Drill/Assay Highlights] | [District Proximity Context] | [Source Link]

Rules:
1. Only include companies showing notable high-grade or high-width results (e.g., 'g/t Au', '% Cu', 'AgEq', '% U3O8', 'Li2O').
2. In the 'District Proximity Context' column, specify why the location matters historically or geologically (e.g., 'Sits in the Carlin Trend near Barrick producers' or 'Located in the James Bay lithium district near Patriot Battery Metals discovery').
3. Format the source link as a clickable markdown hyperlink layout displaying the company name or '[View Release]' utilizing the exact URL string.
"""

response = client.chat.completions.create(
    model="gpt-4o-mini", # Microscopic pay-as-you-go cost model (~$0.003 a run)
    messages=[{"role": "user", "content": ai_prompt}]
)

print("\n=== FINAL JUNIOR MINING DISTRICT INTELLIGENCE ===")
print(response.choices[0].message.content)
