from langchain_core.messages import HumanMessage
from agent.state import State
from agent.prompts import draft_prompt
from agent.utils import call_llm

MOCK_RESPONSE = False  # Toggle to False for API calls

def retry_draft(state: State) -> State:
    """Regenerate the draft using feedback."""
    ticket = state["ticket"]
    category = state["category"]
    context = state["context"]
    feedbacks = state["feedbacks"]
    
    message = draft_prompt.format(
        subject=ticket["subject"],
        description=ticket["description"],
        category=category,
        context=f"{context}\n\nFeedback from previous draft: {feedbacks or 'No specific feedback provided. Ensure the response is concise and actionable.'}"
    )
    
    mock_response = (
        "Hello Customer,\n\nThank you for contacting us regarding the double charge on your account. We apologize for the inconvenience. "
        "Please check your transaction history at https://billing.company.com to confirm the charges. If duplicates are found, submit a ticket with the transaction IDs, "
        "and a refund will be processed within 5-7 business days. If the issue persists, contact our billing team for further assistance.\n\nBest regards,\nSupport Team"
    ) if MOCK_RESPONSE else None
    
    response = call_llm(
        message=message,
        mock_response=mock_response,
        max_tokens=400,
        temperature=0.3
    )
    
    messages = state["messages"] + [HumanMessage(content=f"Retry draft generated: {response}")]
    return {
        "draft": response,
        "messages": messages
    }