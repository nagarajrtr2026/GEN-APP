from app.services.ai_client import AIClient
from app.services.intent_extractor import IntentExtractor
from app.services.system_designer import SystemDesigner
from app.services.schema_generator import SchemaGenerator
from app.services.validator import Validator
from app.services.repair_engine import RepairEngine


class Pipeline:
    def __init__(self):
        self.ai_client = AIClient()
        self.extractor = IntentExtractor(self.ai_client)
        self.designer = SystemDesigner(self.ai_client)
        self.generator = SchemaGenerator(self.ai_client)
        self.validator = Validator()
        self.repair_engine = RepairEngine()

    def format_output(self, schema: dict) -> dict:
        """
        Final cleanup layer:
        - consistent key order
        - remove duplicates
        - clean naming
        """

        ordered = {
            "app_name": schema.get("app_name", "Generated App"),
            "app_type": schema.get("app_type", "web_app"),
            "ui": schema.get("ui", {}),
            "api": schema.get("api", {}),
            "database": schema.get("database", {}),
            "auth": schema.get("auth", {}),
            "business_logic": schema.get("business_logic", []),
            "assumptions": schema.get("assumptions", [])
        }

        # -------- Clean UI Pages --------
        pages = ordered["ui"].get("pages", [])
        seen_pages = set()
        clean_pages = []

        for page in pages:
            name = page.get("name", "").strip().lower()

            if name and name not in seen_pages:
                seen_pages.add(name)

                page["name"] = name.title()
                clean_pages.append(page)

        ordered["ui"]["pages"] = clean_pages

        # -------- Clean DB Tables --------
        tables = ordered["database"].get("tables", [])
        seen_tables = set()
        clean_tables = []

        for table in tables:
            name = table.get("name", "").strip().lower()

            if name and name not in seen_tables:
                seen_tables.add(name)

                table["name"] = name
                clean_tables.append(table)

        ordered["database"]["tables"] = clean_tables

        # -------- Clean Relations --------
        relations = ordered["database"].get("relations", [])
        seen_relations = set()
        clean_relations = []
        for rel in relations:
            key = f"{rel.get('from')}->{rel.get('to')}"
            if key not in seen_relations:
                seen_relations.add(key)
                clean_relations.append(rel)
        ordered["database"]["relations"] = clean_relations

        # -------- Clean API Endpoints --------
        endpoints = ordered["api"].get("endpoints", [])
        seen_endpoints = set()
        clean_endpoints = []

        for ep in endpoints:
            path = ep.get("path", "").strip()
            method = ep.get("method", "").upper()

            key = f"{method}:{path}"

            if path and method and key not in seen_endpoints:
                seen_endpoints.add(key)

                ep["method"] = method
                clean_endpoints.append(ep)

        ordered["api"]["endpoints"] = clean_endpoints

        # -------- Clean Roles --------
        roles = ordered["auth"].get("roles", [])
        clean_roles = []

        for role in roles:
            role_name = str(role).strip().lower()

            if role_name and role_name not in clean_roles:
                clean_roles.append(role_name)

        ordered["auth"]["roles"] = clean_roles

        return ordered

    def run(self, prompt: str) -> dict:
        if not prompt or not prompt.strip():
            raise ValueError("Invalid empty prompt")

        # -------- Stage 1: Intent Extraction --------
        intent = self.extractor.extract(prompt) or {}

        # -------- Stage 2: System Design --------
        design = self.designer.design(intent) or {}

        # -------- Stage 3: Schema Generation --------
        schemas = self.generator.generate(intent, design)

        # -------- Stage 4: Validation --------
        errors = self.validator.validate(schemas)

        print("VALIDATION ERRORS:", errors)

        # -------- Stage 5: Repair --------
        if errors:
            print("BEFORE REPAIR:", schemas)
            schemas = self.repair_engine.repair(schemas, errors)
            print("AFTER REPAIR:", schemas)

        # -------- Stage 6: Final Formatting --------
        schemas = self.format_output(schemas)

        print("FINAL CLEAN OUTPUT:", schemas)

        return schemas