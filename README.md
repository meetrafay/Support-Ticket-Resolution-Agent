# 🛠️ Support Ticket Resolution Agent

This project implements an automated support ticket resolution agent using **LangGraph**, designed to:

- Process customer support tickets  
- Classify them  
- Retrieve relevant context  
- Generate draft responses  
- Review drafts  
- Retry or escalate as needed  

A **Gradio UI** enhances user interaction with a loading indicator and input validation. The agent is modular, robust, and gracefully handles edge cases, supporting various ticket types like **Billing, Technical, Security, and General**.

---

## 📌 Project Overview

The agent processes tickets through the following workflow:

1. **Classify** – Identifies the ticket category (Billing, Technical, etc.)  
2. **Retrieve** – Fetches relevant context from knowledge base (`src/agent/knowledge/`)  
3. **Draft** – Generates a professional response  
4. **Review** – Evaluates response quality  
5. **Retry Draft** – Attempts improvement (max 3 tries)  
6. **Output** – Approves or escalates

### 🔧 Technologies Used

- **LangGraph** – Orchestration and state flow  
- **Hugging Face** – `mistralai/Mistral-7B-Instruct-v0.2` for LLM  
- **Gradio** – User-friendly interface for ticket submission  
- **Clean Modular Architecture**

---

## ⚙️ Setup Instructions

### ✅ Prerequisites

- Python 3.10+  
- Virtual environment (recommended)  
- Hugging Face API token  
- LangGraph CLI  
- Gradio for UI  

---

### ✅ Installation

#### 1. Clone the Repository

