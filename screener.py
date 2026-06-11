import os
import requests
import xml.etree.ElementTree as ET
from openai import OpenAI

# Initialize AI Client
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

print("Connecting to Junior Mining Network Feed...")

# Fetching the live news distribution feed from Junior Mining Network
feed_url = "https://juniorminingnetwork.com"

try:
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    response = requests.get(feed_url, headers=headers, timeout=15)
    
    # Parse the XML data structure from the website feed
    root = ET.fromstring(response.content)
    articles = []
    
    # Extract the titles, text blurbs, and reference links for today's releases
    for item in root.findall(".//item")[:25]:  # Sift through the top 25 newest updates
        title = item.find("title").text if item.find("title") is not None else ""
        description = item.find("description").text if item.find("description") is not None else ""
        link = item.find("link").text if item.find("link") is not None else ""
        
        articles.append({
            "title": title,
            "summary": description[:400],  # Give AI the first 400 characters for context
            "link": link
        })
        
    print(f"Successfully downloaded {len(articles)} fresh industry updates.")

except Exception as e:
    print(f"Network error trying to read the live feed: {e}")
    exit()

if not articles:
    print("No new articles posted on the feed today.")
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
3. Format the source link as a clickable markdown markdown hyper-link using the exact URL provided.
"""

response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": ai_prompt}]
)

print("\n=== FINAL JUNIOR MINING DISTRICT INTELLIGENCE ===")
print(response.choices[0].message.content)
