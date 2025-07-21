from langchain.prompts import PromptTemplate

# Classification prompt
classify_prompt = PromptTemplate.from_template("""
Classify the ticket into one of: [Billing, Technical, Security, General]
Subject: {subject}
Description: {description}
Respond ONLY with the category name (e.g., Billing).
""")

# Draft generation prompt
draft_prompt = PromptTemplate.from_template("""
You are a support agent. Generate a concise, professional response to the customer based on the ticket and context. Ensure the response:
1. Starts with a polite, personal greeting (e.g., 'Hello [Customer]').
2. Addresses the issue directly with clear, actionable steps from the context (e.g., refund timelines, troubleshooting).
3. Ends with a professional closing (e.g., 'Best regards, Support Team').
4. Is concise, under 300 words, avoiding repetition or unnecessary details.
5. Avoids placeholders like '[Customer]' and uses 'Customer' or a generic term.

Ticket Subject: {subject}
Ticket Description: {description}
Category: {category}
Context: {context}

Response:
""")

# Review prompt
review_prompt = PromptTemplate.from_template("""
You are a senior support agent. Review the draft response for:
1. Relevance: Does it address the ticket's issue and match the category?
2. Completeness: Does it include actionable steps (e.g., refund timeline, troubleshooting) and a closing?
3. Professionalism: Is the tone polite, professional, and includes a personal greeting?

Return 'Approved' if the draft is relevant, mostly complete (minor issues like slight verbosity are acceptable), and professional.
Return 'Escalate' only if the draft is irrelevant, significantly incomplete (e.g., missing key steps or closing), or unprofessional.

If escalating, provide specific, concise feedback on what to improve (e.g., 'Add a closing', 'Include refund timeline', 'Simplify instructions').

Ticket Subject: {subject}
Ticket Description: {description}
Category: {category}
Context: {context}
Draft Response: {draft}

Response: [Approved or Escalate]
Feedback (if Escalate): [specific feedback]
""")

# Feedback prompt
feedback_prompt = PromptTemplate.from_template("""
You are a senior support agent. The draft response was rejected. Provide concise, specific feedback on why the draft is not suitable (e.g., irrelevant, missing key steps, unprofessional) and suggest improvements (e.g., 'Add refund timeline', 'Include a closing').

Ticket Subject: {subject}
Ticket Description: {description}
Category: {category}
Context: {context}
Draft Response: {draft}

Feedback:
""")