```bash
git clone https://github.com/meetrafay/Support-Ticket-Resolution-Agent.git
cd Support-Ticket-Resolution-Agent
````

#### 2. Set Up Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

#### 3. Install Dependencies

```bash
pip install -r requirements.txt
pip install -e .
```

Requirements include:

* `langgraph`
* `langchain-community`
* `huggingface_hub`
* `python-dotenv`
* `gradio`

---

### ✅ Configure Environment

Create a `.env` file:

```env
HUGGINGFACE_API_TOKEN=<your-huggingface-token>
LANGCHAIN_TRACING_V2=false
```

Get your token here: [https://huggingface.co/settings/tokens](https://huggingface.co/settings/tokens)

---

### ✅ Set Up Knowledge Base

Ensure these files exist inside `src/agent/knowledge/`:

* `billing.txt`
* `technical.txt`
* `security.txt`
* `general.txt`

Each should contain relevant resolution guidance.

---

### ✅ Start LangGraph UI (Optional)

```bash
langgraph dev
```

Then open: [http://localhost:8123](http://localhost:8123)

---

## 🚀 Running and Testing the Agent

### ✅ 1. Command-Line Interface

```bash
python src/agent/graph.py
```

**Sample Billing Ticket:**

```json
{
  "subject": "I was charged twice for the same service",
  "description": "Hi, I noticed two charges..."
}
```

**Sample Output:**

```json
{
  "category": "Billing",
  "draft": "Hello Customer, Thank you for contacting us...",
  "approved": true
}
```

---

### ✅ 2. Gradio UI

```bash
python app.py
```

Open: [http://localhost:7860](http://localhost:7860)

**Enter a ticket:**

* Subject: *Max 100 characters* (e.g., "I was charged twice")
* Description: *Max 500 characters* (e.g., "Two charges on my card this month.")

**Click "Submit Ticket"**

**Observe:**

* Loading message: "Processing your ticket..."
* Response with:

  * Category
  * Draft (or escalation message)
  * Feedback (if escalated)

**Example:**

```
**Category**: Billing  
**Output**: Hello Customer, Thank you for contacting us... Best regards, Support Team
```

---

### ✅ Toggle Mock Responses

To run with real LLM (not mock), set:

```python
MOCK_RESPONSE = False
```

In these files:

* `src/agent/nodes/classify.py`
* `src/agent/nodes/draft.py`
* `src/agent/nodes/review.py`
* `src/agent/nodes/retry_draft.py`

Ensure `.env` has a valid Hugging Face token.

---

### ✅ View Escalation Logs

See `escalation_log.csv`:

```
timestamp,subject,description,category,draft,reason
"2025-07-21 23:05:45","Can't log in...","I keep getting an error...","Billing","Hello Customer,...","Draft rejected after 3 attempts..."
```

---

### ✅ Use LangGraph UI (Optional)

Open: [http://localhost:8123](http://localhost:8123)

Try a custom ticket:

* Subject: I was charged twice
* Description: Two charges on my card

**Observe:**

* Category assignment
* Context retrieval
* Draft response
* Final decision (approved or escalated)

---

## 🧠 Design and Architectural Decisions

### ✅ Workflow Design

* **LangGraph**: Stateful orchestration for clear transitions & retry logic
* **Nodes**: Single-purpose modules:

  * `classify`
  * `retrieve`
  * `draft`
  * `review`
  * `retry_draft`
* **State**: Defined in `state.py` with fields:

  * `ticket`, `category`, `context`, `draft`, `approved`, `attempt`, `drafts`, `feedbacks`, `output`

---

### ✅ Modular Architecture

* **Nodes**: `src/agent/nodes/*.py`
* **Shared Logic**: `utils.py` (e.g., `call_llm`)
* **Knowledge Base**: Text files in `src/agent/knowledge/`

---

### ✅ Prompt Engineering

* `prompts.py`: Node-specific prompts

  * `classify_prompt`: Ensures only valid categories
  * `review_prompt`: Approves minor issues, reduces false escalations

---

### ✅ Error Handling

* **API Errors**: Graceful fallback in `utils.py`
* **Classify**: Defaults to `General` if LLM output invalid
* **Review**: Escalates if not clearly "Approved"
* **Retrieve**: Warns if file missing
* **Gradio**: Validates inputs:

  * Subject ≤100 chars
  * Description ≤500 chars

---

### ✅ Token Optimization

* `classify`: `max_tokens=50`
* `review`: `max_tokens=100`
* `draft`/`retry_draft`: `max_tokens=400`

---

### ✅ Traceability

* `state["messages"]`: Logs every step
* `escalation_log.csv`: Records all escalations
* **LangGraph UI**: Visual step-by-step
* **Gradio UI**: Shows processing state & result

---

### ✅ Gradio UI

Implemented in `app.py`:

* ✅ Loading indicator
* ✅ Input validation
* ✅ Displays:

  * Category
  * Draft
  * Feedback (if escalated)
* Runs on: [http://localhost:7860](http://localhost:7860)

---

## ✅ Testing

### ✔️ Sample Tickets

```bash
python src/agent/graph.py
```

* Billing: should pass on first try
* Technical: triggers retry/escalation

---

### ✔️ Gradio UI

```bash
python app.py
```

Open: [http://localhost:7860](http://localhost:7860)

**Test Cases:**

* ✅ Valid input → Successful
* ❌ Empty input → "Please provide both subject and description."
* ❌ Too long → Error for subject or description length
* ✅ Confirm loading spinner and output

---

### ✔️ Edge Cases

| Case                | Behavior                |
| ------------------- | ----------------------- |
| 🔄 Missing file     | Fallback message shown  |
| ❌ Invalid category  | Fallback to `General`   |
| 🔒 Bad API token    | Logs error + fallback   |
| 🖼️ Gradio UI fails | Check port 7860 is free |

---

## 📈 Future Improvements

* Add full docstrings and inline comments
* Dynamic loading of knowledge base
* Retry logic for API rate limits
* UI enhancements: history, visual trace

---

## 🧩 Troubleshooting

| Problem                      | Solution                                        |
| ---------------------------- | ----------------------------------------------- |
| **API Errors**               | Check `HUGGINGFACE_API_TOKEN` in `.env`         |
| **LangGraph UI not loading** | Ensure `langgraph.json` points to correct graph |
| **Gradio UI not loading**    | Free port `7860`, ensure `gradio` is installed  |
| **Drafts cut short**         | Increase `max_tokens=400` in `draft.py`         |
| **Unexpected escalations**   | Tweak `review_prompt`                           |
| **Input validation**         | Keep subject ≤100, description ≤500 chars       |

```