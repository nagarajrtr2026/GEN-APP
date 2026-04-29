import json
from app.services.ai_client import AIClient


class SystemDesigner:
    def __init__(self, ai_client: AIClient):
        self.ai = ai_client

    def design(self, intent: dict) -> dict:
        ai_prompt = f"""
You are a senior software solution architect.

Based on the given intent, design the system and return ONLY valid JSON.

Required JSON format:
{{
  "entities": [],
  "flows": [],
  "permissions": {{}},
  "navigation": []
}}

Rules:
- No markdown
- No explanation
- No extra text
- entities = database/business objects
- flows = user journeys
- permissions = role based access
- navigation = pages/modules

Intent:
{json.dumps(intent)}
"""

        try:
            content = self.ai.generate(ai_prompt)

            # Clean accidental markdown
            content = content.replace("```json", "").replace("```", "").strip()

            data = json.loads(content)

            # Safety defaults
            data.setdefault("entities", [])
            data.setdefault("flows", [])
            data.setdefault("permissions", {})
            data.setdefault("navigation", [])

            return data

        except Exception:
            # ---------- Smart Fallback ----------
            modules = intent.get("modules", [])
            roles = intent.get("roles", ["admin", "user"])

            entities = []
            flows = []
            navigation = []

            for module in modules:
                entity_name = module[:-1].title() if module.endswith("s") else module.title()
                entities.append(entity_name)
                navigation.append(module.title())
                flows.append(f"Manage {module.title()}")

            permissions = {}

            for role in roles:
                if role == "admin":
                    permissions[role] = "full_access"
                else:
                    permissions[role] = "limited_access"

            if not entities:
                entities = ["User"]

            if not navigation:
                navigation = ["Dashboard"]

            if not flows:
                flows = ["View Dashboard"]

            return {
                "entities": entities,
                "flows": flows,
                "permissions": permissions,
                "navigation": navigation
            }