import json
from app.services.ai_client import AIClient


class SchemaGenerator:
    def __init__(self, ai_client: AIClient):
        self.ai = ai_client

    def generate(self, intent_data: dict, design_data: dict) -> dict:
        """
        Final schema generator.
        Uses intent + system design data.
        Always returns valid structured output.
        """

        # -------------------------------------------------
        # BASE DATA
        # -------------------------------------------------
        app_name = intent_data.get("app_name", "Generated App")
        app_type = intent_data.get("app_type", "web_app")

        modules = intent_data.get("modules", [])
        roles = intent_data.get("roles", ["admin", "user"])
        features = intent_data.get("features", [])
        billing = intent_data.get("billing", "free")

        navigation = design_data.get("navigation", [])
        entities = design_data.get("entities", [])

        # -------------------------------------------------
        # MODULE FALLBACK
        # -------------------------------------------------
        if not modules and navigation:
            modules = [item.lower() for item in navigation]

        if not modules and entities:
            modules = [item.lower() for item in entities]

        if not modules:
            modules = ["dashboard", "users"]

        # -------------------------------------------------
        # UI GENERATION
        # -------------------------------------------------
        pages = []

        for module in modules:
            page = {
                "name": module.title(),
                "components": ["table", "form"]
            }

            if module == "dashboard":
                page["components"] = ["stats", "charts", "cards"]

            if module in ["billing", "payments"]:
                page["components"] = ["table", "payment_form"]

            if module in ["appointments", "booking"]:
                page["components"] = ["calendar", "table", "form"]

            pages.append(page)

        # -------------------------------------------------
        # DATABASE GENERATION
        # -------------------------------------------------
        tables = []

        for module in modules:
            columns = ["id", "name", "created_at"]

            if module in ["users", "doctors", "patients", "students", "teachers"]:
                columns = ["id", "name", "email", "phone", "created_at"]

            if module in ["appointments", "orders", "booking"]:
                columns = ["id", "user_id", "status", "created_at"]

            if module in ["billing", "payments", "fees"]:
                columns = ["id", "amount", "status", "created_at"]

            tables.append({
                "name": module.lower(),
                "columns": columns
            })

        # -------------------------------------------------
        # RELATIONS GENERATION
        # -------------------------------------------------
        relations = []
        table_names = [t["name"] for t in tables]

        for table in tables:
            t_name = table["name"]
            if t_name == "appointments":
                if "patients" in table_names:
                    relations.append({"from": f"{t_name}.patient_id", "to": "patients.id", "type": "many_to_one"})
                if "doctors" in table_names:
                    relations.append({"from": f"{t_name}.doctor_id", "to": "doctors.id", "type": "many_to_one"})
                if "users" in table_names:
                    relations.append({"from": f"{t_name}.user_id", "to": "users.id", "type": "many_to_one"})
            elif t_name == "orders":
                if "users" in table_names:
                    relations.append({"from": f"{t_name}.user_id", "to": "users.id", "type": "many_to_one"})
                if "products" in table_names:
                    relations.append({"from": f"{t_name}.product_id", "to": "products.id", "type": "many_to_one"})
            elif t_name in ["payments", "billing"]:
                if "orders" in table_names:
                    relations.append({"from": f"{t_name}.order_id", "to": "orders.id", "type": "one_to_one"})
                if "patients" in table_names:
                    relations.append({"from": f"{t_name}.patient_id", "to": "patients.id", "type": "many_to_one"})
                if "users" in table_names:
                    relations.append({"from": f"{t_name}.user_id", "to": "users.id", "type": "many_to_one"})
            elif t_name in ["reports", "attendance"]:
                if "students" in table_names:
                    relations.append({"from": f"{t_name}.student_id", "to": "students.id", "type": "many_to_one"})
                if "teachers" in table_names:
                    relations.append({"from": f"{t_name}.teacher_id", "to": "teachers.id", "type": "many_to_one"})
            elif t_name in ["contacts", "leads"]:
                if "users" in table_names:
                    relations.append({"from": f"{t_name}.user_id", "to": "users.id", "type": "many_to_one"})

        # -------------------------------------------------
        # API GENERATION
        # -------------------------------------------------
        endpoints = []

        for module in modules:
            resource = module.lower()

            endpoints.extend([
                {"path": f"/{resource}", "method": "GET"},
                {"path": f"/{resource}", "method": "POST"},
                {"path": f"/{resource}/{{id}}", "method": "PUT"},
                {"path": f"/{resource}/{{id}}", "method": "DELETE"}
            ])

        # -------------------------------------------------
        # VALIDATION GENERATION
        # -------------------------------------------------
        validation = {}
        for ep in endpoints:
            method = ep["method"]
            path = ep["path"]
            if method in ["POST", "PUT"]:
                resource = path.strip("/").split("/")[0].lower()
                prefix = "required" if method == "POST" else "optional"
                
                if resource == "students":
                    rules = {"name": f"{prefix}|min:3|max:100", "email": f"{prefix}|email", "phone": "optional|min:10|max:15"}
                elif resource in ["teachers", "doctors"]:
                    spec = "specialization" if resource == "doctors" else "subject"
                    rules = {"name": f"{prefix}|min:3|max:100", "email": f"{prefix}|email", spec: f"{prefix}|string"}
                elif resource == "patients":
                    rules = {"name": f"{prefix}|min:3|max:100", "email": f"{prefix}|email", "phone": "optional|min:10|max:15"}
                elif resource == "products":
                    rules = {"name": f"{prefix}|min:2", "price": f"{prefix}|number|min:1", "stock": f"{prefix}|integer|min:0"}
                elif resource == "orders":
                    rules = {"user_id": f"{prefix}|integer", "status": f"{prefix}|string", "total": f"{prefix}|number|min:0"}
                elif resource == "appointments":
                    rules = {"patient_id": f"{prefix}|integer", "doctor_id": f"{prefix}|integer", "date": f"{prefix}|date", "status": "optional|string"}
                elif resource == "reports":
                    rules = {"title": f"{prefix}|min:5|max:200", "description": f"{prefix}|string"}
                else:
                    rules = {"name": f"{prefix}|string|min:2"}
                
                key = f"{method} {path}"
                validation[key] = rules

        # -------------------------------------------------
        # AUTH
        # -------------------------------------------------
        if not roles:
            roles = ["admin", "user"]

        # -------------------------------------------------
        # BUSINESS LOGIC
        # -------------------------------------------------
        business_logic = []

        if billing == "premium":
            business_logic.append("Premium subscription unlocks advanced features")

        if "role-based" in features:
            business_logic.append("Role-based access enabled")

        if "appointments" in modules:
            business_logic.append("Appointment scheduling supported")

        if "orders" in modules:
            business_logic.append("Order lifecycle management enabled")

        # -------------------------------------------------
        # ASSUMPTIONS
        # -------------------------------------------------
        assumptions = intent_data.get("assumptions", [])

        if "login" not in modules:
            assumptions.append("Authentication handled globally")

        if "dashboard" not in modules:
            assumptions.append("Dashboard recommended for analytics")

        # remove duplicates
        assumptions = list(dict.fromkeys(assumptions))

        # -------------------------------------------------
        # FINAL OUTPUT
        # -------------------------------------------------
        output = {
            "app_name": app_name,
            "app_type": app_type,
            "ui": {
                "pages": pages
            },
            "api": {
                "endpoints": endpoints,
                "validation": validation
            },
            "database": {
                "tables": tables,
                "relations": relations
            },
            "auth": {
                "roles": roles
            },
            "business_logic": business_logic,
            "assumptions": assumptions
        }

        return output