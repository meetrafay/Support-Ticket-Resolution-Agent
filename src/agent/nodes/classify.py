from langchain_core.messages import HumanMessage
from agent.state import State
from agent.prompts import classify_prompt
from agent.utils import call_llm

MOCK_RESPONSE = False  # Toggle to False for API calls

def classify_ticket(state: State) -> State:
    """Classify the ticket into a category.

    Args:
        state (State): Current state with ticket details.

    Returns:
        State: Updated state with category and messages.
    """
    
    ticket = state["ticket"]
    message = classify_prompt.format(subject=ticket["subject"], description=ticket["description"])
    
    valid_categories = ["Billing", "Technical", "Security", "General"]
    mock_response = "Billing" if MOCK_RESPONSE else None
    
    try:
        response = call_llm(
            message=message,
            mock_response=mock_response,
            max_tokens=50,
            temperature=0
        )
        # Validate output
        if response.rstrip('.').strip() not in valid_categories:
            error_msg = f"Invalid category: {response}. Using fallback: General"
            messages = state["messages"] + [HumanMessage(content=error_msg)]
            return {
                "category": "General",
                "messages": messages
            }
    except ValueError as e:
        error_msg = f"Classification error: {str(e)}. Using fallback: General"
        messages = state["messages"] + [HumanMessage(content=error_msg)]
        return {
            "category": "General",
            "messages": messages
        }
    
    messages = state["messages"] + [HumanMessage(content=f"Ticket classified as: {response}")]
    return {
        "category": response,
        "messages": messages
    } 