from langgraph.graph import StateGraph, START, END
from agent.state import State
from agent.nodes import classify_ticket, retrieve_context, generate_draft, review_draft, retry_draft


# Initialize graph with custom State
builder = StateGraph(State)

# Add nodes
builder.add_node("classify", classify_ticket)
builder.add_node("retrieve", retrieve_context)
builder.add_node("draft", generate_draft)
builder.add_node("review", review_draft)
builder.add_node("retry_draft", retry_draft)

# Set edges
builder.add_edge(START, "classify")
builder.add_edge("classify", "retrieve")
builder.add_edge("retrieve", "draft")
builder.add_edge("draft", "review")

# Conditional edge for review
def route_review(state: State) -> str:
    """Route to retry_draft if not approved and attempts < 3, else END."""
    if state["approved"] or state["attempt"] >= 3:
        return END
    return "retry_draft"

builder.add_conditional_edges("review", route_review, {"retry_draft": "retry_draft", END: END})
builder.add_edge("retry_draft", "review")

# Compile graph
graph = builder.compile(name="Support Agent")

if __name__ == "__main__":
    # Sample ticket (Billing, should approve)
    ticket_example = {
        "subject": "I was charged twice for the same service",
        "description": "Hi, I noticed two charges on my credit card for this month's billing. Can you look into this?"
    }
    result = graph.invoke({"ticket": ticket_example, "messages": [], "attempt": 0, "drafts": [], "feedbacks": []})
    print("Ticket Input (Billing):", ticket_example)
    print("Result:", result)
