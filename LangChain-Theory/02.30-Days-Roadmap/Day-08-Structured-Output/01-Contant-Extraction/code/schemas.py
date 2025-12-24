from typing import List, Optional, Literal
from pydantic import BaseModel, Field, EmailStr, conint, confloat

# 1) Contact Extraction
class Contact(BaseModel):
    name: str = Field(..., description="Full name")
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    company: Optional[str] = None

# 2) Job Posting Extraction
class JobPosting(BaseModel):
    title: str
    company: str
    location: Optional[str] = None
    employment_type: Optional[Literal["full-time","part-time","contract","internship","temporary"]] = None
    experience_years: Optional[int] = None
    skills: List[str] = Field(default_factory=list)
    salary_range: Optional[str] = None
    description: Optional[str] = None

# 3) Meeting Minutes (nested)
class ActionItem(BaseModel):
    owner: str
    task: str
    due_date: Optional[str] = None

class MeetingMinutes(BaseModel):
    meeting_title: str
    date: Optional[str] = None
    attendees: List[str] = Field(default_factory=list)
    key_points: List[str] = Field(default_factory=list)
    decisions: List[str] = Field(default_factory=list)
    action_items: List[ActionItem] = Field(default_factory=list)

# 4) Product Review JSON (validation)
class ProductReview(BaseModel):
    product_name: str
    rating: conint(ge=1, le=5)
    sentiment: Literal["positive", "neutral", "negative"]
    pros: List[str] = Field(default_factory=list)
    cons: List[str] = Field(default_factory=list)
    summary: str
    would_recommend: bool

# 5) Ticket Triage (enums + confidence)
class TicketTriage(BaseModel):
    customer_name: Optional[str] = None
    issue: str
    category: Literal["billing", "bug", "feature_request", "account", "other"]
    urgency: Literal["low", "medium", "high"]
    recommended_team: Literal["support", "engineering", "billing"]
    suggested_reply: str
    confidence: confloat(ge=0, le=1)
