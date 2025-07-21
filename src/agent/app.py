import gradio as gr
from agent.graph import graph
from agent.state import State
from langchain_core.messages import HumanMessage

def process_ticket(subject: str, description: str) -> str:
    """Process a support ticket through the agent workflow and return formatted output.

    Args:
        subject (str): Ticket subject (max 100 characters).
        description (str): Ticket description (max 500 characters).

    Returns:
        str: Formatted output (approved draft or escalation message).
    """
    # Validate inputs
    if not subject or not description:
        return "Error: Please provide both subject and description."
    if len(subject) > 100:
        return "Error: Subject must be 100 characters or less."
    if len(description) > 500:
        return "Error: Description must be 500 characters or less."

    # Initialize state
    ticket = {"subject": subject, "description": description}
    initial_state = {
        "ticket": ticket,
        "messages": [HumanMessage(content=f"Received ticket: {subject}")],
        "attempt": 0,
        "drafts": [],
        "feedbacks": []
    }

    # Run the agent
    try:
        result = graph.invoke(initial_state)
        output = result.get("output", "No output generated.")
        category = result.get("category", "Unknown")
        approved = result.get("approved", False)
        feedback = result.get("feedback", None)

        # Format response
        response = f"**Category**: {category}\n\n**Output**:\n{output}"
        if not approved and feedback:
            response += f"\n\n**Feedback**: {feedback}"
        return response
    except Exception as e:
        return f"Error processing ticket: {str(e)}"

# Define Gradio interface
with gr.Blocks(title="Support Ticket Resolution Agent") as app:
    gr.Markdown("# Support Ticket Resolution Agent")
    gr.Markdown("Enter a support ticket (Subject: max 100 chars, Description: max 500 chars).")
    
    with gr.Row():
        subject_input = gr.Textbox(
            label="Subject",
            placeholder="e.g., I was charged twice",
            max_lines=1,
            interactive=True
        )
        description_input = gr.Textbox(
            label="Description",
            placeholder="e.g., I noticed two charges on my card...",
            lines=4,
            interactive=True
        )
    
    submit_button = gr.Button("Submit Ticket")
    output = gr.Markdown(label="Response", value="Submit a ticket to see the response.")
    
    # Add loader feedback
    def submit_with_loader(subject, description):
        # Show loading message
        yield "**Processing your ticket...**"
        # Process ticket
        result = process_ticket(subject, description)
        # Return final result
        yield result

    submit_button.click(
        fn=submit_with_loader,
        inputs=[subject_input, description_input],
        outputs=output,
        queue=True  # Enable queue for loading state
    )

if __name__ == "__main__":
    app.launch(server_name="0.0.0.0", server_port=7860)