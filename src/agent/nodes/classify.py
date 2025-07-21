from langchain_core.messages import HumanMessage
from agent.state import State
from agent.prompts import classify_prompt
from agent.utils import call_llm

MOCK_RESPONSE = False  # Toggle to False for API calls

def classify_ticket(state: State) -> State:
    """Classify the ticket into a category."""
    ticket = state["ticket"]
    message = classify_prompt.format(subject=ticket["subject"], description=ticket["description"])
    
    response = call_llm(
        message=message,
        mock_response="Billing" if MOCK_RESPONSE else None,
        max_tokens=50,
        temperature=0
    )
    
    # Remove trailing period
    clean_response = response.rstrip(".")
    
    messages = state["messages"] + [HumanMessage(content=f"Ticket classified as: {clean_response}")]
    return {
        "category": clean_response,
        "messages": messages
    }   