Support Ticket Resolution Agent
A LangGraph-based agent for automating the classification, drafting, and review of customer support tickets. The agent processes tickets through a workflow that classifies the ticket, retrieves relevant knowledge, generates a draft response, reviews it for quality, and retries if needed, escalating to a human agent after three failed attempts.
Project Overview
The agent handles customer support tickets in categories like Billing, Technical, Security, and General. It uses a LangGraph workflow to:

Classify: Identifies the ticket category (e.g., Billing) using an LLM.
Retrieve: Pulls relevant context from knowledge files (e.g., billing.txt).
Draft: Generates a professional response based on the ticket and context.
Review: Evaluates the draft for relevance, completeness, and professionalism.
Retry Draft: Regenerates the draft with feedback if rejected (up to 3 attempts).
Output: Sets the approved draft as the final response or escalates to a human agent.

The workflow is visualized using the LangGraph Server UI at http://localhost:8123.
Prerequisites

Python: Version 3.10 or higher.
Virtual Environment: Recommended for dependency isolation.
Hugging Face API Token: Required for LLM calls (if not using mock responses).
Git: Optional, for cloning the repository.

Setup Instructions

Clone the Repository (if applicable):
git clone <repository-url>
cd support-agent


Create and Activate a Virtual Environment:
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows


Install Dependencies:The project uses frozen dependencies listed in requirements.txt for reproducibility.
pip install -r requirements.txt

This installs langgraph, langchain, python-dotenv, and other required packages.

Set Environment Variables:Create a .env file in the project root (/home/abdulrafay/Desktop/str_agent/support-agent/):
HUGGINGFACE_API_TOKEN=your_huggingface_token
LANGCHAIN_TRACING_V2=false


Replace your_huggingface_token with a valid token from https://huggingface.co/settings/tokens (required for real LLM calls).
LANGCHAIN_TRACING_V2=false disables LangSmith integration to avoid warnings.



Running the Agent

Execute the Workflow:
python src/agent/graph.py

This runs the agent with two sample tickets:

Billing Ticket: A double-charge issue, expected to approve on the first attempt.
Technical Ticket: A login issue, may retry or escalate after three attempts.

