from typing import Dict, Any, List
from models.state import AgentState
from utils.llm_helper import llm_helper
import json
from datetime import datetime
import os

def document_agent(state: AgentState) -> AgentState:
    """AI-powered document processing and organization agent"""
    print("📄 Document Agent: AI-powered document processing in progress...")
    
    query = state.get("query", "")
    results = state.get("results", {})
    summary = state.get("summary", "")
    llm_responses = state.get("llm_responses", {})
    
    # AI-powered document structuring
    system_prompt = """You are an expert document architect and technical writer. 
    Create a comprehensive document structure and organization plan for the multi-agent analysis results.
    
    Your task is to:
    1. Analyze all the results and create a logical document hierarchy
    2. Suggest appropriate document types and formats
    3. Recommend content organization strategies
    4. Provide executive summary recommendations
    5. Suggest visualization and presentation formats
    
    Focus on creating professional, well-structured documentation that would be suitable for business or research purposes."""
    
    # Prepare context for AI document planning
    document_context = {
        "query": query,
        "total_analyses": len(results),
        "available_sections": list(results.keys()),
        "has_summary": bool(summary),
        "analysis_depth": "comprehensive" if len(llm_responses) > 3 else "basic"
    }
    
    user_prompt = f"""Document Organization Request:
    
    Analysis Context: {document_context}
    
    Available Content Sections:
    {json.dumps(list(results.keys()), indent=2)}
    
    Please provide:
    1. Recommended document structure and hierarchy
    2. Content organization strategy
    3. Executive summary approach
    4. Key sections to highlight
    5. Professional formatting recommendations"""
    
    document_planning_response = llm_helper.generate_response(system_prompt, user_prompt)
    
    # Create structured documents using AI guidance
    documents = []
    
    # 1. Executive Summary Document
    executive_summary = create_executive_summary(query, results, summary, llm_responses)
    documents.append(executive_summary)
    
    # 2. Comprehensive Analysis Report
    main_report = create_main_report(query, results, summary, llm_responses, document_planning_response)
    documents.append(main_report)
    
    # 3. Individual Specialist Reports
    for specialist, data in results.items():
        if specialist not in ["summary", "documents", "repair"]:
            specialist_doc = create_specialist_report(specialist, data, llm_responses.get(specialist, ""))
            documents.append(specialist_doc)
    
    # 4. Technical Data Export
    technical_export = create_technical_export(state)
    documents.append(technical_export)
    
    # 5. Quality Assurance Report
    if "repair" in results:
        qa_report = create_qa_report(results["repair"])
        documents.append(qa_report)
    
    # 6. Methodology and Process Documentation
    methodology_doc = create_methodology_document(state)
    documents.append(methodology_doc)
    
    # AI-powered document metadata generation
    metadata_prompt = f"""Generate comprehensive metadata for this document collection:
    Query: {query}
    Total Documents: {len(documents)}
    Document Types: {[doc['type'] for doc in documents]}
    
    Provide JSON metadata including tags, categories, and search keywords."""
    
    metadata_response = llm_helper.generate_response(
        "You are a metadata specialist. Generate comprehensive document metadata in JSON format.",
        metadata_prompt
    )
    
    # Update state with document results
    document_summary = {
        "ai_document_planning": document_planning_response,
        "ai_metadata": metadata_response,
        "total_documents": len(documents),
        "document_types": [doc["type"] for doc in documents],
        "processing_status": "completed",
        "organization_strategy": "ai_optimized_hierarchy",
        "export_formats": ["json", "markdown", "structured_text"],
        "timestamp": datetime.now().isoformat()
    }
    
    state["documents"] = documents
    state["results"]["documents"] = document_summary
    state["llm_responses"] = state.get("llm_responses", {})
    state["llm_responses"]["documents"] = document_planning_response
    state["messages"].append(f"Document Agent: {len(documents)} AI-structured documents created")
    state["workflow_complete"] = True
    state["next_agent"] = None
    
    # Save documents to files
    save_documents_to_files(documents, query)
    
    print(f"✅ Document Agent: {len(documents)} professional documents generated and saved")
    return state

