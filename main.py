from langgraph.graph import StateGraph, END
from models.state import AgentState
from agents.supervisor import supervisor_agent
from agents.research_agent import research_agent
from agents.repair_agent import repair_agent
from agents.medical_agent import medical_agent
from agents.financial_agent import financial_agent
from agents.summary_agent import summary_agent
from agents.document_agent import document_agent
from config.settings import settings
import json
import os
from datetime import datetime

def create_ai_multi_agent_system():
    """Create AI-powered multi-agent system"""
    
    # Validate OpenAI configuration
    settings.validate()
    print(f"✅ OpenAI configured with model: {settings.OPENAI_MODEL}")
    
    # Initialize the graph
    workflow = StateGraph(AgentState)
    
    # Add all AI-powered agent nodes
    workflow.add_node("supervisor", supervisor_agent)
    workflow.add_node("team1", research_agent)
    workflow.add_node("team2", repair_agent)
    workflow.add_node("team3", medical_agent)
    workflow.add_node("team4", financial_agent)
    workflow.add_node("team5", summary_agent)
    workflow.add_node("team6", document_agent)
    
    # Define AI-powered routing
    def route_to_agent(state: AgentState):
        next_agent = state.get("next_agent")
        if state.get("workflow_complete", False) or next_agent is None:
            return END
        return next_agent
    
    # Add conditional edges
    workflow.add_conditional_edges(
        "supervisor",
        route_to_agent,
        {
            "team1": "team1",
            "team2": "team2", 
            "team3": "team3",
            "team4": "team4",
            "team5": "team5",
            "team6": "team6",
            END: END
        }
    )
    
    # All teams return to AI supervisor
    for team in ["team1", "team2", "team3", "team4", "team5", "team6"]:
        workflow.add_edge(team, "supervisor")
    
    workflow.set_entry_point("supervisor")
    
    return workflow.compile()

def run_ai_multi_agent_system(query: str):
    """Execute AI-powered multi-agent system"""
    
    print(f"\n🤖 Starting AI-Powered Multi-Agent System")
    print(f"🔑 Using OpenAI Model: {settings.OPENAI_MODEL}")
    print(f"📝 Query: {query}")
    print("=" * 70)
    
    app = create_ai_multi_agent_system()
    
    # Initialize state with AI capabilities
    initial_state = {
        "messages": [f"AI System initialized with query: {query}"],
        "current_task": "ai_initialization",
        "query": query,
        "query_analysis": {},
        "results": {},
        "next_agent": "supervisor",
        "workflow_complete": False,
        "handoff_context": {},
        "research_data": {},
        "medical_findings": {},
        "financial_data": {},
        "repair_status": {},
        "summary": "",
        "documents": [],
        "iteration_count": 0,
        "max_iterations": 15,
        "llm_responses": {},
        "confidence_scores": {}
    }
    
    try:
        final_state = app.invoke(initial_state)
        
        print("\n" + "=" * 70)
        print("🎉 AI Multi-Agent System Execution Complete!")
        print("=" * 70)
        
        # Display AI-generated summary
        if final_state.get("summary"):
            print("\n🤖 AI-GENERATED COMPREHENSIVE ANALYSIS:")
            print("-" * 50)
            print(final_state["summary"])
        
        print(f"\n📈 EXECUTION STATISTICS:")
        print(f"• AI Model Used: {settings.OPENAI_MODEL}")
        print(f"• Total iterations: {final_state.get('iteration_count', 0)}")
        print(f"• AI agents involved: {len(final_state.get('llm_responses', {}))}")
        print(f"• Documents generated: {len(final_state.get('documents', []))}")
        
        # Save AI results
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"ai_multi_agent_results_{timestamp}.json"
        
        with open(filename, 'w') as f:
            json.dump(final_state, f, indent=2, default=str)
        
        print(f"\n💾 AI Results saved to: {filename}")
        return final_state
        
    except Exception as e:
        print(f"❌ Error during AI execution: {str(e)}")
        return None

