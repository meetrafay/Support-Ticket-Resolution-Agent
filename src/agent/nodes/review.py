import os
import csv
from datetime import datetime
from langchain_core.messages import HumanMessage
from agent.state import State
from agent.prompts import review_prompt, feedback_prompt
from agent.utils import call_llm

MOCK_RESPONSE = False  # Toggle to False for API calls

def review_draft(state: State) -> State:
    """Review the draft response and approve or escalate."""
    ticket = state["ticket"]
    category = state["category"]
    context = state["context"]
    draft = state["draft"]
    attempt = state.get("attempt", 0)
    drafts = state.get("drafts", []) + [draft]
    feedbacks = state.get("feedbacks", [])
    
    message = review_prompt.format(
        subject=ticket["subject"],
        description=ticket["description"],
        category=category,
        context=context,
        draft=draft
    )
    
    mock_response = "Approved" if MOCK_RESPONSE else None
    response = call_llm(
        message=message,
        mock_response=mock_response,
        max_tokens=100,  # Short output (Approved/Escalate + feedback)
        temperature=0
    )
    
    # Parse response strictly
    response = response.strip()
    review_result = "Approved" if response.startswith("Approved") else "Escalate"
    feedback = response.split("\nFeedback: ")[1].strip() if "\nFeedback: " in response else None
    
    messages = state["messages"] + [HumanMessage(content=f"Draft review result: {review_result}")]
    
    if review_result == "Approved":
        return {
            "approved": True,
            "output": draft,
            "messages": messages,
            "drafts": drafts,
            "feedbacks": feedbacks,
            "attempt": attempt
        }
    
    if feedback:
        messages = messages + [HumanMessage(content=f"Feedback for rejected draft: {feedback}")]
    
    if attempt >= 2:
        log_filepath = "escalation_log.csv"
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = {
            "timestamp": timestamp,
            "subject": ticket["subject"],
            "description": ticket["description"],
            "category": category,
            "draft": draft,
            "reason": f"Draft rejected after {attempt + 1} attempts. Feedback: {feedback or 'No specific feedback provided.'}"
        }
        
        file_exists = os.path.exists(log_filepath)
        with open(log_filepath, "a", newline="") as csvfile:
            fieldnames = ["timestamp", "subject", "description", "category", "draft", "reason"]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            if not file_exists:
                writer.writeheader()
            writer.writerow(log_entry)
        
        return {
            "approved": False,
            # "feedback": feedback,
            "messages": messages,
            "drafts": drafts,
            "feedbacks": feedbacks + [feedback] if feedback else feedbacks,
            "attempt": attempt + 1,
            "output": "Ticket escalated to human agent after max retries."
        }
    
    return {
        "approved": False,
        # "feedback": feedback,
        "messages": messages,
        "drafts": drafts,
        "feedbacks": feedbacks + [feedback] if feedback else feedbacks,
        "attempt": attempt + 1
    }