def create_executive_summary(query: str, results: Dict[str, Any], summary: str, llm_responses: Dict[str, str]) -> Dict[str, Any]:
    """Create executive summary document"""
    
    # AI-generated executive summary
    system_prompt = """You are an executive summary specialist. Create a concise, high-level executive summary 
    that captures the key insights, findings, and recommendations from the multi-agent analysis.
    
    Format it for C-level executives and decision-makers. Focus on actionable insights and strategic implications."""
    
    user_prompt = f"""Create an executive summary for:
    Query: {query}
    
    Key Results Available: {list(results.keys())}
    Comprehensive Summary: {summary[:500]}...
    
    Include:
    1. Key findings (3-5 bullet points)
    2. Strategic implications
    3. Recommended actions
    4. Risk considerations
    5. Next steps"""
    
    executive_content = llm_helper.generate_response(system_prompt, user_prompt)
    
    return {
        "type": "executive_summary",
        "title": f"Executive Summary: {query}",
        "content": executive_content,
        "priority": "high",
        "audience": "executives",
        "timestamp": datetime.now().isoformat(),
        "metadata": {
            "query": query,
            "analysis_scope": "multi_agent_comprehensive",
            "confidence_level": "high"
        }
    }

def create_main_report(query: str, results: Dict[str, Any], summary: str, llm_responses: Dict[str, str], planning_guidance: str) -> Dict[str, Any]:
    """Create comprehensive main analysis report"""
    
    # Structure main report content
    report_sections = []
    
    # Introduction
    report_sections.append(f"# Comprehensive Multi-Agent Analysis Report\n\n**Query:** {query}\n**Analysis Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n**Analysis Type:** AI-Powered Multi-Agent System\n\n")
    
    # Executive Summary
    if summary:
        report_sections.append(f"## Executive Summary\n\n{summary}\n\n")
    
    # Detailed Findings by Agent
    report_sections.append("## Detailed Analysis by Specialist\n\n")
    
    for agent, response in llm_responses.items():
        if agent != "documents":
            agent_title = agent.replace("_", " ").title()
            report_sections.append(f"### {agent_title} Analysis\n\n{response}\n\n")
    
    # Synthesis and Conclusions
    report_sections.append("## Synthesis and Conclusions\n\n")
    report_sections.append("This analysis was conducted using a coordinated multi-agent system, with each specialist contributing domain expertise to provide comprehensive insights.\n\n")
    
    # Methodology
    report_sections.append("## Methodology\n\n")
    report_sections.append("- **Research Agent:** Conducted initial analysis and information gathering\n")
    report_sections.append("- **Specialist Agents:** Provided domain-specific expertise (medical, financial, etc.)\n")
    report_sections.append("- **Quality Assurance:** Validated findings and identified potential issues\n")
    report_sections.append("- **Synthesis Agent:** Integrated all findings into coherent insights\n")
    report_sections.append("- **Documentation Agent:** Structured and organized final deliverables\n\n")
    
    full_content = "".join(report_sections)
    
    return {
        "type": "main_report",
        "title": f"Comprehensive Analysis: {query}",
        "content": full_content,
        "format": "markdown",
        "sections": len([s for s in report_sections if s.startswith("#")]),
        "word_count": len(full_content.split()),
        "timestamp": datetime.now().isoformat(),
        "metadata": {
            "query": query,
            "agents_involved": list(llm_responses.keys()),
            "analysis_depth": "comprehensive"
        }
    }

