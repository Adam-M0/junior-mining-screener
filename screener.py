import os
import re
import requests
from openai import OpenAI

# Initialize AI Client
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

print("Connecting to Open Google News Mining Network...")

# Expanded search query to maximize target article discovery
feed_url = "https://google.com"

# Authentic desktop browser identity headers to bypass firewalls
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
    "Referer": "https://google.com"
}

# CRITICAL LINE: Defining the articles list container explicitly
articles = []

try:
    response = requests.get(feed_url, headers=headers, timeout=15)
    raw_text = response.text
    
    # Isolate articles via text tags
    items = re.findall(r'<item>(.*?)</item>', raw_text, re.DOTALL)
    
    # Capture up to 60 items to accurately analyze a full 3-day history
    for item in items[:60]:
        title_match = re.search(r'<title>(.*?)</title>', item, re.DOTALL)
        link_match = re.search(r'<link>(.*?)</link>', item, re.DOTALL)
        
        title = title_match.group(1).strip() if title_match else "Unknown Title"
        link = link_match.group(1).strip() if link_match else ""
        
        # Clean up data wrappers
        title = re.sub(r'<!\[CDATA\[(.*?)\]\]>', r'\1', title)
        
        articles.append({
            "title": title,
            "summary": "Review title for context.",
            "link": link
        })
        
    print(f"Successfully processed {len(articles)} live mining reports.")

except Exception as e:
    print(f"Network error: {e}")
    exit()

if not articles:
    print("No fresh wire articles could be extracted today.")
    exit()

print("Routing mining stream data to AI geological analysis agent...")

# Optimization prompt ensuring rapid sifting to keep OpenAI token cost at fractions of a penny
ai_prompt = f"""
You are an expert economic geologist and junior mining analyst. Review these global industry releases spanning the past 3 days:
{articles}

CRITICAL FILTER RULE: Quickly skim the titles. If a headline does not explicitly mention junior resource drill results, core assays, intercepts, grading metrics, or exploration discoveries, discard it immediately. Ignore generic macro economics, options updates, oil/gas, and corporate management layout updates.

For each passing junior mining discovery catalyst, use your geological knowledge base to verify if their asset sits within a prolific mining district, structural trend, greenstone belt, or has proven multi-million ounce/ton deposit mines nearby.

Output a clean Markdown report with the exact structure below:
### ⛏️ Top Drilling & Discovery Catalysts (Past 3 Days)
Create a Markdown table with columns: [Company / Project] | [Commodity] | [Drill/Assay Highlights] | [District Proximity Context] | [Source Link]

Rules:
1. Only include companies showing notable high-grade or high-width results (e.g., 'g/t Au', '% Cu', 'AgEq', '% U3O8', 'Li2O').
2. In the 'District Proximity Context' column, specify why the location matters historically or geologically (e.g., 'Sits in the Carlin Trend near Barrick producers' or 'Located in the James Bay lithium district near Patriot Battery Metals discovery').
3. Format the source link as a clickable markdown hyperlink displaying '[View Release]' utilizing the exact URL string.
"""

response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": ai_prompt}]
)

print("\n=== FINAL JUNIOR MINING DISTRICT INTELLIGENCE ===")
print(response.choices.message.content)
