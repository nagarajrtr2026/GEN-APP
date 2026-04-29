class Validator:
    def validate(self, schema: dict) -> list[str]:
        errors = []

        # -----------------------------------------
        # EMPTY CHECK
        # -----------------------------------------
        if not schema:
            return ["Empty schema output"]

        # -----------------------------------------
        # REQUIRED KEYS
        # -----------------------------------------
        required_keys = ["ui", "api", "database", "auth"]

        for key in required_keys:
            if key not in schema:
                errors.append(f"Missing key: {key}")

        # -----------------------------------------
        # UI VALIDATION
        # -----------------------------------------
        ui = schema.get("ui", {})
        pages = ui.get("pages", [])

        if not isinstance(pages, list) or not pages:
            errors.append("UI pages missing")

        # -----------------------------------------
        # DATABASE VALIDATION
        # -----------------------------------------
        db = schema.get("database", {})
        tables = db.get("tables", [])

        if not isinstance(tables, list) or not tables:
            errors.append("Database tables missing")

        table_names = []

        for table in tables:
            name = table.get("name")

            if not name:
                errors.append("Table missing name field")
                continue

            table_names.append(str(name).lower())

            if "columns" not in table:
                errors.append(f"Table '{name}' missing columns")

        # -----------------------------------------
        # API VALIDATION
        # -----------------------------------------
        api = schema.get("api", {})
        endpoints = api.get("endpoints", [])

        if not isinstance(endpoints, list) or not endpoints:
            errors.append("API endpoints missing")

        internal_routes = {
            "health",
            "docs",
            "redoc",
            "openapi.json",
            ""
        }

        for ep in endpoints:
            path = ep.get("path")
            method = ep.get("method")

            if not path:
                errors.append("API endpoint missing path")
                continue

            if not method:
                errors.append(f"Endpoint '{path}' missing method")

            if not path.startswith("/"):
                errors.append(f"Invalid endpoint path: {path}")
                continue

            # /users/{id} -> users
            resource = path.strip("/").split("/")[0].lower()

            # Ignore internal routes
            if resource in internal_routes:
                continue

            if resource not in table_names:
                errors.append(f"API refers to missing table: {resource}")

        # -----------------------------------------
        # RELATIONS VALIDATION
        # -----------------------------------------
        relations = db.get("relations", [])
        if not isinstance(relations, list):
            errors.append("Database relations must be a list")
            
        for rel in relations:
            rel_to = rel.get("to", "")
            if rel_to:
                to_table = rel_to.split(".")[0].lower()
                if to_table not in table_names:
                    errors.append(f"Relation refers to missing table: {to_table}")

        # -----------------------------------------
        # API RULES VALIDATION
        # -----------------------------------------
        validation = api.get("validation", {})
        if not isinstance(validation, dict):
            errors.append("API validation must be a dictionary")

        for ep in endpoints:
            method = ep.get("method", "").upper()
            path = ep.get("path", "")
            if method in ["POST", "PUT"]:
                key = f"{method} {path}"
                if key not in validation:
                    errors.append(f"Missing validation rules for {key}")

        # -----------------------------------------
        # AUTH VALIDATION
        # -----------------------------------------
        auth = schema.get("auth", {})
        roles = auth.get("roles", [])

        if not isinstance(roles, list) or not roles:
            errors.append("No roles defined in auth")

        # -----------------------------------------
        # UI ↔ DB VALIDATION
        # -----------------------------------------
        ignore_pages = {"dashboard", "login", "home"}

        for page in pages:
            page_name = page.get("name", "").strip().lower()

            if not page_name:
                continue

            # common utility pages ignore
            if page_name in ignore_pages:
                continue

            if page_name not in table_names:
                errors.append(f"UI page '{page_name}' not linked to DB table")

        # -----------------------------------------
        # REMOVE DUPLICATE ERRORS
        # -----------------------------------------
        errors = list(dict.fromkeys(errors))

        return errors