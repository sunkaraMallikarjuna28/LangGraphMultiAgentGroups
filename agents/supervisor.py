from typing import Dict, Any
from models.state import AgentState
from utils.llm_helper import llm_helper

def supervisor_agent(state: AgentState) -> AgentState:
    """AI-powered supervisor coordinating all teams"""
    print("👑 Supervisor: Analyzing current state with AI...")
    
    iteration_count = state.get("iteration_count", 0)
    max_iterations = state.get("max_iterations", 10)
    results = state.get("results", {})
    
    # Increment iteration counter
    state["iteration_count"] = iteration_count + 1
    
    # Check completion conditions
    if state.get("workflow_complete", False):
        print("👑 Supervisor: Workflow marked as complete")
        state["next_agent"] = None
        return state
    
    if iteration_count >= max_iterations:
        print("👑 Supervisor: Maximum iterations reached")
        state["workflow_complete"] = True
        state["next_agent"] = None
        return state
    
    # Use AI to make routing decision
    routing_context = {
        "query": state.get("query", ""),
        "completed_tasks": list(results.keys()),
        "iteration": iteration_count,
        "query_analysis": state.get("query_analysis", {})
    }
    
    # AI-powered routing decision
    system_prompt = """You are an intelligent supervisor managing a multi-agent workflow. 
    Based on the current state, decide the next agent to route to:
    
    Available agents:
    - team1: Research and initial analysis
    - team2: Repair and quality assurance  
    - team3: Medical/pharmaceutical specialist
    - team4: Financial analysis specialist
    - team5: Summary and synthesis
    - team6: Document processing and organization
    
    Rules:
    1. Start with team1 (research) if no research is done
    2. Route to team3 for medical queries, team4 for financial queries
    3. Use team2 for quality checks and repairs
    4. Use team5 for summarization after main analysis
    5. Use team6 for final document processing
    6. Return 'END' when all necessary tasks are complete
    
    Return only the team name or 'END'."""
    
    user_prompt = f"Current workflow state: {routing_context}"
    
    next_agent = llm_helper.generate_response(system_prompt, user_prompt).strip().lower()
    
    # Validate and clean the response
    valid_agents = ["team1", "team2", "team3", "team4", "team5", "team6", "end"]
    if next_agent not in valid_agents:
        # Fallback logic
        if not results.get("research"):
            next_agent = "team1"
        elif not results.get("summary"):
            next_agent = "team5"
        else:
            next_agent = "end"
    
    if next_agent == "end":
        state["workflow_complete"] = True
        state["next_agent"] = None
    else:
        state["next_agent"] = next_agent
    
    state["messages"].append(f"Supervisor: AI routing decision - {next_agent}")
    print(f"👑 Supervisor: AI routing decision - {next_agent}")
    
    return state