def get_user_query():
    """Interactive query input with validation and suggestions"""
    
    print("\n" + "="*60)
    print("🤖 AI MULTI-AGENT QUERY INPUT")
    print("="*60)
    
    # Provide query suggestions and examples
    print("\n💡 QUERY SUGGESTIONS:")
    print("─" * 30)
    
    suggestions = [
        "Research the latest developments in AI-powered medical diagnostics",
        "Analyze the financial impact of renewable energy adoption in 2024",
        "Investigate pharmaceutical drug development processes and regulations",
        "Study the market trends for electric vehicles in emerging markets",
        "Examine the role of AI in healthcare cost reduction strategies",
        "Analyze cybersecurity threats in financial technology sector",
        "Research sustainable agriculture technologies and their economic impact"
    ]
    
    for i, suggestion in enumerate(suggestions, 1):
        print(f"{i}. {suggestion}")
    
    print("\n📝 QUERY GUIDELINES:")
    print("─" * 20)
    print("• Be specific and clear about what you want to analyze")
    print("• Include domain context (medical, financial, technical, etc.)")
    print("• Ask for analysis, research, or investigation")
    print("• Avoid yes/no questions - ask for comprehensive analysis")
    
    print("\n" + "─" * 60)
    
    while True:
        print("\nOPTIONS:")
        print("1. Enter your custom query")
        print("2. Use a suggested query")
        print("3. Get help with query formulation")
        print("4. Exit")
        
        choice = input("\nSelect option (1-4): ").strip()
        
        if choice == "1":
            # Custom query input
            query = input("\n📝 Enter your analysis query: ").strip()
            
            if not query:
                print("❌ Query cannot be empty. Please try again.")
                continue
            
            if len(query) < 10:
                print("❌ Query too short. Please provide more details.")
                continue
            
            # Validate query
            if validate_query(query):
                return query
            else:
                print("❌ Query validation failed. Please try again.")
                continue
        
        elif choice == "2":
            # Use suggested query
            print(f"\nSelect a suggestion (1-{len(suggestions)}):")
            try:
                suggestion_choice = int(input("Enter number: ")) - 1
                if 0 <= suggestion_choice < len(suggestions):
                    selected_query = suggestions[suggestion_choice]
                    print(f"\n✅ Selected: {selected_query}")
                    
                    confirm = input("\nUse this query? (y/n): ").strip().lower()
                    if confirm in ['y', 'yes']:
                        return selected_query
                    else:
                        continue
                else:
                    print("❌ Invalid selection. Please try again.")
                    continue
            except ValueError:
                print("❌ Please enter a valid number.")
                continue
        
        elif choice == "3":
            # Query help
            show_query_help()
            continue
        
        elif choice == "4":
            print("👋 Goodbye!")
            return None
        
        else:
            print("❌ Invalid option. Please select 1-4.")

def validate_query(query: str) -> bool:
    """Validate user query"""
    
    # Basic validation checks
    if len(query) < 10:
        print("❌ Query too short (minimum 10 characters)")
        return False
    
    if len(query) > 500:
        print("❌ Query too long (maximum 500 characters)")
        return False
    
    # Check for analysis keywords
    analysis_keywords = [
        'analyze', 'research', 'investigate', 'study', 'examine', 
        'evaluate', 'assess', 'review', 'explore', 'compare'
    ]
    
    if not any(keyword in query.lower() for keyword in analysis_keywords):
        print("💡 Tip: Consider using analysis keywords like 'analyze', 'research', or 'investigate'")
        
        proceed = input("Continue anyway? (y/n): ").strip().lower()
        if proceed not in ['y', 'yes']:
            return False
    
    print("✅ Query validation passed")
    return True

