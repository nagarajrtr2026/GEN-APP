class RepairEngine:
    def repair(self, schema: dict, errors: list[str]) -> dict:
        if not schema:
            return {}

        # -----------------------------------------
        # SAFE DEFAULT STRUCTURE
        # -----------------------------------------
        schema.setdefault("ui", {}).setdefault("pages", [])
        schema.setdefault("api", {}).setdefault("endpoints", [])
        schema["api"].setdefault("validation", {})
        schema.setdefault("database", {}).setdefault("tables", [])
        schema["database"].setdefault("relations", [])
        schema.setdefault("auth", {}).setdefault("roles", ["admin", "user"])

        internal_routes = {"health", "docs", "redoc", "openapi.json"}

        # -----------------------------------------
        # HELPER: CURRENT TABLE NAMES
        # -----------------------------------------
        def get_table_names():
            return {
                t.get("name", "").lower()
                for t in schema["database"]["tables"]
                if t.get("name")
            }

        # -----------------------------------------
        # FIX DATABASE MISSING
        # -----------------------------------------
        if any("Database tables missing" in e for e in errors):
            schema["database"]["tables"] = [
                {
                    "name": "users",
                    "columns": ["id", "name", "email", "created_at"]
                }
            ]

        # -----------------------------------------
        # FIX UI MISSING
        # -----------------------------------------
        if any("UI pages missing" in e for e in errors):
            schema["ui"]["pages"] = [
                {
                    "name": "Dashboard",
                    "components": ["stats", "charts", "cards"]
                }
            ]

        # -----------------------------------------
        # FIX API MISSING
        # -----------------------------------------
        if any("API endpoints missing" in e for e in errors):
            schema["api"]["endpoints"] = [
                {"path": "/users", "method": "GET"},
                {"path": "/users", "method": "POST"},
                {"path": "/users/{id}", "method": "PUT"},
                {"path": "/users/{id}", "method": "DELETE"},
            ]

        # -----------------------------------------
        # FIX AUTH MISSING
        # -----------------------------------------
        if any("No roles defined in auth" in e for e in errors):
            schema["auth"]["roles"] = ["admin", "user"]

        # -----------------------------------------
        # FIX API ↔ DB MISMATCH
        # -----------------------------------------
        for error in errors:
            if "API refers to missing table:" in error:
                missing_table = error.split(":")[-1].strip().lower()

                if missing_table in internal_routes:
                    continue

                if missing_table not in get_table_names():
                    schema["database"]["tables"].append({
                        "name": missing_table,
                        "columns": ["id", "name", "created_at"]
                    })

        # -----------------------------------------
        # FIX UI ↔ DB MISMATCH
        # -----------------------------------------
        ignore_pages = {"dashboard", "login", "home"}

        for page in schema["ui"]["pages"]:
            page_name = page.get("name", "").strip().lower()

            if not page_name:
                continue

            if page_name in ignore_pages:
                continue

            if page_name not in get_table_names():
                schema["database"]["tables"].append({
                    "name": page_name,
                    "columns": ["id", "name", "created_at"]
                })

        # -----------------------------------------
        # REMOVE DUPLICATE TABLES
        # -----------------------------------------
        unique_tables = []
        seen = set()

        for table in schema["database"]["tables"]:
            name = table.get("name", "").lower()

            if name and name not in seen:
                seen.add(name)
                unique_tables.append(table)

        schema["database"]["tables"] = unique_tables

        # -----------------------------------------
        # FIX RELATIONS MISSING OR INVALID
        # -----------------------------------------
        valid_relations = []
        for rel in schema["database"].get("relations", []):
            rel_to = rel.get("to", "")
            if rel_to:
                to_table = rel_to.split(".")[0].lower()
                if to_table in get_table_names():
                    valid_relations.append(rel)
        schema["database"]["relations"] = valid_relations

        # -----------------------------------------
        # FIX API RULES MISSING
        # -----------------------------------------
        for error in errors:
            if "Missing validation rules for" in error:
                key = error.replace("Missing validation rules for", "").strip()
                schema["api"]["validation"][key] = {
                    "data": "required|string"
                }

        # -----------------------------------------
        # REMOVE DUPLICATE ENDPOINTS
        # -----------------------------------------
        unique_endpoints = []
        seen_routes = set()

        for ep in schema["api"]["endpoints"]:
            key = f"{ep.get('method')}:{ep.get('path')}"

            if key not in seen_routes:
                seen_routes.add(key)
                unique_endpoints.append(ep)

        schema["api"]["endpoints"] = unique_endpoints

        return schema