from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage
from config.settings import settings
from typing import List, Dict, Any
import json

class LLMHelper:
    def __init__(self):
        settings.validate()
        self.llm = ChatOpenAI(
            api_key=settings.OPENAI_API_KEY,
            model=settings.OPENAI_MODEL,
            temperature=settings.TEMPERATURE,
            max_tokens=settings.MAX_TOKENS
        )
    
    def generate_response(self, system_prompt: str, user_prompt: str) -> str:
        """Generate a response using OpenAI"""
        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=user_prompt)
        ]
        
        response = self.llm.invoke(messages)
        return response.content
    
    def analyze_query(self, query: str) -> Dict[str, Any]:
        """Analyze query intent and characteristics"""
        system_prompt = """You are an expert query analyzer. Analyze the given query and return a JSON response with:
        - intent: the main purpose (research, analysis, question, etc.)
        - domain: the subject area (medical, financial, technical, general, etc.)
        - complexity: low, medium, or high
        - keywords: list of important keywords
        - suggested_agents: list of agent types that should handle this query
        - estimated_time: rough estimate in minutes"""
        
        user_prompt = f"Analyze this query: {query}"
        
        response = self.generate_response(system_prompt, user_prompt)
        try:
            return json.loads(response)
        except:
            return {
                "intent": "general_inquiry",
                "domain": "general",
                "complexity": "medium",
                "keywords": query.split(),
                "suggested_agents": ["research", "summary"],
                "estimated_time": "5-10"
            }
    
    def make_routing_decision(self, state: Dict[str, Any]) -> str:
        """Help supervisor make routing decisions"""
        system_prompt = """You are a supervisor agent coordinator. Based on the current state, decide which agent should handle the next task.
        Available agents: team1 (research), team2 (repair), team3 (medical), team4 (financial), team5 (summary), team6 (document)
        Return only the agent name (e.g., 'team1') or 'END' if workflow is complete."""
        
        user_prompt = f"Current state: {json.dumps(state, default=str)}"
        
        response = self.generate_response(system_prompt, user_prompt)
        return response.strip().lower()

# Global LLM helper instance
llm_helper = LLMHelper()
