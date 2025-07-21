Support Ticket Resolution Agent
This project implements an automated support ticket resolution agent using LangGraph, designed to process customer support tickets, classify them, retrieve relevant context, generate draft responses, review drafts, and retry or escalate as needed. The agent is modular, robust, and handles edge cases gracefully, making it suitable for handling various ticket types (Billing, Technical, Security, General).
Project Overview
The agent processes tickets through a workflow:

Classify: Identifies the ticket category (e.g., Billing, Technical).
Retrieve: Fetches context from a knowledge base (src/agent/knowledge/).
Draft: Generates a professional response with a greeting, actionable steps, and closing.
Review: Evaluates the draft for relevance, completeness, and professionalism.
Retry Draft: Regenerates drafts based on feedback (up to 3 attempts).
Output: Returns the approved draft or escalates to a human agent.

The project uses LangGraph for workflow orchestration, Hugging Face’s mistralai/Mistral-7B-Instruct-v0.2 for LLM tasks, and a clean directory structure for modularity.
Setup Instructions
Prerequisites

Python: 3.8 or higher.
Virtual Environment: Recommended for dependency isolation.
Hugging Face API Token: Required for LLM calls.
LangGraph: For workflow visualization and execution.

Installation

Clone the Repository:
git clone <repository-url>
cd support-agent


Set Up Virtual Environment:
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate


Install Dependencies:
pip install -r requirements.txt

The requirements.txt includes:

langgraph
langchain-community
huggingface_hub
Other dependencies for LLM and workflow management.


Configure Environment:

Create a .env file in the project root:HUGGINGFACE_API_TOKEN=<your-huggingface-token>
LANGCHAIN_TRACING_V2=false


Obtain a Hugging Face API token from https://huggingface.co/settings/tokens.
Set LANGCHAIN_TRACING_V2=false to disable LangSmith tracing (optional).


Set Up Knowledge Base:

Ensure src/agent/knowledge/ contains files like billing.txt, technical.txt, security.txt, and general.txt with relevant support instructions.


Start LangGraph Server:
langgraph dev


Access the UI at http://localhost:8123 to visualize and test the workflow.



Running and Testing the Agent
Running the Agent

Execute the Main Script:
python src/agent/graph.py


This runs the agent with sample tickets (Billing and Technical).
Outputs include classification, draft responses, and review results.
Example output for a Billing ticket:Ticket Input (Billing): {'subject': 'I was charged twice for the same service', 'description': 'Hi, I noticed two charges...'}
Result: {
    'category': 'Billing',
    'draft': 'Hello Customer,\n\nThank you for contacting us... Best regards,\nSupport Team',
    'approved': True,
    ...
}




Toggle Mock Responses:

Edit src/agent/nodes/classify.py, draft.py, review.py, retry_draft.py to set MOCK_RESPONSE = False for real LLM calls.
Ensure HUGGINGFACE_API_TOKEN is valid in .env.


View Logs:

Check escalation_log.csv for escalated tickets:timestamp,subject,description,category,draft,reason
"2025-07-21 23:05:45","Can't log in...","I keep getting an error...","Billing","Hello Customer,...","Draft rejected after 3 attempts. Feedback: Add specific troubleshooting steps..."





Testing the Agent

Test with Sample Tickets:

Run python src/agent/graph.py to test predefined Billing and Technical tickets.
Verify Billing ticket approves on first attempt and Technical ticket escalates if misclassified (mock mode).


Test Edge Cases:

Missing Knowledge File: Rename src/agent/knowledge/billing.txt, run graph.py, confirm fallback context: No knowledge base found for category: Billing.
Invalid LLM Output: Set mock response in classify.py to InvalidCategory, confirm fallback to General.
API Error: Set invalid HUGGINGFACE_API_TOKEN, run with MOCK_RESPONSE = False, confirm fallback to General (classify) or Escalate (review).


Use LangGraph UI:

Open http://localhost:8123.
Input a ticket (e.g., subject: "I was charged twice", description: "Two charges on my card") and trace the workflow.
Verify state (category, context, draft, approved) at each node.



Design and Architectural Decisions
Workflow Design

LangGraph Workflow: Adopted LangGraph for its stateful, graph-based orchestration, enabling clear node transitions and conditional routing (e.g., retry_draft vs. END).
Nodes: Split into single-purpose nodes (classify, retrieve, draft, review, retry_draft) for modularity and reusability.
State Management: Defined State (src/agent/state.py) with fields (ticket, category, context, draft, approved, attempt, drafts, feedbacks, output) for traceability across nodes.

Key Decisions

Modular Architecture:

Nodes are independent (src/agent/nodes/*.py), with shared logic in utils.py (e.g., call_llm) to keep code DRY.
Knowledge base (src/agent/knowledge/*.txt) allows easy updates for new ticket types.


Prompt Engineering:

prompts.py: Tailored prompts for each node (e.g., classify_prompt for single-word output, draft_prompt for concise responses).
review_prompt: Relaxed to approve suitable drafts with minor issues, reducing escalations.


Error Handling:

utils.py: Try-catch for Hugging Face API errors (e.g., rate limits, invalid token) with fallback responses.
classify.py: Validates LLM output against valid categories, falls back to General.
review.py: Validates Approved/Escalate, falls back to Escalate for invalid outputs.
retrieval.py: Handles missing knowledge files with a fallback context.


Token Optimization:

max_tokens: Set to 50 (classify), 100 (review), 400 (draft, retry_draft) based on output needs to prevent truncation while ensuring efficiency.


Traceability:

messages in State logs node actions (e.g., Ticket classified as: Billing).
escalation_log.csv: Records escalations with timestamp, ticket details, and feedback.
LangGraph UI (http://localhost:8123) visualizes state and flow.


Testing:

Mock responses (MOCK_RESPONSE = True) for consistent testing without API costs.
Real LLM support (mistralai/Mistral-7B-Instruct-v0.2) for production.
Edge case tests for missing files, invalid outputs, and API errors.



Trade-Offs

Mock vs. Real LLM: Mock responses prioritize testing speed but may miss real-world LLM variability (mitigated by testing with MOCK_RESPONSE = False).
Retry Limit: Set to 3 attempts to balance automation and escalation, preventing infinite loops.
General Category Fallback: Used for classification errors to ensure workflow continuity, though it may reduce specificity for edge cases.

Troubleshooting

API Errors: Verify HUGGINGFACE_API_TOKEN in .env and check quota at https://huggingface.co/settings/tokens.
LangGraph UI Issues: Ensure langgraph.json points to src.agent.graph:graph and LANGCHAIN_TRACING_V2=false.
Draft Truncation: Confirm max_tokens=400 in draft.py and retry_draft.py.
Escalations: Check review_prompt for overly strict criteria if drafts are rejected unexpectedly.

Future Improvements

Add docstrings and inline comments for better code quality.
Support dynamic knowledge base updates without file edits.
Implement retry logic for API rate limits with exponential backoff.

For issues or contributions, contact the repository maintainer.