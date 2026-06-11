import os
import re
import requests
from openai import OpenAI

# Initialize AI Client
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

print("Connecting to Unblocked Mining Press Release Wire...")
# This uses a public global wire distribution link that never blocks cloud automations
feed_url = "https://rss.app" 

try:
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
    response = requests.get(feed_url, headers=headers, timeout=15)
    raw_text = response.text
    
    # Isolate articles via regex
    items = re.findall(r'<item>(.*?)</item>', raw_text, re.DOTALL)
    articles = []
    
    # Pull up to 60 items to accurately capture a full 3-day history of global mining releases
    for item in items[:60]:
        title_match = re.search(r'<title>(.*?)</title>', item, re.DOTALL)
        link_match = re.search(r'<link>(.*?)</link>', item, re.DOTALL)
        desc_match = re.search(r'<description>(.*?)</description>', item, re.DOTALL)
        
        title = title_match.group(1).strip() if title_match else "Unknown Title"
        link = link_match.group(1).strip() if link_match else ""
        desc = desc_match.group(1).strip() if desc_match else ""
        
        # Clean unneeded web code tags
        title = re.sub(r'<!\[CDATA\[(.*?)\]\]>', r'\1', title)
        desc = re.sub(r'<!\[CDATA\[(.*?)\]\]>', r'\1', desc)
        desc = re.sub(r'<[^>]*>', '', desc) 
        
        articles.append({
            "title": title,
            "summary": desc[:300], # Keep summary tight to stay ultra-cheap on OpenAI costs
            "link": link
        })
        
    print(f"Successfully processed {len(articles)} fresh industry wire releases.")

except Exception as e:
    print(f"Network processing error: {e}")
    exit()

if not articles:
    print("No fresh wire articles could be extracted from the feed stream today.")
    exit()

print("Routing live exploration news to AI geological analysis agent...")

ai_prompt = f"""
You are an expert economic geologist and mining analyst. Review these mining wire releases spanning the past 3 days:
{articles}

CRITICAL FILTER RULE: Quickly scan the titles. If a headline does not mention drill results, assays, intercepts, or exploration discoveries, ignore it. Discard generic corporate items, private placements, and corporate appointments.

For each valid discovery, cross-reference your geological knowledge base to verify if their asset sits within a prolific mining district, geological belt, or has proven multi-million ounce/ton deposits nearby.

Output a clean Markdown report with the following structure:
### ⛏️ Top Drilling & Discovery Catalysts (Past 3 Days)
Create a Markdown table with columns: [Company / Project] | [Commodity] | [Drill/Assay Highlights] | [District Proximity Context] | [Source Link]

Rules:
1. Only include companies showing high-grade or high-width results (e.g., 'g/t Au', '% Cu', 'AgEq', '% U3O8').
2. In the 'District Proximity Context' column, specify why the location matters geologically or historically.
3. Format the source link as a clickable markdown hyperlink using the exact URL provided.
"""

response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": ai_prompt}]
)

print("\n=== FINAL JUNIOR MINING DISTRICT INTELLIGENCE ===")
print(response.choices.message.content)
