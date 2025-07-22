from router import (
    explain_llm, 
    translate_llm, 
    summarize_llm,
    router, 
    evaluator_llm
)


def generate_solution(task, user_input, feedback=None):
    """_summary_
    Calls the appropiate generator LLM, optionally with feedback.
    Args:
        task (_type_): _description_
        user_input (_type_): _description_
        feedback (_type_, optional): _description_. Defaults to None.

    """

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


def main():
    user_input = input("Enter your request: ")
    task = router(user_input)
    # print(f"DEBUG: Router classified as: {task}")
    max_attempts = 3
    feedback = None

    for attempt in range(max_attempts):
        solution = generate_solution(task, user_input, feedback)
        evaluation = evaluator_llm(task, user_input, solution)
        # print(f"DEBUG: Evaluation - Relevant: {evaluation.is_relevant}, Feedback: {evaluation.feedback}")
        if evaluation.is_relevant == "yes":
            print(f"Result accepted on attempt {attempt + 1}:\n{solution}")
            break
        else:
            print(f"Attempt {attempt +1} rejected. Feedback: {evaluation.feedback}")
            feedback = evaluation.feedback


if __name__ == "__main__":
    main()
    
