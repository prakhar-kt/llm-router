# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is an LLM-based router that calls different functions based on user requests. The project uses Anthropic's Claude API with Pydantic for data validation.

## Development Environment

- Python virtual environment: `llm-router-venv/`
- Uses standard pip for package management (not uv with pyproject.toml)
- Python version: 3.11.5

## Essential Commands

### Environment Setup
```bash
# Activate virtual environment
source llm-router-venv/bin/activate

# Install missing dependencies
pip install python-dotenv

# Install other dependencies as needed
pip install anthropic pydantic
```

### Running the Application
```bash
# Run main application
python main.py
```

## Project Structure

- `main.py` - Main application entry point with LLM router logic
- `llm-router-venv/` - Python virtual environment
- `.env` - Environment variables (not tracked in git)

## Key Dependencies

- `anthropic` - Anthropic Claude API client
- `pydantic` - Data validation and settings management
- `python-dotenv` - Environment variable loading

## Development Notes

- This project uses traditional pip/venv setup, not modern pyproject.toml
- Dependencies are managed manually via pip install commands
- The virtual environment already has most packages but may be missing python-dotenv

## Environment Variables

The application requires environment variables to be set in a `.env` file for API keys and configuration.