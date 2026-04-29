from pydantic import BaseModel
from typing import Any, Dict

class AppConfig(BaseModel):
    ui_schema: Dict[str, Any]
    api_schema: Dict[str, Any]
    db_schema: Dict[str, Any]
    auth_schema: Dict[str, Any]