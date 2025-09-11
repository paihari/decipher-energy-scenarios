"""
Language Translator Agent for Swiss Energy Scenarios Decipher System

This agent handles translation between English, German, French, and Italian
to enable multilingual query processing and response generation.
"""

import asyncio
from typing import Dict, Any, Optional, List
from .base_agent import BaseAgent, AgentResponse

class LanguageTranslatorAgent(BaseAgent):
    def __init__(self, openai_api_key: str):
        super().__init__(
            name="LanguageTranslator",
            description="Translates text between English, German, French, and Italian for multilingual support",
            openai_api_key=openai_api_key,
            model="gpt-4",
            temperature=0.1,  # Low temperature for accurate translations
            max_tokens=3000
        )
        
        self.supported_languages = {
            "en": "English",
            "de": "German (Deutsch)", 
            "fr": "French (Français)",
            "it": "Italian (Italiano)"
        }
    
    def _build_system_prompt(self) -> str:
        return """You are a professional translator specializing in Swiss energy and climate policy terminology. 
        
Your role is to provide accurate translations between English, German, French, and Italian, with particular expertise in:
- Energy transition terminology
- Climate policy vocabulary  
- Technical energy sector terms
- Swiss governmental and policy language
- Statistical and analytical terminology

IMPORTANT GUIDELINES:
1. Maintain technical accuracy and consistency
2. Preserve the original meaning and nuance
3. Use appropriate formal/technical register
4. Keep proper nouns, acronyms, and technical terms where appropriate
5. For energy scenarios, preserve terms like "ZERO", "WWB" as they are official scenario names
6. Maintain numerical values and units exactly
7. Provide only the translation without explanations unless specifically requested

You will receive requests in this format:
- "translate_to_{language_code}: {text}"
- "detect_language: {text}" 
- "translate_query: {text} | target_language: {language_code}"
- "translate_response: {text} | target_language: {language_code}"

Supported language codes: en (English), de (German), fr (French), it (Italian)"""

    async def process_query(self, query: str, context: Optional[Dict[str, Any]] = None) -> AgentResponse:
        """Process translation request."""
        try:
            messages = self._prepare_messages(query, context)
            response_text = await self._call_openai(messages)
            
            confidence = self._calculate_translation_confidence(query, response_text)
            
            return AgentResponse(
                content=response_text.strip(),
                confidence=confidence,
                data_sources=["OpenAI GPT-4 Translation Model"],
                reasoning=f"Translation processed using specialized multilingual model with Swiss energy terminology expertise"
            )
            
        except Exception as e:
            return AgentResponse(
                content=f"Translation error: {str(e)}",
                confidence=0.0,
                reasoning=f"Translation failed: {str(e)}"
            )
    
    async def detect_language(self, text: str) -> str:
        """Detect the language of the input text."""
        query = f"detect_language: {text}"
        response = await self.process_query(query)
        
        # Extract language code from response
        content = response.content.lower()
        for code, name in self.supported_languages.items():
            if code in content or name.lower() in content:
                return code
        
        return "en"  # Default to English if detection fails
    
    async def translate_to_english(self, text: str, source_language: str = None) -> str:
        """Translate any supported language to English."""
        if source_language:
            query = f"translate_to_en: {text} (from {self.supported_languages.get(source_language, source_language)})"
        else:
            query = f"translate_to_en: {text}"
        
        response = await self.process_query(query)
        return response.content
    
    async def translate_from_english(self, text: str, target_language: str) -> str:
        """Translate English to specified target language."""
        if target_language not in self.supported_languages:
            return text  # Return original if language not supported
        
        if target_language == "en":
            return text  # No translation needed
        
        target_name = self.supported_languages[target_language]
        query = f"translate_to_{target_language}: {text} (to {target_name})"
        
        response = await self.process_query(query)
        return response.content
    
    async def translate_query(self, query_text: str, target_language: str = "en") -> str:
        """Translate a user query, optimized for energy scenario questions."""
        query = f"translate_query: {query_text} | target_language: {target_language}"
        response = await self.process_query(query)
        return response.content
    
    async def translate_response(self, response_text: str, target_language: str = "en") -> str:
        """Translate an agent response, preserving technical terminology."""
        if target_language == "en":
            return response_text
            
        query = f"translate_response: {response_text} | target_language: {target_language}"
        response = await self.process_query(query)
        return response.content
    
    def _calculate_translation_confidence(self, query: str, response: str) -> float:
        """Calculate confidence level for translation quality."""
        base_confidence = 0.8
        
        # Higher confidence for shorter texts
        if len(query.split()) <= 10:
            base_confidence += 0.1
        
        # Lower confidence for very long texts
        if len(query.split()) > 100:
            base_confidence -= 0.1
        
        # Check for translation indicators in response
        if any(indicator in response.lower() for indicator in ["translation error", "unable to", "cannot translate"]):
            base_confidence = 0.2
        
        return max(0.0, min(1.0, base_confidence))
    
    def get_supported_languages(self) -> Dict[str, str]:
        """Return supported languages."""
        return self.supported_languages.copy()
    
    async def is_multilingual_query_needed(self, query: str, user_language: str) -> bool:
        """Determine if query needs translation for processing."""
        if user_language == "en":
            return False
        
        detected_language = await self.detect_language(query)
        return detected_language != "en"