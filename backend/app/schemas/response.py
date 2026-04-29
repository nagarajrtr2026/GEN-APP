from pydantic import BaseModel
from typing import Any, Dict, Optional

class GenerateResponse(BaseModel):
    success: bool
    data: Optional[Dict[str, Any]] = None
    error: Optional[str] = None