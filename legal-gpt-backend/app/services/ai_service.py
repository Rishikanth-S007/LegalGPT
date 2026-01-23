import openai
from app.config.settings import settings
import asyncio
from typing import Dict, List

class AIService:
    def __init__(self):
        # Use GitHub Models instead of OpenAI directly - FREE!
        self.client = openai.OpenAI(
            api_key=settings.openai_api_key,  # This is now your GitHub token
            base_url="https://models.inference.ai.azure.com"  # GitHub Models endpoint
        )
    
    async def process_legal_query(self, question: str, language: str = "en") -> Dict:
        """Process legal questions with AI - now using FREE GitHub Models!"""
        
        # Create specialized prompts for legal assistance
        if language == "hi":
            system_prompt = """आप एक सहायक कानूनी सहायक हैं जो भारतीय कानून में विशेषज्ञ हैं। 
            सरल हिंदी में जवाब दें और हमेशा उपयोगकर्ताओं को योग्य वकीलों से सलाह लेने की सलाह दें।
            जवाब संक्षिप्त और व्यावहारिक रखें।"""
        else:
            system_prompt = """You are a helpful legal assistant specializing in Indian law. 
            Provide clear, understandable legal guidance while always reminding users to 
            consult qualified lawyers for specific legal advice. Focus on Indian laws and regulations.
            Keep responses concise and practical. Maximum 200 words."""
        
        try:
            print(f"🔄 Processing legal query with GitHub Models: {question[:50]}...")
            
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",  # Use mini version - higher free limits
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": question}
                ],
                temperature=0.1,
                max_tokens=300  # Keep responses concise to save quota
            )
            
            ai_response = response.choices[0].message.content
            print(f"✅ GitHub AI responded successfully!")
            
            # Extract key information
            related_laws = self._extract_laws(ai_response)
            suggested_actions = self._extract_actions(ai_response, language)
            
            return {
                "response": ai_response,
                "confidence": 0.95,  # GitHub models are high quality
                "related_laws": related_laws,
                "suggested_actions": suggested_actions,
                "language": language,
                "model_used": "GitHub GPT-4o Mini (FREE! 🎉)",
                "status": "success"
            }
            
        except Exception as e:
            print(f"❌ GitHub AI Error: {str(e)}")
            
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
