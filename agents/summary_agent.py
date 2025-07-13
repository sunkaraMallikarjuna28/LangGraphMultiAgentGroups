from typing import Dict, Any
from models.state import AgentState
from utils.llm_helper import llm_helper

def summary_agent(state: AgentState) -> AgentState:
    """AI-powered summary and synthesis agent"""
    print("📊 Summary Agent: AI-powered synthesis in progress...")
    
    query = state.get("query", "")
    results = state.get("results", {})
    llm_responses = state.get("llm_responses", {})
    
    # Compile all AI responses for synthesis
    all_analyses = []
    for agent, response in llm_responses.items():
        all_analyses.append(f"{agent.upper()} ANALYSIS:\n{response}\n")
    
    # AI-powered comprehensive summary
    system_prompt = """You are an expert synthesis analyst. Create a comprehensive, well-structured summary 
    that integrates all the specialist analyses into a coherent, actionable report.
    
    Structure your summary with:
    1. Executive Summary
    2. Key Findings by Domain
    3. Cross-Domain Insights
    4. Recommendations
    5. Conclusion
    
    Make it professional, clear, and actionable."""
    
    user_prompt = f"""Create a comprehensive summary for the query: "{query}"
    
    Specialist Analyses to Synthesize:
    {chr(10).join(all_analyses)}
    
    Additional Context:
    - Total agents involved: {len(results)}
    - Query complexity: {state.get('query_analysis', {}).get('complexity', 'medium')}
    - Domain focus: {state.get('query_analysis', {}).get('domain', 'general')}"""
    
    comprehensive_summary = llm_helper.generate_response(system_prompt, user_prompt)
    
    state["summary"] = comprehensive_summary
    state["results"]["summary"] = {
        "ai_summary": comprehensive_summary,
        "synthesis_complete": True,
        "agents_synthesized": list(llm_responses.keys())
    }
    state["llm_responses"]["summary"] = comprehensive_summary
    state["messages"].append("Summary Agent: AI-powered synthesis completed")
    state["next_agent"] = "supervisor"
    
    print("✅ Summary Agent: AI synthesis completed")
    return state
