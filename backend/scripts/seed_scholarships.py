import json
import os
from sqlalchemy.orm import Session
from app.db.session import SessionLocal, engine
from app.models.scholarship import Scholarship
from app.db.base import Base

# Ensure tables are created
Base.metadata.create_all(bind=engine)

def seed_data():
    db = SessionLocal()
    try:
        # Clear existing data
        db.query(Scholarship).delete()
        
        scholarships = [
            {
                "name": "PM Scholarship Scheme",
                "description": "Scholarship for children of Ex-Servicemen and Ex-Coast Guard personnel for technical and professional education.",
                "eligibility": ["Son/daughter of Ex-Servicemen", "Minimum 60% marks in 12th"],
                "amount": "₹3,000 per month",
                "deadline": "2026-12-31",
                "application_link": "https://ksb.gov.in",
                "category": "Ex-Servicemen, Technical",
                "language_support": ["en", "hi"]
            },
            {
                "name": "Merit-cum-Means Scholarship",
                "description": "For economically weaker sections pursuing higher education in technical or professional courses.",
                "eligibility": ["Family income < ₹2.5 lakh", "Good academic record", "Minority communities"],
                "amount": "₹20,000 per year",
                "deadline": "2026-11-15",
                "application_link": "https://scholarships.gov.in",
                "category": "Merit, Minority, Financial Support",
                "language_support": ["en", "hi"]
            },
            {
                "name": "National Overseas Scholarship (SC)",
                "description": "Financial assistance for SC/ST students to pursue Master's or PhD abroad.",
                "eligibility": ["SC/ST category", "Minimum 60% marks", "Age < 35 years"],
                "amount": "Full tuition + Allowance",
                "deadline": "2026-03-31",
                "application_link": "https://nosmsje.gov.in",
                "category": "SC, ST, International",
                "language_support": ["en"]
            },
            {
                "name": "AICTE Pragati Scholarship for Girls",
                "description": "To empower girls pursuing technical education in AICTE approved institutions.",
                "eligibility": ["Female students", "Family income < 8 LPA", "Maximum 2 girls per family"],
                "amount": "₹50,000 per year",
                "deadline": "2026-10-31",
                "application_link": "https://aicte-india.org",
                "category": "Girls, Engineering, Technical",
                "language_support": ["en", "hi"]
            },
            {
                "name": "INSPIRE Scholarship for Higher Education",
                "description": "To attract students to pursue natural sciences at the undergraduate level.",
                "eligibility": ["Top 1% in 12th Board", "Pursuing B.Sc/M.Sc", "Science stream"],
                "amount": "₹80,000 per year",
                "deadline": "2026-06-30",
                "application_link": "https://online-inspire.gov.in",
                "category": "Science, Merit",
                "language_support": ["en"]
            },
            {
                "name": "National Scholarship for Persons with Disabilities",
                "description": "Support for students with disabilities to pursue diploma and graduate courses.",
                "eligibility": ["40% or more disability", "Income < 2.5 LPA", "Academic merit"],
                "amount": "₹25,000 per year",
                "deadline": "2026-09-30",
                "application_link": "https://scholarships.gov.in",
                "category": "Disability, PWD",
                "language_support": ["en", "hi"]
            },
            {
                "name": "Sitaram Jindal Foundation Scholarship",
                "description": "Merit-based financial assistance for students in various categories from Class 11 to PG.",
                "eligibility": ["Based on class results", "Open to all categories", "Income certificate required"],
                "amount": "₹500 to ₹3,200 per month",
                "deadline": "2026-12-15",
                "application_link": "https://sitaramjindalfoundation.org",
                "category": "General, Merit, Financial Support",
                "language_support": ["en"]
            },
            {
                "name": "HDFC Bank Badhte Kadam Scholarship",
                "description": "Support for high-performing students who have faced crises like loss of parent.",
                "eligibility": ["Class 10 to PG", "Crisis condition", "Minimum 60% marks"],
                "amount": "Up to ₹1,00,000",
                "deadline": "2026-08-31",
                "application_link": "https://buddy4study.com",
                "category": "Financial Support, Crisis",
                "language_support": ["en", "hi"]
            },
            {
                "name": "L'Oréal India For Young Women In Science",
                "description": "Specifically for young women who have passed Class 12 in Science and want to pursue STEM.",
                "eligibility": ["Female students", "PCB/PCM stream", "Minimum 85% in Class 12"],
                "amount": "₹2.5 Lakh over 3-4 years",
                "deadline": "2026-07-15",
                "application_link": "https://loreal.com",
                "category": "STEM, Girls, Science",
                "language_support": ["en"]
            },
            {
                "name": "UGC PG Merit Scholarship for University Rank Holders",
                "description": "For first and second rank holders at the undergraduate level in various universities.",
                "eligibility": ["1st/2nd Rank in UG", "Pursuing PG", "Age < 30 years"],
                "amount": "₹3,100 per month",
                "deadline": "2026-10-15",
                "application_link": "https://ugc.ac.in",
                "category": "Merit, Post-Graduate",
                "language_support": ["en"]
            }
        ]
        
        for s in scholarships:
            db_scholarship = Scholarship(
                name=s["name"],
                description=s["description"],
                eligibility=json.dumps(s["eligibility"]),
                amount=s["amount"],
                deadline=s["deadline"],
                application_link=s["application_link"],
                category=s["category"],
                language_support=json.dumps(s["language_support"])
            )
            db.add(db_scholarship)
        
        db.commit()
        print(f"Successfully seeded {len(scholarships)} scholarships.")
    except Exception as e:
        db.rollback()
        print(f"Error seeding data: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    seed_data()
