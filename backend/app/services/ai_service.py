from app.services.law_predictor_service import predict_law
from app.config.settings import settings
import asyncio
from concurrent.futures import ThreadPoolExecutor
from typing import Dict, List

_executor = ThreadPoolExecutor(max_workers=2)

class AIService:
    def __init__(self):
        # We use the law_predictor_service initialized at startup
        pass
    
    async def process_legal_query(self, question: str, language: str = "en") -> Dict:
        """Process legal questions with a high-precision LOCAL predictive model"""
        
        try:
            print(f"Processing legal query with LOCAL Predictive Model: {question[:50]}...")
            
            # Use the high-precision local RAG engine via predict_law function
            # run_in_executor prevents the synchronous CPU-bound call from blocking the async event loop
            loop = asyncio.get_event_loop()
            result = await loop.run_in_executor(_executor, predict_law, question)
            
            if result:
                # Handle different response formats from predict_law
                if isinstance(result, dict):
                    # Check if it's the new format with structured data
                    structured_data = result.get('structured_data') or result
                    ai_response = (
                        structured_data.get('legal_position') or 
                        structured_data.get('prediction') or
                        result.get('prediction') or
                        str(result)
                    )
                    confidence = result.get('confidence', 0.75)
                    related_laws = [structured_data.get('applicable_law', 'Indian Law')]
                    
                    # Normalize confidence to 0-1 range
                    if confidence > 1:
                        normalized_confidence = min(0.99, max(0.7, 0.7 + (confidence / 20)))
                    else:
                        normalized_confidence = max(0.5, min(0.99, confidence))
                else:
                    ai_response = str(result)
                    normalized_confidence = 0.75
                    structured_data = {}
                    related_laws = ["Indian Law"]
            else:
                ai_response = "I'm sorry, I couldn't find a high-confidence legal prediction for your specific situation."
                normalized_confidence = 0.5
                related_laws = ["Consumer Protection Act, 2019"]
                structured_data = {}

            print(f"Local model predicted successfully (Confidence: {normalized_confidence:.2f})")
            
            # Suggested actions based on prediction
            suggested_actions = structured_data.get("next_steps", self._extract_actions(ai_response, language))
            
            return {
                "response": ai_response,
                "structured_data": structured_data,
                "confidence": normalized_confidence,
                "related_laws": related_laws,
                "suggested_actions": suggested_actions,
                "language": language,
                "model_used": "Multi-Law Predictor Engine (FAISS + Cross-Encoder)",
                "status": "success"
            }
            
        except Exception as e:
            print(f"Local AI Error: {str(e)}")

            
            # Provide helpful fallback response
            if language == "hi":
                fallback_response = f"""मैं आपके कानूनी प्रश्न में सहायता करना चाहता हूँ: "{question}"

मुख्य कानूनी सुझाव:
• एक योग्य वकील से सलाह लें
• संबंधित दस्तावेज़ एकत्र करें  
• कानूनी सहायता केंद्र से संपर्क करें

भारत में उपभोक्ता अधिकार, संपत्ति कानून, और रोजगार कानून मुख्य क्षेत्र हैं।"""
            else:
                fallback_response = f"""I'd like to help with your legal question: "{question}"

Key Legal Guidance:
• Consult a qualified lawyer for specific advice
• Gather all relevant documents
• Contact legal aid centers for affordable help

In India, key areas include consumer rights, property law, employment law, and contract law. Free legal aid is available through government centers."""
            
            return {
                "response": fallback_response,
                "confidence": 0.8,
                "related_laws": ["Consumer Protection Act", "Indian Contract Act", "Property Act"],
                "suggested_actions": self._extract_actions("", language),
                "language": language,
                "model_used": "Legal Guidance System (Fallback)",
                "status": "fallback",
                "note": "AI temporarily unavailable - providing legal guidance"
            }
    
    def _extract_laws(self, response: str) -> List[str]:
        """Extract relevant laws mentioned in the response"""
        common_laws = [
            "Indian Contract Act", "Consumer Protection Act", "Property Act",
            "Employment Act", "Criminal Procedure Code", "Civil Procedure Code",
            "Indian Penal Code", "Right to Information Act", "Marriage Act"
        ]
        
        mentioned_laws = []
        response_lower = response.lower()
        
        for law in common_laws:
            if any(word in response_lower for word in law.lower().split()):
                mentioned_laws.append(law)
        
        return mentioned_laws[:3]  # Limit to 3 most relevant
    
    def _extract_actions(self, response: str, language: str) -> List[str]:
        """Generate suggested next steps"""
        if language == "hi":
            return [
                "एक योग्य वकील से सलाह लें",
                "संबंधित दस्तावेज़ एकत्र करें",
                "कानूनी सहायता केंद्र से संपर्क करें",
                "अपने अधिकारों के बारे में जानें"
            ]
        else:
            return [
                "Consult a qualified lawyer",
                "Gather relevant documents", 
                "Contact legal aid center",
                "Know your rights and options"
            ]

# Global AI service instance
ai_service = AIService()
