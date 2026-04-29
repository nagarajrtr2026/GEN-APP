import json
import re

def extract_json(text: str) -> dict:
    # Handle markdown JSON wrappers safely
    pattern = r"```(?:json)? 
?(.*?)
?```"
    match = re.search(pattern, text, re.DOTALL)
    if match:
        text = match.group(1)
    
    try:
        return json.loads(text.strip())
    except Exception:
        return {}