from pydantic import BaseModel, Field, EmailStr
from typing import Optional, Literal, Annotated
from datetime import date

class StudentSchema(BaseModel):

    id: Annotated[Optional[int], Field(default=None,description="Student ID")]
    name: str = Field(..., min_length=2, max_length=50, description="Full name of the student")
    age: int = Field(..., gt=0, le=100, description="Age of the student (1-100)")
    email: EmailStr = Field(..., description="Email address (must be valid format)")
    enrolled_date: Optional[date] = Field(default_factory=date.today, description="Enrollment date (defaults to today)")

    class Config:
        from_attributes = True  # Needed when returning SQLAlchemy models as responses
