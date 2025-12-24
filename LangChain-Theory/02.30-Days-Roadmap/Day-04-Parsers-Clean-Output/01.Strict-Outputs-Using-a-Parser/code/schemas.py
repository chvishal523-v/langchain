from pydantic import BaseModel, Field
from typing import Literal

class Ticket(BaseModel):
    name: str = Field(..., description="Customer name")
    issue: str = Field(..., description="What problem they report")
    urgency: Literal["low", "medium", "high"] = Field(..., description="Urgency level")
