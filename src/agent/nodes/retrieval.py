import os
from agent.state import State
from langchain_core.messages import HumanMessage

def retrieve_context(state: State) -> State:
    """Retrieve context from knowledge base based on ticket category.
    
    Args:
        state (State): Current state with ticket category.
        
    Returns:
        State: Updated state with retrieved context and messages.
    
    """
    
    category = state["category"].rstrip(".")
    filepath = f"src/agent/knowledge/{category.lower()}.txt"
    
    if not os.path.exists(filepath):
        context = "No relevant documentation found."
        messages = state["messages"] + [HumanMessage(content=f"Retrieval failed: No documentation for category {category}.")]
        return {"context": context, "messages": messages}
    
    with open(filepath, "r") as file:
        context = file.read().strip()[:1500]
    
    messages = state["messages"] + [HumanMessage(content=f"Retrieved context for category {category}.")]
    return {
        "context": context,
        "messages": messages
    }