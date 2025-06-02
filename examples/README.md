# Examples

This directory contains examples demonstrating how to use the `llm-eval` package.

## Files

- `basic_usage.py` - Basic usage examples showing evaluation and HTML report generation

## Running Examples

Make sure you have the package installed:

```bash
pip install llm-eval
```

Then run the examples:

```bash
python examples/basic_usage.py
```

## CLI Usage Examples

```bash
# Basic evaluation
llm-eval --model hf --model_name microsoft/DialoGPT-small --tasks arc_easy --limit 10

# Generate HTML report from existing results
llm-eval-demo --latest

# Showcase the framework
llm-eval-showcase
``` 