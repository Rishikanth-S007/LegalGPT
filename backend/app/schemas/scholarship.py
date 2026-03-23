from pydantic import BaseModel
from typing import List

class ScholarshipBase(BaseModel):
    name: str
    description: str
    eligibility: List[str]
    amount: str
    deadline: str
    application_link: str
    category: str
    language_support: List[str]

    class Config:
        from_attributes = True