def create_specialist_report(specialist: str, data: Dict[str, Any], llm_response: str) -> Dict[str, Any]:
    """Create individual specialist team report"""
    
    specialist_title = specialist.replace("_", " ").title()
    
    content_sections = []
    content_sections.append(f"# {specialist_title} Specialist Report\n\n")
    content_sections.append(f"**Specialist Domain:** {specialist_title}\n")
    content_sections.append(f"**Analysis Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
    
    # AI Analysis
    if llm_response:
        content_sections.append("## AI-Powered Analysis\n\n")
        content_sections.append(f"{llm_response}\n\n")
    
    # Technical Details
    content_sections.append("## Technical Details\n\n")
    if isinstance(data, dict):
        for key, value in data.items():
            if key not in ["ai_analysis", "timestamp"]:
                content_sections.append(f"**{key.replace('_', ' ').title()}:** {value}\n\n")
    
    # Confidence and Validation
    confidence = data.get("confidence", 0) if isinstance(data, dict) else 0
    content_sections.append(f"## Quality Metrics\n\n")
    content_sections.append(f"- **Confidence Level:** {confidence:.1%}\n")
    content_sections.append(f"- **Analysis Status:** {data.get('status', 'completed') if isinstance(data, dict) else 'completed'}\n")
    content_sections.append(f"- **Validation:** {'Passed' if confidence > 0.8 else 'Requires Review'}\n\n")
    
    full_content = "".join(content_sections)
    
    return {
        "type": f"{specialist}_specialist_report",
        "title": f"{specialist_title} Analysis Report",
        "content": full_content,
        "format": "markdown",
        "specialist": specialist,
        "confidence": confidence,
        "timestamp": datetime.now().isoformat(),
        "metadata": {
            "domain": specialist,
            "analysis_type": "ai_powered",
            "validation_status": "passed" if confidence > 0.8 else "review_required"
        }
    }

def create_technical_export(state: AgentState) -> Dict[str, Any]:
    """Create technical data export document"""
    
    # Clean state for export (remove circular references)
    export_state = {}
    for key, value in state.items():
        if key not in ["llm_responses"]:  # Exclude large text responses
            export_state[key] = value
    
    return {
        "type": "technical_export",
        "title": "Technical Data Export",
        "content": json.dumps(export_state, indent=2, default=str),
        "format": "json",
        "size_kb": len(json.dumps(export_state, default=str)) / 1024,
        "timestamp": datetime.now().isoformat(),
        "metadata": {
            "export_type": "full_state",
            "format": "json",
            "purpose": "technical_analysis"
        }
    }

def create_qa_report(repair_data: Dict[str, Any]) -> Dict[str, Any]:
    """Create quality assurance report"""
    
    qa_content = []
    qa_content.append("# Quality Assurance Report\n\n")
    qa_content.append(f"**Assessment Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
    
    # Overall Assessment
    qa_content.append("## Overall Assessment\n\n")
    qa_content.append(f"**Status:** {repair_data.get('status', 'unknown')}\n")
    qa_content.append(f"**Quality Score:** {repair_data.get('quality_score', 0)}/10\n")
    qa_content.append(f"**Issues Found:** {repair_data.get('issues_found', 0)}\n\n")
    
    # Detailed Findings
    if repair_data.get("repair_actions"):
        qa_content.append("## Issues and Recommendations\n\n")
        for i, action in enumerate(repair_data["repair_actions"], 1):
            qa_content.append(f"{i}. {action}\n")
        qa_content.append("\n")
    
    # AI Assessment
    if repair_data.get("ai_quality_assessment"):
        qa_content.append("## AI Quality Assessment\n\n")
        qa_content.append(f"{repair_data['ai_quality_assessment']}\n\n")
    
    full_content = "".join(qa_content)
    
    return {
        "type": "quality_assurance_report",
        "title": "Quality Assurance and Validation Report",
        "content": full_content,
        "format": "markdown",
        "quality_score": repair_data.get("quality_score", 0),
        "issues_count": repair_data.get("issues_found", 0),
        "timestamp": datetime.now().isoformat(),
        "metadata": {
            "assessment_type": "ai_powered_qa",
            "validation_status": repair_data.get("status", "unknown")
        }
    }

def create_methodology_document(state: AgentState) -> Dict[str, Any]:
    """Create methodology and process documentation"""
    
    methodology_content = []
    methodology_content.append("# Multi-Agent Analysis Methodology\n\n")
    methodology_content.append("## System Architecture\n\n")
    methodology_content.append("This analysis was conducted using an AI-powered multi-agent system with the following components:\n\n")
    
    # Agent descriptions
    agents_info = {
        "supervisor": "Central coordinator managing workflow and routing decisions",
        "research": "Primary research and initial analysis",
        "medical": "Medical and pharmaceutical domain expertise",
        "financial": "Financial analysis and market insights",
        "repair": "Quality assurance and error detection",
        "summary": "Synthesis and comprehensive reporting",
        "documents": "Document structuring and organization"
    }
    
    for agent, description in agents_info.items():
        methodology_content.append(f"- **{agent.title()} Agent:** {description}\n")
    
    methodology_content.append("\n## Process Flow\n\n")
    methodology_content.append("1. **Initialization:** Query analysis and routing strategy\n")
    methodology_content.append("2. **Research Phase:** Initial information gathering and analysis\n")
    methodology_content.append("3. **Specialist Analysis:** Domain-specific deep analysis\n")
    methodology_content.append("4. **Quality Assurance:** Validation and error checking\n")
    methodology_content.append("5. **Synthesis:** Integration of all findings\n")
    methodology_content.append("6. **Documentation:** Professional report generation\n\n")
    
    methodology_content.append("## AI Integration\n\n")
    methodology_content.append("- **Language Model:** OpenAI GPT-4\n")
    methodology_content.append("- **Decision Making:** AI-powered routing and analysis\n")
    methodology_content.append("- **Quality Control:** Automated validation and consistency checking\n")
    methodology_content.append("- **Synthesis:** Intelligent integration of multi-domain insights\n\n")
    
    # Execution statistics
    methodology_content.append("## Execution Statistics\n\n")
    methodology_content.append(f"- **Total Iterations:** {state.get('iteration_count', 0)}\n")
    methodology_content.append(f"- **Agents Activated:** {len(state.get('results', {}))}\n")
    methodology_content.append(f"- **Processing Time:** Real-time analysis\n")
    methodology_content.append(f"- **Quality Score:** {state.get('repair_status', {}).get('quality_score', 'N/A')}/10\n\n")
    
    full_content = "".join(methodology_content)
    
    return {
        "type": "methodology_document",
        "title": "Analysis Methodology and Process Documentation",
        "content": full_content,
        "format": "markdown",
        "timestamp": datetime.now().isoformat(),
        "metadata": {
            "system_type": "multi_agent_ai",
            "methodology": "comprehensive_analysis",
            "ai_model": "gpt-4"
        }
    }

def save_documents_to_files(documents: List[Dict[str, Any]], query: str):
    """Save generated documents to files"""
    
    # Create output directory
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir = f"analysis_output_{timestamp}"
    os.makedirs(output_dir, exist_ok=True)
    
    # Save each document
    for i, doc in enumerate(documents):
        doc_type = doc.get("type", f"document_{i}")
        filename = f"{doc_type}_{timestamp}"
        
        # Determine file extension
        if doc.get("format") == "json":
            filename += ".json"
        elif doc.get("format") == "markdown":
            filename += ".md"
        else:
            filename += ".txt"
        
        filepath = os.path.join(output_dir, filename)
        
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(doc["content"])
            print(f"📄 Saved: {filepath}")
        except Exception as e:
            print(f"❌ Error saving {filepath}: {e}")
    
    # Create index file
    index_content = f"# Analysis Output Index\n\n**Query:** {query}\n**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n## Documents:\n\n"
    
    for doc in documents:
        index_content += f"- **{doc['title']}** ({doc['type']})\n"
    
    index_path = os.path.join(output_dir, "index.md")
    with open(index_path, 'w', encoding='utf-8') as f:
        f.write(index_content)
    
    print(f"📁 All documents saved to: {output_dir}/")
