from typing import TypedDict, List, Dict, Any, Optional
from datetime import datetime

class AgentState(TypedDict):
    messages: List[str]
    current_task: str
    query: str
    query_analysis: Dict[str, Any]
    results: Dict[str, Any]
    next_agent: Optional[str]
    workflow_complete: bool
    handoff_context: Dict[str, Any]
    research_data: Dict[str, Any]
    medical_findings: Dict[str, Any]
    financial_data: Dict[str, Any]
    repair_status: Dict[str, Any]
    summary: str
    documents: List[Dict[str, Any]]
    iteration_count: int
    max_iterations: int
    llm_responses: Dict[str, str]
    confidence_scores: Dict[str, float]
