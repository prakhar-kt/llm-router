import dspy
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()

# Configure DSPy with Anthropic via LiteLLM
lm = dspy.LM(model="anthropic/claude-3-5-sonnet-20241022")
dspy.settings.configure(lm=lm)


class EvaluationResult(BaseModel):
    is_relevant: str
    feedback: str


class TaskRouter(dspy.Signature):
    """Route user input to appropriate task: Explain, Translate, Summarize, or None"""
    user_input = dspy.InputField(desc="User's request")
    task = dspy.OutputField(desc="Exactly one word: Explain (for explanations of concepts), Translate (for translation requests), Summarize (for summarization requests), or None (if it doesn't fit any category)")

def router(user_input: str) -> str:
    router_module = dspy.Predict(TaskRouter)
    result = router_module(user_input=user_input)
    return result.task.strip().lower()


class ExplainTask(dspy.Signature):
    """Provide clear explanations for concepts, topics, or questions"""
    user_input = dspy.InputField(desc="What the user wants explained")
    explanation = dspy.OutputField(desc="Clear, helpful explanation")

def explain_llm(user_input: str) -> str:
    explain_module = dspy.Predict(ExplainTask)
    result = explain_module(user_input=user_input)
    return result.explanation.lower()


class TranslateTask(dspy.Signature):
    """Translate English text to German"""
    user_input = dspy.InputField(desc="English text to translate")
    translation = dspy.OutputField(desc="German translation")

def translate_llm(user_input: str) -> str:
    translate_module = dspy.Predict(TranslateTask)
    result = translate_module(user_input=user_input)
    return result.translation.lower()


class SummarizeTask(dspy.Signature):
    """Summarize text concisely while preserving key information"""
    user_input = dspy.InputField(desc="Text to summarize")
    summary = dspy.OutputField(desc="Concise summary")

def summarize_llm(user_input: str) -> str:
    summarize_module = dspy.Predict(SummarizeTask)
    result = summarize_module(user_input=user_input)
    return result.summary


class EvaluateTask(dspy.Signature):
    """Evaluate if a solution correctly performs the requested task and is helpful"""
    task = dspy.InputField(desc="The task type (explain, translate, summarize)")
    user_input = dspy.InputField(desc="Original user request")
    solution = dspy.InputField(desc="Generated solution to evaluate")
    is_relevant = dspy.OutputField(desc="yes or no - whether solution actually performs the requested task correctly")
    feedback = dspy.OutputField(desc="Detailed feedback focusing on task completion accuracy")

def evaluator_llm(task: str, user_input: str, solution: str) -> EvaluationResult:
    evaluator_module = dspy.Predict(EvaluateTask)
    result = evaluator_module(task=task, user_input=user_input, solution=solution)
    
    return EvaluationResult(
        is_relevant=result.is_relevant.strip().lower(),
        feedback=result.feedback.strip()
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
    
