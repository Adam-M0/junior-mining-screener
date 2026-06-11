import os
import re
import requests
from openai import OpenAI

# Initialize AI Client
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

print("Connecting to Junior Mining Network Feed...")
feed_url = "https://juniorminingnetwork.com"

try:
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    response = requests.get(feed_url, headers=headers, timeout=15)
    
    # We convert the webpage text into a safe format to prevent encoding crashes
    raw_text = response.text
    
    # We extract individual articles using text patterns instead of strict XML parsing
    items = re.findall(r'<item>(.*?)</item>', raw_text, re.DOTALL)
    articles = []
    
    # Sift through the newest 25 updates on the feed
    for item in items[:25]:
        # Safely extract Title, Link, and Description using regular expressions
        title_match = re.search(r'<title>(.*?)</title>', item, re.DOTALL)
        link_match = re.search(r'<link>(.*?)</link>', item, re.DOTALL)
        desc_match = re.search(r'<description>(.*?)</description>', item, re.DOTALL)
        
        title = title_match.group(1).strip() if title_match else "Unknown Title"
        link = link_match.group(1).strip() if link_match else ""
        desc = desc_match.group(1).strip() if desc_match else ""
        
        # Clean up common internet code tags from the text
        title = re.sub(r'<!\[CDATA\[(.*?)\]\]>', r'\1', title)
        desc = re.sub(r'<!\[CDATA\[(.*?)\]\]>', r'\1', desc)
        desc = re.sub(r'<[^>]*>', '', desc)  # Strips out raw HTML formatting tags
        
        articles.append({
            "title": title,
            "summary": desc[:400],  # Give AI the first 400 characters for background context
            "link": link
        })
        
    print(f"Successfully processed {len(articles)} fresh industry updates.")

except Exception as e:
    print(f"Network error trying to read the live feed: {e}")
    exit()

if not articles:
    print("No new articles could be extracted from the feed today.")
    exit()

print("Routing mining news to AI geological analysis agent...")

# Instruct the AI agent to explicitly act as a professional economic geologist
ai_prompt = f"""
You are an expert economic geologist and mining analyst. Review these junior mining news items:
{articles}

Your task is to isolate early-phase miners reporting notable drill results or sampling assays.
For each valid discovery, cross-reference your geological knowledge base to verify if their asset sits within a prolific mining district, geological belt, or has proven multi-million ounce/ton deposits nearby.

Output a clean Markdown report with the following structure:
### ⛏️ Top Drilling & Discovery Catalysts
Create a Markdown table with columns: [Company / Project] | [Commodity] | [Drill/Assay Highlights] | [District Proximity Context] | [Source Link]

Rules:
1. Only include companies showing high-grade or high-width results (e.g., 'g/t Au', '% Cu', 'AgEq').
2. In the 'District Proximity Context' column, specify why the location matters (e.g., 'Sits in the Carlin Trend near Nevada Gold Mines operations' or 'Located in the Abitibi Greenstone belt near historical producers').
3. Format the source link as a clickable markdown hyperlink using the exact URL provided.
"""

response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": ai_prompt}]
)

print("\n=== FINAL JUNIOR MINING DISTRICT INTELLIGENCE ===")
print(response.choices[0].message.content)
