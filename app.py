import gradio as gr
from router import explain_llm, translate_llm, summarize_llm, router, evaluator_llm


def generate_solution(task, user_input, feedback=None):
    if feedback:
        user_input = f"{user_input}\n[Evaluator feedback: {feedback}]"
    if "explain" in task:
        return explain_llm(user_input)
    elif "translate" in task:
        return translate_llm(user_input)
    elif "summarize" in task:
        return summarize_llm(user_input)
    else:
        return "Sorry, your request doesn't fit our supported tasks (Explain, Translate, Summarize). Please rephrase your request."


def process_request(user_input):
    """Process user request through the LLM router system"""
    if not user_input.strip():
        return "Please enter a request.", "", ""

    task = router(user_input)
    max_attempts = 3
    feedback = None

    attempt_logs = []

    for attempt in range(max_attempts):
        solution = generate_solution(task, user_input, feedback)

        if task == "none":
            return solution, f"Task: {task.capitalize()}", "Completed in 1 attempt"

        evaluation = evaluator_llm(task, user_input, solution)

        if evaluation.is_relevant == "yes":
            attempt_logs.append(f"✅ Attempt {attempt + 1}: Accepted")
            return solution, f"Task: {task.capitalize()}", "\n".join(attempt_logs)
        else:
            attempt_logs.append(
                f"❌ Attempt {attempt + 1}: Rejected - {evaluation.feedback}"
            )
            feedback = evaluation.feedback

    return (
        solution,
        f"Task: {task.capitalize()}",
        "\n".join(attempt_logs) + "\n⚠️ Max attempts reached",
    )


# Create Gradio interface
with gr.Blocks(title="LLM Router with DSPy", theme=gr.themes.Soft()) as demo:
    gr.Markdown(
        """
        # 🚀 LLM Router with DSPy
        
        An intelligent routing system that automatically classifies your requests and routes them to specialized handlers:
        - **Explain**: Get clear explanations of concepts and topics
        - **Translate**: Translate English text to German
        - **Summarize**: Create concise summaries of text
        
        The system uses DSPy framework for structured LLM programming and includes an evaluation loop for quality assurance.
        """
    )

    with gr.Row():
        with gr.Column(scale=2):
            user_input = gr.Textbox(
                label="Your Request",
                placeholder="e.g., 'Explain quantum computing' or 'Translate: Hello world' or 'Summarize: [your text]'",
                lines=3,
            )
            submit_btn = gr.Button("Submit", variant="primary")

        with gr.Column(scale=1):
            task_output = gr.Textbox(label="Detected Task", interactive=False)
            process_log = gr.Textbox(label="Process Log", interactive=False, lines=4)

    response_output = gr.Textbox(label="Response", lines=8, interactive=False)

    # Example inputs
    gr.Markdown("### 📝 Example Inputs:")
    examples = gr.Examples(
        examples=[
            ["Explain how machine learning works"],
            ["Translate: How are you doing today?"],
            [
                "Summarize: Machine learning is a method of data analysis that automates analytical model building. It is a branch of artificial intelligence based on the idea that systems can learn from data, identify patterns and make decisions with minimal human intervention."
            ],
            ["What's the weather like today?"],  # This should be routed to "None"
        ],
        inputs=[user_input],
    )

    submit_btn.click(
        fn=process_request,
        inputs=[user_input],
        outputs=[response_output, task_output, process_log],
    )

    user_input.submit(
        fn=process_request,
        inputs=[user_input],
        outputs=[response_output, task_output, process_log],
    )

if __name__ == "__main__":
    demo.launch(share=True)
