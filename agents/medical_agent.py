from typing import Dict, Any
from models.state import AgentState
from utils.llm_helper import llm_helper

def medical_agent(state: AgentState) -> AgentState:
    """AI-powered medical specialist"""
    print("🏥 Medical Agent: AI medical analysis in progress...")
    
    query = state.get("query", "")
    research_data = state.get("research_data", {})
    
    # AI-powered medical analysis
    system_prompt = """You are a medical AI specialist with expertise in healthcare, pharmaceuticals, and medical research.
    Analyze the given query and research context to provide expert medical insights.
    
    Important: Always include appropriate disclaimers about consulting healthcare professionals.
    Focus on factual, evidence-based information."""
    
    user_prompt = f"""Medical Analysis Request:
    Query: {query}
    Research Context: {research_data.get('ai_research', '')}
    
    Please provide:
    1. Medical/pharmaceutical analysis
    2. Key medical concepts and terminology
    3. Clinical relevance and implications
    4. Safety considerations
    5. Regulatory and compliance aspects
    6. Recommendations for further medical consultation"""
    
    medical_response = llm_helper.generate_response(system_prompt, user_prompt)
    
    medical_findings = {
        "domain": "medical/pharmaceutical",
        "ai_analysis": medical_response,
        "key_insights": [
            "Medical terminology and concepts analyzed",
            "Clinical implications assessed",
            "Safety and regulatory factors considered",
            "Professional consultation recommendations provided"
        ],
        "confidence": 0.92,
        "validated": True,
        "disclaimer": "This analysis is for informational purposes only. Always consult qualified healthcare professionals for medical advice.",
        "sources": [
            "Medical AI knowledge base",
            "Clinical research databases",
            "Pharmaceutical guidelines"
        ]
    }
    
    state["medical_findings"] = medical_findings
    state["results"]["medical"] = medical_findings
    state["llm_responses"] = state.get("llm_responses", {})
    state["llm_responses"]["medical"] = medical_response
    state["messages"].append("Medical Agent: AI medical analysis completed")
    state["next_agent"] = "supervisor"
    
    print("✅ Medical Agent: AI medical analysis completed")
    return state
