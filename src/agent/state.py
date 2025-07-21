from typing import Dict, Any, Annotated
from typing_extensions import TypedDict
from langgraph.graph.message import add_messages

class State(TypedDict):
    messages: Annotated[list, add_messages] # Tracks interactions
    ticket: Dict[str, str]                  # Ticket details (subject, description)
    category: str                           # Classified category
    attempt: int                            # Retry attempts
    context: str                            # Retrieved context
    draft: str                              # Draft response
    approved: bool                          # Draft approval status
    feedbacks: list                         # Reviewer feedback
    drafts: list                            # List of drafts
    feedbacks: list                         # List of feedback
    output: str                             # Final response or escalation