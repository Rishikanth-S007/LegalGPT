from typing import List, Dict
import json
from datetime import datetime

class ScholarshipService:
    def __init__(self):
        # Mock scholarship database - you can later connect to real APIs
        self.scholarships_db = [
            {
                "name": "PM Scholarship Scheme",
                "description": "Scholarship for children of Ex-Servicemen and Ex-Coast Guard personnel",
                "eligibility": ["Son/daughter of Ex-Servicemen", "Minimum 60% marks in 12th"],
                "amount": "₹3,000 per month",
                "deadline": "2025-12-31",
                "application_link": "https://ksb.gov.in",
                "category": "defense",
                "language_support": ["en", "hi"]
            },
            {
                "name": "Merit-cum-Means Scholarship",
                "description": "For economically weaker sections pursuing higher education",
                "eligibility": ["Family income < ₹2.5 lakh", "Good academic record"],
                "amount": "₹20,000 per year",
                "deadline": "2025-01-15",
                "application_link": "https://scholarships.gov.in",
                "category": "economic",
                "language_support": ["en", "hi"]
            },
            {
                "name": "Minority Scholarship",
                "description": "Scholarship for students from minority communities",
                "eligibility": ["Minority community certificate", "Merit-based selection"],
                "amount": "₹15,000 per year",
                "deadline": "2025-02-28",
                "application_link": "https://scholarships.gov.in",
                "category": "minority",
                "language_support": ["en", "hi"]
            },
            {
                "name": "Girl Child Education Scholarship",
                "description": "Special scholarship to promote girl child education",
                "eligibility": ["Female students", "Academic excellence"],
                "amount": "₹25,000 per year",
                "deadline": "2025-03-31",
                "application_link": "https://scholarships.gov.in",
                "category": "gender",
                "language_support": ["en", "hi"]
            },
            {
                "name": "Technical Education Scholarship",
                "description": "For students pursuing engineering and technical courses",
                "eligibility": ["Engineering/Technical stream", "Merit-based"],
                "amount": "₹50,000 per year",
                "deadline": "2025-06-30",
                "application_link": "https://aicte-india.org",
                "category": "technical",
                "language_support": ["en", "hi"]
            }
        ]
    
    async def search_scholarships(self, query: str, filters: Dict = None, language: str = "en") -> Dict:
        """Search scholarships based on query and filters"""
        
        matching_scholarships = []
        query_lower = query.lower()
        
        for scholarship in self.scholarships_db:
            # Simple keyword matching
            if self._matches_query(scholarship, query_lower, filters):
                # Format scholarship based on language
                formatted_scholarship = self._format_scholarship(scholarship, language)
                matching_scholarships.append(formatted_scholarship)
        
        # If no matches, return most popular scholarships
        if not matching_scholarships:
            matching_scholarships = [
                self._format_scholarship(s, language) 
                for s in self.scholarships_db[:3]
            ]
        
        return {
            "query": query,
            "scholarships": matching_scholarships,
            "total_found": len(matching_scholarships),
            "language": language,
            "search_tips": self._get_search_tips(language)
        }
    
    def _matches_query(self, scholarship: Dict, query: str, filters: Dict) -> bool:
        """Check if scholarship matches the search query"""
        
        # Check name and description
        searchable_text = f"{scholarship['name']} {scholarship['description']}".lower()
        
        # Basic keyword matching
        query_words = query.split()
        for word in query_words:
            if word in searchable_text:
                return True
        
        # Category-based matching
        category_keywords = {
            "government": ["pm", "government", "ministry"],
            "merit": ["merit", "academic", "excellence"],
            "minority": ["minority", "muslim", "christian"],
            "girl": ["girl", "female", "women"],
            "technical": ["engineering", "technical", "computer"]
        }
        
        for category, keywords in category_keywords.items():
            if any(keyword in query for keyword in keywords):
                if scholarship["category"] == category or category in scholarship["category"]:
                    return True
        
        return False
    
    def _format_scholarship(self, scholarship: Dict, language: str) -> Dict:
        """Format scholarship information based on language"""
        
        if language == "hi":
            return {
                "name": scholarship["name"],  # Keep English name for official reference
                "description": scholarship["description"],  # You can add Hindi translations
                "eligibility": scholarship["eligibility"],
                "amount": scholarship["amount"],
                "deadline": scholarship["deadline"],
                "application_link": scholarship["application_link"],
                "status": "सक्रिय" if self._is_active(scholarship["deadline"]) else "समाप्त"
            }
        else:
            return {
                "name": scholarship["name"],
                "description": scholarship["description"],
                "eligibility": scholarship["eligibility"],
                "amount": scholarship["amount"],
                "deadline": scholarship["deadline"],
                "application_link": scholarship["application_link"],
                "status": "Active" if self._is_active(scholarship["deadline"]) else "Expired"
            }
    
    def _is_active(self, deadline: str) -> bool:
        """Check if scholarship deadline is still active"""
        try:
            deadline_date = datetime.strptime(deadline, "%Y-%m-%d")
            return deadline_date > datetime.now()
        except:
            return True  # Assume active if can't parse date
    
    def _get_search_tips(self, language: str) -> List[str]:
        """Provide search tips to users"""
        if language == "hi":
            return [
                "विशिष्ट श्रेणी खोजें जैसे 'इंजीनियरिंग छात्रवृत्ति'",
                "अपनी पात्रता के आधार पर खोजें",
                "नवीनतम समय सीमा की जांच करें"
            ]
        else:
            return [
                "Search for specific categories like 'engineering scholarship'",
                "Search based on your eligibility criteria",
                "Check latest deadlines and requirements"
            ]

# Global scholarship service instance
scholarship_service = ScholarshipService()
