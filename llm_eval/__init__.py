"""
Professional LLM Evaluation Framework

A comprehensive package for evaluating Large Language Models with beautiful HTML reports.
This framework provides professional-grade evaluation capabilities suitable for research,
development, and commercial applications.

Features:
- Beautiful, interactive HTML reports
- Comprehensive evaluation metrics
- Multiple model backends support  
- Professional presentation quality
- Easy-to-use Python API and CLI
"""

__version__ = "1.0.0"
__author__ = "Matthias De Paolis"
__email__ = "mattdepaolis@users.noreply.github.com"
__license__ = "MIT"
__url__ = "https://github.com/mattdepaolis/llm-eval"

# Core evaluation functionality
from .evaluation.evaluator import evaluate_model
from .tasks.task_config import list_available_tasks, TASK_NAME_MAPPING
from .normalization.score_normalizer import normalize_scores

# Reporting functionality
from .reporting.report_generator import generate_report
from .reporting.html_report_generator import generate_html_report, generate_html_report_from_json
from .reporting.professional_report_generator import generate_professional_report

# Main functionality
from .main import main

# Expose the leaderboard tasks
LEADERBOARD_TASKS = TASK_NAME_MAPPING['LEADERBOARD']

# Package metadata
__all__ = [
    # Core functions
    "evaluate_model",
    "main",
    
    # Task management
    "list_available_tasks", 
    "TASK_NAME_MAPPING",
    "LEADERBOARD_TASKS",
    
    # Scoring and normalization
    "normalize_scores",
    
    # Report generation
    "generate_report",
    "generate_html_report",
    "generate_html_report_from_json", 
    "generate_professional_report",
    
    # Metadata
    "__version__",
    "__author__",
    "__email__",
    "__license__",
    "__url__",
]

# Convenience imports for common workflows
def quick_eval(model_name: str, tasks: str = "arc_easy", **kwargs):
    """
    Quick evaluation function for common use cases.
    
    Args:
        model_name: Name or path of the model to evaluate
        tasks: Comma-separated list of tasks to run
        **kwargs: Additional arguments passed to the evaluator
        
    Returns:
        Dictionary containing evaluation results
        
    Example:
        >>> import llm_eval
        >>> results = llm_eval.quick_eval("microsoft/DialoGPT-small", "arc_easy")
    """
    from .evaluation.evaluator import evaluate_model
    return evaluate_model(
        model_name=model_name,
        tasks=tasks.split(",") if isinstance(tasks, str) else tasks,
        **kwargs
    )

def quick_html_report(model_name: str, tasks: str = "arc_easy", output_dir: str = "reports", **kwargs):
    """
    Quick evaluation with HTML report generation.
    
    Args:
        model_name: Name or path of the model to evaluate
        tasks: Comma-separated list of tasks to run
        output_dir: Directory to save the HTML report
        **kwargs: Additional arguments passed to the evaluator
        
    Returns:
        Tuple of (results_dict, html_report_path)
        
    Example:
        >>> import llm_eval
        >>> results, report_path = llm_eval.quick_html_report("microsoft/DialoGPT-small")
        >>> print(f"Report saved to: {report_path}")
    """
    import os
    from .evaluation.evaluator import evaluate_model
    from .reporting.html_report_generator import generate_html_report
    
    # Run evaluation
    results = evaluate_model(
        model_name=model_name,
        tasks=tasks.split(",") if isinstance(tasks, str) else tasks,
        **kwargs
    )
    
    # Generate HTML report
    os.makedirs(output_dir, exist_ok=True)
    model_safe_name = model_name.replace("/", "_").replace(":", "_")
    output_path = os.path.join(output_dir, f"{model_safe_name}_evaluation_report.html")
    html_path = generate_html_report(results, output_path)
    
    return results, html_path

# Package information for introspection
def get_package_info():
    """Get comprehensive package information."""
    return {
        "name": "llm-eval",
        "version": __version__,
        "author": __author__,
        "email": __email__,
        "license": __license__,
        "url": __url__,
        "description": "Professional LLM Evaluation Framework with Beautiful HTML Reports",
        "python_requires": ">=3.8",
    }
