# LLM Router Evaluator

An intelligent LLM-based router system that automatically classifies user requests and routes them to appropriate task handlers (Explain, Translate, Summarize) with built-in evaluation and feedback loops.

## Features

- **Smart Routing**: Uses DSPy to automatically classify user requests into supported tasks
- **Multiple Task Support**: 
  - **Explain**: Provides clear explanations for concepts and topics
  - **Translate**: Translates English text to German
  - **Summarize**: Creates concise summaries of text
- **Intelligent Evaluation**: Built-in evaluator assesses response quality and provides feedback
- **Iterative Improvement**: Up to 3 attempts with feedback-driven refinement
- **Robust Error Handling**: Gracefully handles requests that don't fit supported categories

## Technology Stack

- **DSPy**: Modern framework for LLM programming with structured prompts
- **Anthropic Claude**: High-quality language model via LiteLLM integration
- **Pydantic**: Data validation and structured outputs
- **Python 3.11+**: Modern Python with type hints

## Setup

1. **Install Dependencies**:
   ```bash
   pip install dspy-ai anthropic pydantic python-dotenv
   ```

2. **Environment Configuration**:
   Create a `.env` file with your Anthropic API key:
   ```bash
   ANTHROPIC_API_KEY=your_api_key_here
   ```

3. **Run the Application**:
   ```bash
   python main.py
   # or
   uv run main.py
   ```

## Usage Examples

### Explanation Request
```
Input: "Please explain quantum computing"
Output: Detailed explanation of quantum computing concepts
```

### Translation Request
```
Input: "Translate: How are you today?"
Output: German translation of the text
```

### Summarization Request
```
Input: "Summarize this text: [long text content]"
Output: Concise summary preserving key information
```

### Invalid Request Handling
```
Input: "How are you doing today?"
Output: "Sorry, your request doesn't fit our supported tasks (Explain, Translate, Summarize). Please rephrase your request."
```

## Architecture

### DSPy Integration
The system leverages DSPy's structured approach to LLM programming:

- **Signatures**: Define input/output schemas for each task
- **Modules**: Encapsulate LLM functionality with clear interfaces  
- **Automatic Prompt Generation**: DSPy handles prompt engineering internally

### Core Components

1. **TaskRouter**: Classifies requests into Explain/Translate/Summarize/None
2. **Task Modules**: Specialized handlers for each supported task type
3. **EvaluateTask**: Assesses response quality and task completion accuracy
4. **Feedback Loop**: Iterative improvement based on evaluator feedback

### Evaluation System
- Validates that responses actually perform the requested task
- Provides detailed feedback for improvement
- Supports up to 3 refinement attempts
- Uses Pydantic models for structured evaluation results

## Project Structure

```
├── main.py              # Main application with DSPy implementation
├── .env                 # Environment variables (API keys)
├── CLAUDE.md           # Development guidance
└── README.md           # This file
```

## Development

The project uses DSPy's declarative approach, eliminating manual prompt engineering:

- **Before**: Manual prompt strings and response parsing
- **After**: Structured signatures with automatic prompt generation
- **Benefits**: More maintainable, robust, and easier to extend

## Requirements

- Python 3.11+
- Anthropic API key
- Dependencies listed in requirements or installed via pip
