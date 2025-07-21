from langchain_core.messages import HumanMessage
from agent.state import State
from agent.prompts import draft_prompt
from agent.utils import call_llm

MOCK_RESPONSE = False  # Toggle to False for API calls

def generate_draft(state: State) -> State:
    """Generate a draft response based on ticket and context.
    
    Args:
        state (State): Current state with ticket, category, and context.
        
    Returns:
        State: Updated state with draft response and messages.
    """
    
    ticket = state["ticket"]
    category = state["category"]
    context = state["context"]
    
    message = draft_prompt.format(
        subject=ticket["subject"],
        description=ticket["description"],
        category=category,
        context=context
    )
    
    mock_response = (
        "Dear Customer,\n\nThank you for reaching out. We apologize for the double charge on your account. "
        "Please verify your transaction history in the billing portal to confirm the charges. "
        "This issue may be due to a duplicate subscription or processing error. "
        "We have escalated your case to our billing team for further investigation, and you will hear back within 24-48 hours.\n\n"
        "Best regards,\nSupport Team"
    ) if MOCK_RESPONSE else None
    
    response = call_llm(
        message=message,
        mock_response=mock_response,
        max_tokens=400,
        temperature=0.3
    )
    
    messages = state["messages"] + [HumanMessage(content=f"Draft response generated: {response}")]
    return {
        "draft": response,
        "messages": messages
    }