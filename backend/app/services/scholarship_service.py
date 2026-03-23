from typing import List, Dict
import json
from datetime import datetime

from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.models.scholarship import Scholarship

class ScholarshipService:
    def __init__(self):
        # We now query directly from the database instead of mocked data
        pass
    
    async def search_scholarships(self, query: str, filters: Dict = None, language: str = "en") -> Dict:
        """Search scholarships based on query and filters from the database"""
        
        matching_scholarships = []
        query_lower = query.lower()
        
        # Create a new DB session for the search
        db: Session = SessionLocal()
        try:
            # Query all scholarships for simplicity. Can be optimized into a SQL ILIKE query later.
            all_scholarships = db.query(Scholarship).all()
            
            for scholarship_model in all_scholarships:
                # Convert model to dict format expected by matching engine
                scholarship = {
                    "name": scholarship_model.name,
                    "description": scholarship_model.description,
                    "eligibility": json.loads(scholarship_model.eligibility) if scholarship_model.eligibility else [],
                    "amount": scholarship_model.amount,
                    "deadline": scholarship_model.deadline,
                    "application_link": scholarship_model.application_link,
                    "category": scholarship_model.category,
                    "language_support": json.loads(scholarship_model.language_support) if scholarship_model.language_support else ["en", "hi"]
                }
                
                # Check match and get relevance score
                score = self._get_relevance_score(scholarship, query_lower, filters)
                if score > 0:
                    # Format scholarship based on language
                    formatted_scholarship = self._format_scholarship(scholarship, language)
                    matching_scholarships.append((score, formatted_scholarship))
            
            # Sort by relevance score (highest first) and extract scholarships
            matching_scholarships.sort(key=lambda x: x[0], reverse=True)
            matching_scholarships = [s[1] for s in matching_scholarships]
            
            # If no matches, return most popular scholarships (top 3)
            if not matching_scholarships:
                matching_scholarships = []
                for s_model in all_scholarships[:3]:
                    s = {
                        "name": s_model.name,
                        "description": s_model.description,
                        "eligibility": json.loads(s_model.eligibility) if s_model.eligibility else [],
                        "amount": s_model.amount,
                        "deadline": s_model.deadline,
                        "application_link": s_model.application_link,
                        "category": s_model.category,
                        "language_support": json.loads(s_model.language_support) if s_model.language_support else ["en", "hi"]
                    }
                    matching_scholarships.append(self._format_scholarship(s, language))
        finally:
            db.close()
        
        return {
            "query": query,
            "scholarships": matching_scholarships,
            "total_found": len(matching_scholarships),
            "language": language,
            "search_tips": self._get_search_tips(language)
        }
    
    def _get_relevance_score(self, scholarship: Dict, query: str, filters: Dict) -> int:
        """Calculate relevance score for scholarship based on query (higher = more relevant)"""
        
        query_lower = query.lower()
        score = 0
        
        # Stop-words to ignore for broad matching
        stop_words = {"scholarship", "scheme", "for", "the", "and", "under", "graduate", "students", "india", "national"}
        
        # Synonym mappings for better matching
        synonyms = {
            "disability": ["disabled", "differently-abled", "handicapped"],
            "disabled": ["disability", "differently-abled", "handicapped"],
            "girl": ["girls", "female", "women"],
            "girls": ["girl", "female", "women"],
            "engineering": ["technical", "engineer"],
            "technical": ["engineering", "engineer"]
        }
        
        # Get categories
        categories = [cat.strip().lower() for cat in scholarship['category'].split(',')]
        
        # Extract meaningful query words
        query_words = [w for w in query_lower.split() if w not in stop_words and len(w) >= 2]
        
        # Expand query words with synonyms
        expanded_words = set(query_words)
        for word in query_words:
            if word in synonyms:
                expanded_words.update(synonyms[word])
        
        # Score 1: Exact category match (highest priority)
        for cat in categories:
            if cat in expanded_words or any(cat == word for word in expanded_words):
                score += 100
        
        # Score 2: Name contains query word (high priority)
        name_lower = scholarship['name'].lower()
        for word in expanded_words:
            if word in name_lower:
                score += 50
        
        # Score 3: Category substring match
        for cat in categories:
            for word in expanded_words:
                if word in cat or cat in word:
                    score += 30
        
        # Score 4: Description contains query word
        desc_lower = scholarship['description'].lower()
        for word in expanded_words:
            if word in desc_lower:
                score += 10
        
        # Score 5: Exact phrase match in name (bonus)
        if query_lower in name_lower:
            score += 80
        
        return score
    
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