Example Output (with MOCK_RESPONSE = True in node files):
Ticket Input (Billing): {'subject': 'I was charged twice for the same service', 'description': 'Hi, I noticed two charges on my credit card for this month's billing. Can you look into this?'}
Result: {
    'messages': [...],
    'ticket': {...},
    'category': 'Billing',
    'context': 'Billing Support Documentation:\n- Double charges: Check the billing portal...',
    'draft': 'Dear Customer,\n\nThank you for reaching out... Refunds typically process within 5-7 business days...',
    'approved': True,
    'output': 'Dear Customer,\n\nThank you for reaching out...',
    'attempt': 0,
    'drafts': ['Dear Customer,\n\nThank you for reaching out...'],
    'feedbacks': [],
    'feedback': None
}

Ticket Input (Technical): {'subject': 'Can't log in to my account', 'description': 'I keep getting an error when trying to log in on my phone.'}
Result: {
    'messages': [...],
    'ticket': {...},
    'category': 'Billing',
    'context': 'Billing Support Documentation:\n- Double charges: Check the billing portal...',
    'draft': 'Dear Customer,\n\nThank you for contacting us...',
    'approved': False,
    'output': 'Ticket routed to human agent for review.',
    'attempt': 3,
    'drafts': [...],
    'feedbacks': ['Draft is not relevant...', 'Draft lacks specific troubleshooting...'],
    'feedback': 'Draft lacks specific troubleshooting...'
}


Using Real LLM (Optional):

Edit src/agent/nodes/classify.py, draft.py, review.py, and retry_draft.py to set MOCK_RESPONSE = False.
Ensure HUGGINGFACE_API_TOKEN is valid in .env.
Run python src/agent/graph.py.
Expect better classification (e.g., Technical for login issues) and improved draft approvals.



Visualizing with LangGraph Server UI

Start the LangGraph Server:
langgraph dev


Access the UI:

Open http://localhost:8123 in a browser.
View the workflow: START -> classify -> retrieve -> draft -> review -> [retry_draft] -> END.
Inspect node states (e.g., category, context, draft) for debugging.
Test tickets interactively by submitting them in the UI.


Notes:

A LangSmith warning may appear in the UI but can be ignored (controlled by LANGCHAIN_TRACING_V2=false).
The UI visualizes the graph and state without requiring external services.



Project Structure
/home/abdulrafay/Desktop/str_agent/support-agent/
├── src/
│   └── agent/
│       ├── nodes/
│       │   ├── classify.py      # Classifies ticket category
│       │   ├── retrieval.py     # Retrieves knowledge base context
│       │   ├── draft.py         # Generates draft response
│       │   ├── review.py        # Reviews draft for quality
│       │   ├── retry_draft.py   # Retries draft with feedback
│       │   └── __init__.py
│       ├── knowledge/
│       │   ├── billing.txt      # Billing support documentation
│       │   ├── technical.txt    # Technical support documentation
│       │   ├── security.txt     # Security support documentation
│       │   ├── general.txt      # General support documentation
│       ├── graph.py             # Defines the LangGraph workflow
│       ├── state.py            # State definition
│       ├── prompts.py          # Prompts for LLM calls
│       ├── utils.py            # Centralized LLM logic
│       └── __init__.py
├── requirements.txt            # Frozen dependencies
├── langgraph.json             # LangGraph CLI configuration
├── .env                       # Environment variables
├── escalation_log.csv         # Log of escalated tickets
├── README.md                  # This file
├── pyproject.toml             # Project metadata
├── LICENSE
├── Makefile
├── static/
├── tests/
└── venv/

Testing

Run Tests:
python src/agent/graph.py


Tests two sample tickets (Billing and Technical).
Verify the Billing ticket approves on the first attempt.
Check if the Technical ticket retries up to three times and escalates if needed.


Check Escalation Log:

Open escalation_log.csv to verify escalated tickets (e.g., Technical ticket after max attempts):timestamp,subject,description,category,draft,reason
"2025-07-20 18:09:45","Can't log in to my account","I keep getting an error when trying to log in on my phone.","Billing","Dear Customer,...","Draft rejected after 3 attempts. Feedback: Draft lacks specific troubleshooting..."




Visualize in UI:

Run langgraph dev and open http://localhost:8123.
Submit a ticket (e.g., {"subject": "I was charged twice...", "description": "..."}) to trace the workflow.
Verify the context field in the retrieve node includes detailed knowledge base content.



Troubleshooting

ModuleNotFoundError:

Issue: No module named 'src.agent.nodes'.
Fix: Ensure pip install -r requirements.txt is run in the virtual environment. Verify src/agent/nodes/__init__.py exists.


LangGraph UI Warning:

Issue: LangSmith API key warning in the UI.
Fix: Ignore the warning (controlled by LANGCHAIN_TRACING_V2=false). Alternatively, add a LANGSMITH_API_KEY from https://smith.langchain.com.


Hugging Face API Errors (if MOCK_RESPONSE = False):

Issue: LLM calls fail.
Fix: Verify HUGGINGFACE_API_TOKEN in .env and check quota at https://huggingface.co/settings/tokens.


Review Rejections:

Issue: Drafts are rejected too often.
Fix: Ensure src/agent/knowledge/*.txt files are detailed (e.g., include refund timelines, troubleshooting steps). Check prompts.py for strict review criteria.



Notes

The agent uses mock responses by default (MOCK_RESPONSE = True) for testing. Set MOCK_RESPONSE = False in node files for real LLM calls with Hugging Face’s mistralai/Mistral-7B-Instruct-v0.2.
The knowledge base (src/agent/knowledge/) contains detailed documentation for Billing, Technical, Security, and General categories to ensure high-quality drafts.
The project is optimized for reproducibility with requirements.txt and a clean directory structure.
