import dspy
from dotenv import load_dotenv


load_dotenv()

# Configure DSPy with Anthropic via LiteLLM
lm = dspy.LM(model="anthropic/claude-3-5-sonnet-20241022")
dspy.settings.configure(lm=lm)


class EvaluateTask(dspy.Signature):
    """Evaluate if a solution correctly performs the requested task and is helpful"""

    task = dspy.InputField(desc="The task type (explain, translate, summarize)")
    user_input = dspy.InputField(desc="Original user request")
    solution = dspy.InputField(desc="Generated solution to evaluate")
    is_relevant = dspy.OutputField(
        desc="yes or no - whether solution actually performs the requested task correctly"
    )
    feedback = dspy.OutputField(
        desc="Detailed feedback focusing on task completion accuracy"
    )


def evaluator_llm(task: str, user_input: str, solution: str):
    evaluator_module = dspy.Predict(EvaluateTask)
    result = evaluator_module(task=task, user_input=user_input, solution=solution)
    return result


class TaskRouter(dspy.Signature):
    """Route user input to appropriate task: Explain, Translate, Summarize, or None"""

    user_input = dspy.InputField(desc="User's request")
    task = dspy.OutputField(
        desc="Exactly one word: Explain (for explanations of concepts), Translate (for translation requests), Summarize (for summarization requests), or None (if it doesn't fit any category)"
    )


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
    return result.explanation


class TranslateTask(dspy.Signature):
    """Translate English text to German"""

    user_input = dspy.InputField(desc="English text to translate")
    translation = dspy.OutputField(desc="German translation")


def translate_llm(user_input: str) -> str:
    translate_module = dspy.Predict(TranslateTask)
    result = translate_module(user_input=user_input)
    return result.translation


class SummarizeTask(dspy.Signature):
    """Summarize text concisely while preserving key information"""

    user_input = dspy.InputField(desc="Text to summarize")
    summary = dspy.OutputField(desc="Concise summary")


def summarize_llm(user_input: str) -> str:
    summarize_module = dspy.Predict(SummarizeTask)
    result = summarize_module(user_input=user_input)
    return result.summary