def show_query_help():
    """Display query formulation help"""
    
    print("\n" + "="*50)
    print("📚 QUERY FORMULATION HELP")
    print("="*50)
    
    print("\n🎯 EFFECTIVE QUERY STRUCTURE:")
    print("─" * 30)
    print("1. **Action Word**: Start with analyze, research, investigate, etc.")
    print("2. **Topic**: Clearly state what you want to study")
    print("3. **Context**: Provide domain or industry context")
    print("4. **Scope**: Specify time frame, geography, or other constraints")
    
    print("\n✅ GOOD QUERY EXAMPLES:")
    print("─" * 25)
    print("• 'Analyze the impact of AI on healthcare costs in developed countries'")
    print("• 'Research renewable energy adoption trends in Asia-Pacific region'")
    print("• 'Investigate cybersecurity challenges in financial technology sector'")
    print("• 'Examine the pharmaceutical industry's response to personalized medicine'")
    
    print("\n❌ AVOID THESE QUERY TYPES:")
    print("─" * 28)
    print("• Yes/No questions: 'Is AI good for healthcare?'")
    print("• Too vague: 'Tell me about technology'")
    print("• Too narrow: 'What is GDP?'")
    print("• Multiple unrelated topics: 'AI, blockchain, and cooking recipes'")
    
    print("\n🔍 DOMAIN EXAMPLES:")
    print("─" * 18)
    print("• **Medical**: drug development, diagnostics, healthcare delivery")
    print("• **Financial**: market analysis, investment trends, economic impact")
    print("• **Technology**: AI applications, cybersecurity, digital transformation")
    print("• **Business**: strategy analysis, market research, competitive intelligence")
    
    input("\nPress Enter to continue...")

def display_welcome():
    """Display welcome message and system information"""
    
    print("\n" + "="*70)
    print("🤖 AI-POWERED MULTI-AGENT ANALYSIS SYSTEM")
    print("="*70)
    
    print("\n🚀 SYSTEM CAPABILITIES:")
    print("─" * 22)
    print("• **Research Agent**: Comprehensive information gathering and analysis")
    print("• **Medical Specialist**: Healthcare and pharmaceutical expertise")
    print("• **Financial Analyst**: Market trends and economic analysis")
    print("• **Quality Assurance**: Validation and error detection")
    print("• **Synthesis Agent**: Intelligent integration of findings")
    print("• **Document Generator**: Professional report creation")
    
    print("\n🔧 TECHNICAL SPECIFICATIONS:")
    print("─" * 28)
    print(f"• **AI Model**: {settings.OPENAI_MODEL}")
    print("• **Architecture**: Multi-agent coordination system")
    print("• **Output**: Comprehensive analysis reports")
    print("• **Quality Control**: Automated validation and repair")
    
    print("\n📊 ANALYSIS OUTPUTS:")
    print("─" * 19)
    print("• Executive Summary")
    print("• Comprehensive Analysis Report")
    print("• Specialist Domain Reports")
    print("• Quality Assurance Documentation")
    print("• Technical Data Export")
    print("• Methodology Documentation")

def main():
    """Enhanced main function with interactive query input"""
    
    # Display welcome message
    display_welcome()
    
    # Verify OpenAI setup
    try:
        settings.validate()
        print("\n✅ OpenAI API key configured successfully")
    except ValueError as e:
        print(f"\n❌ Configuration error: {e}")
        print("Please set your OPENAI_API_KEY in the .env file")
        print("\nSetup Instructions:")
        print("1. Create a .env file in the project root")
        print("2. Add: OPENAI_API_KEY=your_actual_api_key_here")
        print("3. Add: OPENAI_MODEL=gpt-4")
        return
    
    # Main interaction loop
    while True:
        try:
            # Get user query
            user_query = get_user_query()
            
            if user_query is None:
                break
            
            # Confirm execution
            print(f"\n🔄 Ready to analyze: '{user_query}'")
            confirm = input("Proceed with analysis? (y/n): ").strip().lower()
            
            if confirm in ['y', 'yes']:
                # Run the analysis
                result = run_ai_multi_agent_system(user_query)
                
                if result:
                    print("\n🎉 Analysis completed successfully!")
                    
                    # Ask if user wants to run another analysis
                    another = input("\nRun another analysis? (y/n): ").strip().lower()
                    if another not in ['y', 'yes']:
                        break
                else:
                    print("\n❌ Analysis failed. Please try again.")
            else:
                print("Analysis cancelled.")
        
        except KeyboardInterrupt:
            print("\n\n⚠️  Analysis interrupted by user.")
            break
        except Exception as e:
            print(f"\n❌ Unexpected error: {e}")
            continue
    
    print("\n👋 Thank you for using the AI Multi-Agent Analysis System!")

if __name__ == "__main__":
    main()

