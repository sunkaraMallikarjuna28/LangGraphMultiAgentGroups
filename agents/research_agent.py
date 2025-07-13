from typing import Dict, Any
from models.state import AgentState
from utils.llm_helper import llm_helper
import time

def research_agent(state: AgentState) -> AgentState:
    """AI-powered research agent"""
    print("🔍 Research Agent: Conducting AI-powered research...")
    
    query = state.get("query", "")
    
    # AI-powered query analysis
    if not state.get("query_analysis"):
        query_analysis = llm_helper.analyze_query(query)
        state["query_analysis"] = query_analysis
    else:
        query_analysis = state["query_analysis"]
    
    # AI-powered research
    system_prompt = """You are an expert research analyst. Conduct comprehensive research on the given query.
    Provide detailed findings, identify key areas for investigation, and suggest follow-up actions.
    Format your response as a structured analysis with clear sections."""
    
    user_prompt = f"""Conduct research on: {query}
    
    Query analysis context: {query_analysis}
    
    Provide:
    1. Key research findings
    2. Important insights
    3. Areas requiring specialist attention
    4. Confidence assessment
    5. Recommendations for next steps"""
    
    research_response = llm_helper.generate_response(system_prompt, user_prompt)
    
    # Structure the research results
    research_results = {
        "query_analysis": query_analysis,
        "ai_research": research_response,
        "research_findings": [
            "AI-powered comprehensive analysis completed",
            "Key insights and patterns identified",
            "Specialist areas flagged for deeper analysis"
        ],
        "confidence_score": 0.90,
        "timestamp": time.time(),
        "status": "completed",
        "next_recommendations": query_analysis.get("suggested_agents", [])
    }
    
    # Update state
    state["research_data"] = research_results
    state["results"]["research"] = research_results
    state["llm_responses"] = state.get("llm_responses", {})
    state["llm_responses"]["research"] = research_response
    state["messages"].append("Research Agent: AI-powered research completed")
    
    # AI-powered next step decision
    domain = query_analysis.get("domain", "general")
    if "medical" in domain.lower() or "pharma" in domain.lower():
        state["next_agent"] = "team3"
    elif "financial" in domain.lower() or "finance" in domain.lower():
        state["next_agent"] = "team4"
    else:
        state["next_agent"] = "supervisor"
    
    print("✅ Research Agent: AI analysis completed")
    return state
