from typing import Dict, Any
from models.state import AgentState
from utils.llm_helper import llm_helper

def repair_agent(state: AgentState) -> AgentState:
    """AI-powered repair and quality assurance agent"""
    print("🔧 Repair Agent: AI-powered quality assessment in progress...")
    
    query = state.get("query", "")
    results = state.get("results", {})
    llm_responses = state.get("llm_responses", {})
    
    # AI-powered quality assessment
    system_prompt = """You are an AI quality assurance specialist. Analyze the current workflow state and results to identify:
    1. Potential errors or inconsistencies
    2. Missing information or gaps
    3. Quality issues in the analysis
    4. Recommendations for improvements
    5. Overall confidence assessment
    
    Provide specific, actionable feedback for each identified issue."""
    
    # Prepare context for AI analysis
    analysis_context = {
        "query": query,
        "completed_analyses": list(results.keys()),
        "total_responses": len(llm_responses),
        "workflow_stage": f"Iteration {state.get('iteration_count', 0)}"
    }
    
    # Include sample of results for quality check
    quality_check_data = {}
    for key, value in results.items():
        if isinstance(value, dict):
            quality_check_data[key] = {
                "status": value.get("status", "unknown"),
                "confidence": value.get("confidence", 0),
                "key_metrics": list(value.keys())[:5]  # First 5 keys for overview
            }
    
    user_prompt = f"""Quality Assessment Request:
    
    Workflow Context: {analysis_context}
    Results Overview: {quality_check_data}
    
    Please assess:
    1. Are there any logical inconsistencies?
    2. Is the analysis complete for the given query?
    3. Are confidence scores reasonable?
    4. What improvements could be made?
    5. Overall quality rating (1-10)"""
    
    repair_response = llm_helper.generate_response(system_prompt, user_prompt)
    
    # Analyze for specific repair actions
    repair_actions = []
    quality_issues = []
    
    # Check confidence scores
    for key, value in results.items():
        if isinstance(value, dict) and "confidence" in value:
            confidence = value["confidence"]
            if confidence < 0.7:
                repair_actions.append(f"Low confidence in {key} analysis ({confidence:.2f}) - recommend review")
                quality_issues.append(f"{key}_low_confidence")
    
    # Check for missing critical analyses
    query_lower = query.lower()
    if "medical" in query_lower and "medical" not in results:
        repair_actions.append("Medical query detected but no medical analysis found")
        quality_issues.append("missing_medical_analysis")
    
    if "financial" in query_lower and "financial" not in results:
        repair_actions.append("Financial query detected but no financial analysis found")
        quality_issues.append("missing_financial_analysis")
    
    # Check for incomplete workflow
    expected_stages = ["research"]
    if state.get("iteration_count", 0) > 5 and not results.get("summary"):
        repair_actions.append("Workflow progressed significantly but no summary generated")
        quality_issues.append("missing_summary")
    
    # Determine overall status
    if len(repair_actions) == 0:
        status = "all_systems_normal"
        overall_assessment = "All quality checks passed successfully"
    elif len(repair_actions) <= 2:
        status = "minor_issues_detected"
        overall_assessment = "Minor issues detected, workflow can continue"
    else:
        status = "significant_issues_found"
        overall_assessment = "Significant issues require attention"
    
    repair_status = {
        "ai_quality_assessment": repair_response,
        "issues_found": len(repair_actions),
        "quality_issues": quality_issues,
        "repair_actions": repair_actions,
        "status": status,
        "overall_assessment": overall_assessment,
        "recommendations": [
            "Continue monitoring workflow quality",
            "Validate high-confidence results",
            "Review any flagged inconsistencies"
        ] if status == "all_systems_normal" else repair_actions,
        "quality_score": max(1, 10 - len(repair_actions) * 2),  # Simple scoring
        "timestamp": state.get("iteration_count", 0)
    }
    
    # Update state
    state["repair_status"] = repair_status
    state["results"]["repair"] = repair_status
    state["llm_responses"] = state.get("llm_responses", {})
    state["llm_responses"]["repair"] = repair_response
    state["messages"].append(f"Repair Agent: {overall_assessment}")
    state["next_agent"] = "supervisor"
    
    print(f"✅ Repair Agent: {status} - Quality score: {repair_status['quality_score']}/10")
    return state

def validate_workflow_integrity(state: AgentState) -> Dict[str, Any]:
    """Additional validation function for workflow integrity"""
    
    validation_results = {
        "state_consistency": True,
        "required_fields_present": True,
        "data_integrity": True,
        "issues": []
    }
    
    # Check required state fields
    required_fields = ["query", "results", "iteration_count", "workflow_complete"]
    for field in required_fields:
        if field not in state:
            validation_results["required_fields_present"] = False
            validation_results["issues"].append(f"Missing required field: {field}")
    
    # Check data consistency
    if state.get("iteration_count", 0) < 0:
        validation_results["state_consistency"] = False
        validation_results["issues"].append("Invalid iteration count")
    
    if state.get("max_iterations", 10) <= state.get("iteration_count", 0):
        validation_results["issues"].append("Approaching maximum iterations")
    
    return validation_results
