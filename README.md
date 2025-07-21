# 🛠️ Support Ticket Resolution Agent

This project implements an automated **support ticket resolution agent** using [LangGraph](https://docs.langgraph.dev), designed to:

- Process customer support tickets  
- Classify them  
- Retrieve relevant context  
- Generate draft responses  
- Review drafts  
- Retry or escalate as needed

It is modular, robust, and gracefully handles edge cases — suitable for various ticket types like **Billing**, **Technical**, **Security**, and **General**.

---

## 📌 Project Overview

The agent processes tickets through the following **workflow**:

1. **Classify**: Identifies the ticket category (Billing, Technical, etc.)  
2. **Retrieve**: Fetches relevant context from knowledge base (`src/agent/knowledge/`)  
3. **Draft**: Generates a professional response  
4. **Review**: Evaluates response quality  
5. **Retry Draft**: Attempts improvement (max 3 tries)  
6. **Output**: Approves or escalates

**Technologies:**
- **LangGraph**: Orchestration and state flow  
- **Hugging Face**: `mistralai/Mistral-7B-Instruct-v0.2` for LLM  
- **Clean modular architecture**

---

## ⚙️ Setup Instructions

### ✅ Prerequisites

- Python 3.10+
- Virtual environment (recommended)
- Hugging Face API token
- LangGraph CLI

---

### ✅ Installation

#### 1. Clone the Repository
```bash
git clone https://github.com/meetrafay/Support-Ticket-Resolution-Agent.git
cd support-agent
````

#### 2. Set Up Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

#### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

**Included in `requirements.txt`:**

* `langgraph`
* `langchain-community`
* `huggingface_hub`
* Other dependencies for LLM and workflow orchestration

---

### ✅ Configure Environment

1. Create a `.env` file:

```
HUGGINGFACE_API_TOKEN=<your-huggingface-token>
LANGCHAIN_TRACING_V2=false
```

2. Get your Hugging Face token from:
   [https://huggingface.co/settings/tokens](https://huggingface.co/settings/tokens)

---

### ✅ Set Up Knowledge Base

Ensure the following files exist inside `src/agent/knowledge/`:

```
billing.txt
technical.txt
security.txt
general.txt
```

Each should contain relevant resolution guidance.

---

### ✅ Start LangGraph UI

```bash
langgraph dev
```

Then open:
[http://localhost:8123](http://localhost:8123)

---

## 🚀 Running and Testing the Agent

### ✅ Run the Agent

```bash
python src/agent/graph.py
```

Sample Billing Ticket:

```json
{
  "subject": "I was charged twice for the same service",
  "description": "Hi, I noticed two charges..."
}
```

Sample Output:

```json
{
  "category": "Billing",
  "draft": "Hello Customer, Thank you for contacting us...",
  "approved": true,
  ...
}
```

---

### ✅ Toggle Mock Responses

To run with real LLM instead of mock:

1. Set `MOCK_RESPONSE = False` in:

   * `classify.py`
   * `draft.py`
   * `review.py`
   * `retry_draft.py`
2. Ensure `.env` has a valid Hugging Face token.

---

### ✅ View Escalation Logs

Check `escalation_log.csv`:

```
timestamp,subject,description,category,draft,reason
"2025-07-21 23:05:45","Can't log in...","I keep getting an error...","Billing","Hello Customer,...","Draft rejected after 3 attempts..."
```

---

### ✅ Use LangGraph UI

Open: [http://localhost:8123](http://localhost:8123)

Try a custom ticket:

* **Subject**: I was charged twice
* **Description**: Two charges on my card

Observe:

* Category assignment
* Context retrieved
* Draft response
* Final decision (approved or escalated)

---

## 🧠 Design and Architectural Decisions

### ✅ Workflow Design

* **LangGraph**: Stateful, graph-based orchestration
* **Nodes**: Single-purpose modules:

  * `classify`
  * `retrieve`
  * `draft`
  * `review`
  * `retry_draft`
* **State**: Defined in `state.py`, shared across nodes

### ✅ Modular Architecture

* Nodes: `src/agent/nodes/*.py`
* Shared logic: `utils.py`
* Knowledge base: `src/agent/knowledge/*.txt`

---

### ✅ Prompt Engineering

* `prompts.py`: Tailored per node
* `classify_prompt`: Ensures valid categories only
* `review_prompt`: Approves minor issues to reduce false escalations

---

### ✅ Error Handling

* **API Errors**: Graceful fallback in `utils.py`
* **Classify**: Defaults to `General` if invalid output
* **Review**: Escalates if response isn’t “Approved ✅”
* **Retrieve**: Warns if knowledge file is missing

---

### ✅ Token Optimization

* `classify`: max\_tokens=50
* `review`: max\_tokens=100
* `draft` & `retry`: max\_tokens=400

---

### ✅ Traceability

* `state["messages"]`: Logs all steps
* `escalation_log.csv`: For escalations
* **LangGraph UI**: Live visual debugging

---

## ✅ Testing

### ✔️ Sample Tickets

```bash
python src/agent/graph.py
```

* Billing ticket: should pass first try
* Technical ticket: triggers retry/escalation

### ✔️ Edge Cases

* 🔄 **Missing file**: Rename `billing.txt` → fallback message shown
* ❌ **Invalid category**: Set mock classify → fallback to "General"
* 🔒 **Bad API token**: Observe fallback + logs

---

## 📈 Future Improvements

* Add detailed docstrings + inline comments
* Enable dynamic knowledge base loading
* Add retry logic for API rate limits (exponential backoff)

---

## 🧩 Troubleshooting

| Problem                | Solution                                                  |
| ---------------------- | --------------------------------------------------------- |
| API Errors             | Check `HUGGINGFACE_API_TOKEN` in `.env`                   |
| UI Not Loading         | Ensure `langgraph.json` points to `src.agent.graph:graph` |
| Drafts Cut Short       | Increase `max_tokens=400` in `draft.py`                   |
| Unexpected Escalations | Tweak `review_prompt` for leniency                        |

---
