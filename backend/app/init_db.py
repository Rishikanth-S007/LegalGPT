import json
from app.db.session import SessionLocal, engine
from app.db.base import Base
from app.models.scholarship import Scholarship

# Create tables
Base.metadata.create_all(bind=engine)

def seed_database():
    db = SessionLocal()
    
    # Check if we already have data
    if db.query(Scholarship).count() > 0:
        print("Database already seeded with scholarships!")
        db.close()
        return

    scholarships_data = [
        {
            "name": "PM Scholarship Scheme",
            "description": "Scholarship for children of Ex-Servicemen and Ex-Coast Guard personnel",
            "eligibility": json.dumps(["Son/daughter of Ex-Servicemen", "Minimum 60% marks in 12th", "Age below 30 years"]),
            "amount": "₹3,000 per month",
            "deadline": "2026-12-31",
            "application_link": "https://ksb.gov.in",
            "category": "merit,defence,general",
            "language_support": json.dumps(["en", "hi"])
        },
        {
            "name": "Merit-cum-Means Scholarship",
            "description": "For economically weaker sections pursuing higher education",
            "eligibility": json.dumps(["Family income below ₹2.5 lakh per year", "Minimum 50% marks in previous exam", "Pursuing degree/diploma course"]),
            "amount": "₹20,000 per year",
            "deadline": "2026-10-31",
            "application_link": "https://scholarships.gov.in",
            "category": "merit,means,engineering,general",
            "language_support": json.dumps(["en", "hi"])
        },
        {
            "name": "AICTE Technical Education Scholarship",
            "description": "For students pursuing engineering and technical courses",
            "eligibility": json.dumps(["Enrolled in AICTE approved institution", "Engineering or Technical stream", "Minimum 60% marks", "Family income below ₹8 lakh"]),
            "amount": "₹50,000 per year",
            "deadline": "2026-09-30",
            "application_link": "https://aicte-india.org",
            "category": "engineering,technical,merit",
            "language_support": json.dumps(["en", "hi"])
        },
        {
            "name": "National Scholarship Portal - Central Sector",
            "description": "For college and university students scoring above 80% in Class 12",
            "eligibility": json.dumps(["Above 80% in Class 12 board exam", "Family income below ₹8 lakh per year", "Pursuing undergraduate course"]),
            "amount": "₹12,000 per year",
            "deadline": "2026-11-30",
            "application_link": "https://scholarships.gov.in",
            "category": "merit,general,engineering",
            "language_support": json.dumps(["en", "hi"])
        },
        {
            "name": "Post Matric Scholarship for SC Students",
            "description": "For Scheduled Caste students pursuing post-matriculation education",
            "eligibility": json.dumps(["SC category certificate required", "Pursuing post-matriculation course", "Family income below ₹2.5 lakh"]),
            "amount": "₹23,000 per year",
            "deadline": "2026-10-15",
            "application_link": "https://scholarships.gov.in",
            "category": "sc,reserved,engineering,general",
            "language_support": json.dumps(["en", "hi"])
        },
        {
            "name": "Post Matric Scholarship for ST Students",
            "description": "For Scheduled Tribe students pursuing higher education",
            "eligibility": json.dumps(["ST category certificate required", "Pursuing post-matriculation course", "Any income limit"]),
            "amount": "₹15,000 per year",
            "deadline": "2026-10-15",
            "application_link": "https://scholarships.gov.in",
            "category": "st,reserved,engineering,general",
            "language_support": json.dumps(["en", "hi"])
        },
        {
            "name": "Minority Community Scholarship",
            "description": "For students from minority communities pursuing education",
            "eligibility": json.dumps(["Minority community certificate", "Minimum 50% marks in previous exam", "Family income below ₹2 lakh"]),
            "amount": "₹15,000 per year",
            "deadline": "2026-09-30",
            "application_link": "https://scholarships.gov.in",
            "category": "minority,merit,general",
            "language_support": json.dumps(["en", "hi"])
        },
        {
            "name": "Pragati Scholarship for Girls in Technical Education",
            "description": "AICTE scholarship exclusively for girl students in technical courses",
            "eligibility": json.dumps(["Girl student only", "Enrolled in AICTE approved institution", "Family income below ₹8 lakh", "Only one girl per family"]),
            "amount": "₹50,000 per year",
            "deadline": "2026-09-30",
            "application_link": "https://aicte-india.org",
            "category": "girls,engineering,technical,merit",
            "language_support": json.dumps(["en", "hi"])
        },
        {
            "name": "Saksham Scholarship for Disabled Students",
            "description": "For differently-abled students pursuing technical education",
            "eligibility": json.dumps(["40% or more disability certificate", "Enrolled in AICTE approved institution", "Family income below ₹8 lakh"]),
            "amount": "₹50,000 per year",
            "deadline": "2026-09-30",
            "application_link": "https://aicte-india.org",
            "category": "disabled,engineering,technical",
            "language_support": json.dumps(["en", "hi"])
        },
        {
            "name": "Inspire Scholarship for Higher Education",
            "description": "DST scholarship for students pursuing natural sciences",
            "eligibility": json.dumps(["Top 1% in Class 12 board exam", "Pursuing BSc or integrated MSc", "Age below 22 years"]),
            "amount": "₹80,000 per year",
            "deadline": "2026-11-30",
            "application_link": "https://online-inspire.gov.in",
            "category": "science,merit,general",
            "language_support": json.dumps(["en", "hi"])
        }
    ]

    for data in scholarships_data:
        scholarship = Scholarship(**data)
        db.add(scholarship)
    
    db.commit()
    print("Successfully seeded 10 scholarships into the database!")
    db.close()

if __name__ == "__main__":
    seed_database()
