from sqlalchemy import Column, Integer, String, Text, Date
from app.db.base import Base

class Scholarship(Base):
    __tablename__ = "scholarships"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    description = Column(Text, nullable=False)
    eligibility = Column(String, nullable=False) # Store as JSON string or comma separated
    amount = Column(String, nullable=False)
    deadline = Column(String, nullable=False) # e.g. "2025-12-31" or Date
    application_link = Column(String, nullable=False)
    category = Column(String, index=True, nullable=False)
    language_support = Column(String, nullable=False) # Store as JSON string, e.g. '["en", "hi"]'
