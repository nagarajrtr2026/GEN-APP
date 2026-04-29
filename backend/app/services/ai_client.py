import json
from groq import Groq
from app.core.config import settings


class AIClient:
    def __init__(self):
        self.provider = settings.AI_PROVIDER.lower()
        self.api_key = settings.API_KEY
        self.client = None

        # -------- GROQ --------
        if self.provider == "groq" and self.api_key:
            self.client = Groq(api_key=self.api_key)

    def generate(self, prompt: str) -> str:
        provider_map = {
            "dummy": self._dummy_generate,
            "groq": self._groq_generate,
            "claude": self._claude_generate,
            "openai": self._openai_generate,
        }

        handler = provider_map.get(self.provider, self._dummy_generate)
        return handler(prompt)

    # ---------------------------------------------------
    # DUMMY FALLBACK
    # ---------------------------------------------------
    def _dummy_generate(self, prompt: str) -> str:
        return json.dumps({
            "app_name": "Dummy App",
            "app_type": "web_app",
            "modules": ["dashboard", "users"],
            "roles": ["admin", "user"],
            "features": [],
            "billing": "free",
            "assumptions": ["Fallback response used"]
        })

    # ---------------------------------------------------
    # GROQ PROVIDER
    # ---------------------------------------------------
    def _groq_generate(self, prompt: str) -> str:
        try:
            completion = self.client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[
                    {
                        "role": "system",
                        "content": """
You are an expert SaaS product architect.

Return ONLY valid JSON.
No markdown.
No explanation.
No extra text.

Rules:
- Always return machine-readable JSON
- Use arrays where needed
- Keep module names lowercase
- Keep responses concise
"""
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.1,
                max_tokens=800
            )

            content = completion.choices[0].message.content.strip()

            # Clean accidental markdown wrappers
            content = content.replace("```json", "").replace("```", "").strip()

            # Validate JSON before returning
            json.loads(content)

            return content

        except Exception as e:
            print("Groq Error:", e)
            return self._dummy_generate(prompt)

    # ---------------------------------------------------
    # PLACEHOLDERS
    # ---------------------------------------------------
    def _claude_generate(self, prompt: str) -> str:
        return self._dummy_generate(prompt)

    def _openai_generate(self, prompt: str) -> str:
        return self._dummy_generate(prompt)