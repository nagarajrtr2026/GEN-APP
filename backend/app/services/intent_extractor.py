import json
from app.services.ai_client import AIClient


class IntentExtractor:
    def __init__(self, ai_client: AIClient):
        self.ai = ai_client

    def extract(self, prompt: str) -> dict:
        ai_prompt = f"""
You are an expert product analyst.

Analyze the user request and return ONLY valid JSON.

Required JSON format:
{{
  "app_name": "",
  "app_type": "",
  "modules": [],
  "roles": [],
  "features": [],
  "billing": "",
  "assumptions": []
}}

Rules:
- No markdown
- No explanation
- No extra text
- modules must be lowercase words
- roles should include admin,user when suitable

User Request:
{prompt}
"""

        try:
            content = self.ai.generate(ai_prompt)

            # Clean accidental markdown
            content = content.replace("```json", "").replace("```", "").strip()

            data = json.loads(content)

            # Safety defaults
            data.setdefault("app_name", "Generated App")
            data.setdefault("app_type", "web_app")
            data.setdefault("modules", [])
            data.setdefault("roles", ["admin", "user"])
            data.setdefault("features", [])
            data.setdefault("billing", "free")
            data.setdefault("assumptions", [])

            return data

        except Exception:
            # Smart fallback local parser
            text = prompt.lower()

            modules = []

            keywords = {
                "hospital": ["doctors", "patients", "appointments", "billing", "dashboard"],
                "crm": ["login", "contacts", "dashboard"],
                "ecommerce": ["products", "cart", "orders", "payments"],
                "school": ["students", "teachers", "attendance", "fees"],
                "gym": ["members", "trainers", "subscriptions", "payments"],
                "restaurant": ["menu", "orders", "booking", "delivery"]
            }

            app_name = "Generated App"
            app_type = "web_app"

            for key, value in keywords.items():
                if key in text:
                    app_name = key.title() + " Management"
                    app_type = key
                    modules = value
                    break

            if not modules:
                modules = ["dashboard", "users"]

            return {
                "app_name": app_name,
                "app_type": app_type,
                "modules": modules,
                "roles": ["admin", "user"],
                "features": [],
                "billing": "free",
                "assumptions": ["Generated from fallback parser"]
            }