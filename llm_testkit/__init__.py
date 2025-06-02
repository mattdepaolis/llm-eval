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

__version__ = "1.0.9"
__author__ = "Matthias De Paolis"
__email__ = "mattdepaolis@users.noreply.github.com"
__license__ = "MIT"
__url__ = "https://github.com/mattdepaolis/llm-eval"

# GPU detection and PyTorch installation helper
def check_gpu_compatibility():
    """
    Check GPU compatibility and provide PyTorch installation recommendations.
    
    Returns:
        dict: GPU information and installation recommendations
    """
    try:
        import subprocess
        import re
        
        # Try to get GPU information using nvidia-smi
        try:
            result = subprocess.run(['nvidia-smi', '--query-gpu=name,compute_cap', '--format=csv,noheader,nounits'], 
                                  capture_output=True, text=True, timeout=10)
            
            if result.returncode == 0:
                gpu_info = []
                for line in result.stdout.strip().split('\n'):
                    if line.strip():
                        parts = line.split(',')
                        if len(parts) >= 2:
                            name = parts[0].strip()
                            compute_cap = parts[1].strip()
                            gpu_info.append({'name': name, 'compute_cap': compute_cap})
                
                # Always use CUDA 12.8 for best performance and compatibility
                return {
                    'gpus_detected': gpu_info,
                    'needs_cuda128': True,  # Always true now
                    'installation_command': 'pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu128',
                    'recommendation': f'GPU detected: {gpu_info[0]["name"]}. Using CUDA 12.8 for optimal performance.' if gpu_info else 'Using CUDA 12.8 for optimal performance.'
                }
            
        except (subprocess.TimeoutExpired, FileNotFoundError):
            pass
            
    except ImportError:
        pass
    
    # Default to CUDA 12.8 even if GPU detection fails
    return {
        'gpus_detected': [],
        'needs_cuda128': True,  # Always true now
        'installation_command': 'pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu128',
        'recommendation': 'Could not detect GPU. Using CUDA 12.8 for optimal performance.'
    }

def install_pytorch_for_gpu():
    """
    Automatically install PyTorch with CUDA 12.8 support for optimal performance.
    
    This function installs PyTorch with CUDA 12.8 which provides the best performance
    and is compatible with all modern NVIDIA GPUs (RTX 20 series and newer).
    """
    import subprocess
    import sys
    
    gpu_info = check_gpu_compatibility()
    
    print("🔍 GPU Detection Results:")
    if gpu_info['gpus_detected']:
        for gpu in gpu_info['gpus_detected']:
            print(f"   GPU: {gpu['name']} (Compute {gpu['compute_cap']})")
    else:
        print("   No NVIDIA GPUs detected or nvidia-smi not available")
    
    print(f"\n💡 Recommendation: {gpu_info['recommendation']}")
    print(f"📦 Installation command: {gpu_info['installation_command']}")
    print("\n🚀 CUDA 12.8 provides optimal performance and compatibility for all modern GPUs!")
    
    # Ask user if they want to proceed
    try:
        response = input("\n🚀 Install PyTorch with CUDA 12.8? [y/N]: ").lower().strip()
        if response in ['y', 'yes']:
            print("📦 Installing PyTorch with CUDA 12.8...")
            
            # Uninstall existing torch first
            print("🧹 Removing existing PyTorch installation...")
            subprocess.run([sys.executable, '-m', 'pip', 'uninstall', 'torch', 'torchvision', 'torchaudio', '-y'], 
                         capture_output=True)
            
            # Always install CUDA 12.8 version
            cmd = [sys.executable, '-m', 'pip', 'install', 'torch', 'torchvision', 'torchaudio', 
                   '--index-url', 'https://download.pytorch.org/whl/cu128']
            
            print("📦 Installing PyTorch with CUDA 12.8...")
            result = subprocess.run(cmd)
            
            if result.returncode == 0:
                print("✅ PyTorch with CUDA 12.8 installation completed successfully!")
                
                # Verify installation
                try:
                    import torch
                    print(f"🎯 PyTorch version: {torch.__version__}")
                    if torch.cuda.is_available():
                        print(f"🚀 CUDA available: {torch.cuda.get_device_name(0)}")
                        print(f"🔥 CUDA version: {torch.version.cuda}")
                    else:
                        print("💻 CUDA not available - using CPU")
                except Exception as e:
                    print(f"⚠️  Could not verify PyTorch installation: {e}")
            else:
                print("❌ PyTorch installation failed")
        else:
            print("⏭️  Skipping automatic installation")
            print(f"💡 Manual installation: {gpu_info['installation_command']}")
            
    except KeyboardInterrupt:
        print("\n⏹️  Installation cancelled")
    except Exception as e:
        print(f"❌ Error during installation: {e}")

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
    
    # GPU compatibility helpers
    "check_gpu_compatibility",
    "install_pytorch_for_gpu",
    
    # Metadata
    "__version__",
    "__author__",
    "__email__",
    "__license__",
    "__url__",
]

# Convenience imports for common workflows
def quick_eval(model_name: str, tasks: str = "arc_easy", model_type: str = "hf", limit: int = None, **kwargs):
    """
    Quick evaluation function for common use cases.
    
    Args:
        model_name: Name or path of the model to evaluate
        tasks: Comma-separated list of tasks to run
        model_type: Model backend to use ('hf' for HuggingFace, 'vllm' for vLLM)
        limit: Maximum number of samples per task (optional)
        **kwargs: Additional arguments passed to the evaluator
        
    Returns:
        Dictionary containing evaluation results
        
    Example:
        >>> import llm_testkit
        >>> results = llm_testkit.quick_eval("microsoft/DialoGPT-small", "arc_easy", limit=100)
    """
    from .evaluation.evaluator import evaluate_model
    
    # Convert limit to num_samples if provided
    if limit is not None:
        kwargs['num_samples'] = limit
    
    results, _ = evaluate_model(
        model_type=model_type,
        model_name=model_name,
        tasks=tasks.split(",") if isinstance(tasks, str) else tasks,
        **kwargs
    )
    return results

def quick_html_report(model_name: str, tasks: str = "arc_easy", model_type: str = "hf", limit: int = None, output_dir: str = "reports", **kwargs):
    """
    Quick evaluation with HTML report generation.
    
    Args:
        model_name: Name or path of the model to evaluate
        tasks: Comma-separated list of tasks to run
        model_type: Model backend to use ('hf' for HuggingFace, 'vllm' for vLLM)
        limit: Maximum number of samples per task (optional)
        output_dir: Directory to save the HTML report
        **kwargs: Additional arguments passed to the evaluator
        
    Returns:
        Tuple of (results_dict, html_report_path)
        
    Example:
        >>> import llm_testkit
        >>> results, report_path = llm_testkit.quick_html_report("microsoft/DialoGPT-small", limit=100)
        >>> print(f"Report saved to: {report_path}")
    """
    import os
    from .evaluation.evaluator import evaluate_model
    from .reporting.html_report_generator import generate_html_report
    
    # Convert limit to num_samples if provided
    if limit is not None:
        kwargs['num_samples'] = limit
    
    # Run evaluation - properly unpack the tuple
    results, eval_output_path = evaluate_model(
        model_type=model_type,
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
