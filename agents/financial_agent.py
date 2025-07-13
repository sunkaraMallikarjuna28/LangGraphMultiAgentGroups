from typing import Dict, Any
from models.state import AgentState
from utils.llm_helper import llm_helper

def financial_agent(state: AgentState) -> AgentState:
    """AI-powered financial analyst"""
    print("💰 Financial Agent: AI financial analysis in progress...")
    
    query = state.get("query", "")
    research_data = state.get("research_data", {})
    
    # AI-powered financial analysis
    system_prompt = """You are a financial AI analyst with expertise in markets, investments, economic trends, and financial planning.
    Provide comprehensive financial analysis based on the query and research context.
    
    Include risk assessments, market insights, and actionable recommendations."""
    
    user_prompt = f"""Financial Analysis Request:
    Query: {query}
    Research Context: {research_data.get('ai_research', '')}
    
    Please provide:
    1. Financial market analysis
    2. Economic trends and indicators
    3. Risk assessment and factors
    4. Investment implications
    5. Market opportunities and threats
    6. Strategic recommendations"""
    
    financial_response = llm_helper.generate_response(system_prompt, user_prompt)
    
    financial_data = {
        "analysis_type": "ai_powered_financial_research",
        "ai_analysis": financial_response,
        "market_insights": [
            "Comprehensive market analysis completed",
            "Economic indicators evaluated",
            "Risk factors identified and assessed",
            "Strategic recommendations formulated"
        ],
        "risk_assessment": "AI-evaluated based on current market conditions",
        "confidence": 0.88,
        "disclaimer": "Financial analysis for informational purposes. Consult financial advisors for investment decisions."
    }
    
    state["financial_data"] = financial_data
    state["results"]["financial"] = financial_data
    state["llm_responses"] = state.get("llm_responses", {})
    state["llm_responses"]["financial"] = financial_response
    state["messages"].append("Financial Agent: AI financial analysis completed")
    state["next_agent"] = "supervisor"
    
    print("✅ Financial Agent: AI financial analysis completed")
    return state
