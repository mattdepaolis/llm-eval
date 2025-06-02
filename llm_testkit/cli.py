#!/usr/bin/env python3
"""
Command-line interface for Professional LLM Evaluation Framework

This module provides command-line entry points for the evaluation framework,
including evaluation, reporting, and demonstration functionality.
"""

import argparse
import sys
import os
from typing import List, Optional

def main():
    """Main CLI entry point for llm-eval command."""
    parser = argparse.ArgumentParser(
        prog="llm-eval",
        description="Professional LLM Evaluation Framework with Beautiful HTML Reports",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Basic evaluation
  llm-eval --model hf --model_name microsoft/DialoGPT-small --tasks arc_easy
  
  # Evaluation with professional HTML reports
  llm-eval --model hf --model_name microsoft/DialoGPT-small --tasks arc_easy --report_format professional
  
  # Multiple tasks evaluation
  llm-eval --model hf --model_name microsoft/DialoGPT-small --tasks arc_easy,hellaswag
  
  # GPU evaluation with specific device
  llm-eval --model hf --model_name microsoft/DialoGPT-small --tasks arc_easy --device cuda:0
  
For more information, visit: https://github.com/mattdepaolis/llm-eval
        """
    )
    
    # Model configuration
    model_group = parser.add_argument_group("Model Configuration")
    model_group.add_argument("--model", required=True, 
                           choices=["hf", "openai", "anthropic", "local"],
                           help="Model backend to use")
    model_group.add_argument("--model_name", required=True,
                           help="Model name or path")
    model_group.add_argument("--model_args", 
                           help="Additional model arguments (comma-separated)")
    
    # Task configuration
    task_group = parser.add_argument_group("Task Configuration")
    task_group.add_argument("--tasks", required=True,
                          help="Tasks to evaluate (comma-separated)")
    task_group.add_argument("--num_fewshot", type=int, default=0,
                          help="Number of few-shot examples")
    task_group.add_argument("--limit", type=int,
                          help="Limit number of examples per task")
    
    # Evaluation settings
    eval_group = parser.add_argument_group("Evaluation Settings")
    eval_group.add_argument("--batch_size", type=int, default=1,
                          help="Batch size for evaluation")
    eval_group.add_argument("--device", default="auto",
                          help="Device to use (auto, cuda, cpu, cuda:0, etc.)")
    eval_group.add_argument("--no_cache", action="store_true",
                          help="Disable caching")
    
    # Generation settings
    gen_group = parser.add_argument_group("Generation Settings")
    gen_group.add_argument("--temperature", type=float, default=0.0,
                         help="Sampling temperature")
    gen_group.add_argument("--top_p", type=float, default=1.0,
                         help="Top-p sampling parameter")
    gen_group.add_argument("--max_length", type=int, default=2048,
                         help="Maximum generation length")
    
    # Reporting options
    report_group = parser.add_argument_group("Reporting Options")
    report_group.add_argument("--report_format", 
                            choices=["standard", "professional", "both"],
                            default="professional",
                            help="Report format to generate")
    report_group.add_argument("--output_dir", default="results",
                            help="Output directory for results and reports")
    report_group.add_argument("--output_base_path",
                            help="Base path for output files")
    
    # Advanced options
    advanced_group = parser.add_argument_group("Advanced Options")
    advanced_group.add_argument("--verbosity", choices=["DEBUG", "INFO", "WARNING", "ERROR"],
                              default="INFO", help="Logging verbosity")
    advanced_group.add_argument("--seed", type=int, default=42,
                              help="Random seed for reproducibility")
    advanced_group.add_argument("--trust_remote_code", action="store_true",
                              help="Trust remote code when loading models")
    
    args = parser.parse_args()
    
    # Import and run the evaluation function directly
    try:
        from .evaluation.evaluator import evaluate_model
        from .tasks.task_config import TASK_NAME_MAPPING, BBH_SUBTASKS
        from .utils.gpu import get_available_gpus
        from .reporting.report_generator import get_results_dir
        from datetime import datetime
        import os
        
        # Process tasks - handle comma-separated task names
        tasks_input = args.tasks.split(',') if ',' in args.tasks else [args.tasks]
        valid_tasks = []
        
        # Build list of all available individual tasks
        all_available_tasks = []
        for group, tasks in TASK_NAME_MAPPING.items():
            all_available_tasks.extend(tasks)
        
        # Add BBH subtasks
        for subtask in BBH_SUBTASKS.keys():
            all_available_tasks.append(f"bbh_{subtask}")
        
        for task in tasks_input:
            task = task.strip()
            # Check if task is a task group name
            if task.upper() in TASK_NAME_MAPPING:
                # Add all tasks in the group
                group_tasks = TASK_NAME_MAPPING[task.upper()]
                print(f"Expanding task group '{task.upper()}' to {len(group_tasks)} individual tasks")
                valid_tasks.extend(group_tasks)
            # Check if task is an individual task name
            elif task in all_available_tasks:
                valid_tasks.append(task)
            else:
                print(f"Warning: Unknown task '{task}'. Available tasks: {', '.join(sorted(all_available_tasks[:10]))}...")
                valid_tasks.append(task)  # Still try to run it in case it's a valid lm-eval task
        
        if not valid_tasks:
            print("No valid tasks specified.")
            sys.exit(1)
        
        # Generate output path
        if not args.output_base_path:
            model_name_short = args.model_name.split('/')[-1]
            tasks_str = '_'.join(valid_tasks[:3])  # Use first 3 tasks
            if len(valid_tasks) > 3:
                tasks_str += f"_and_{len(valid_tasks)-3}_more"
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"results_{model_name_short}_{args.model}_{tasks_str}_{timestamp}.json"
            results_dir = get_results_dir()
            output_path = os.path.join(results_dir, filename)
        else:
            output_path = args.output_base_path
        
        print(f"🚀 Starting evaluation...")
        print(f"📊 Output path: {output_path}")
        
        # Run evaluation
        results, final_output_path = evaluate_model(
            model_type=args.model,
            model_name=args.model_name,
            tasks=valid_tasks,
            num_fewshot=args.num_fewshot,
            batch_size=args.batch_size,
            device=args.device,
            output_path=output_path,
            num_samples=args.limit,
            generate_report=True,
            quantize=False,  # Simplified for now
            quantization_method=None,
            dtype=None,
            max_model_len=None,
            tensor_parallel_size=1,
            gpu_memory_utilization=0.9,
            vllm_quantization=None,
            additional_model_args=args.model_args,
            preserve_default_fewshot=False,
            report_format=args.report_format
        )
        
        print("✅ Evaluation completed successfully!")
        print(f"📄 Results saved to: {final_output_path}")
        
        return 0
        
    except ImportError as e:
        print(f"Error importing evaluation module: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Error during evaluation: {e}")
        sys.exit(1)

def demo_main():
    """CLI entry point for llm-eval-demo command."""
    parser = argparse.ArgumentParser(
        prog="llm-eval-demo",
        description="Generate demo HTML reports from existing evaluation results",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Generate report for latest evaluation
  llm-eval-demo --latest
  
  # Generate report for specific file  
  llm-eval-demo -f results/evaluation_results.json
  
  # Generate with custom output path
  llm-eval-demo -f results/eval.json -o custom_report.html
        """
    )
    
    parser.add_argument("--latest", action="store_true",
                       help="Generate report for latest evaluation result")
    parser.add_argument("-f", "--file", 
                       help="JSON results file to generate report from")
    parser.add_argument("-o", "--output",
                       help="Output path for HTML report")
    parser.add_argument("--results_dir", default="results",
                       help="Directory to search for result files")
    
    args = parser.parse_args()
    
    try:
        # Import demo functionality
        import os
        import glob
        import json
        from .reporting.html_report_generator import generate_html_report_from_json
        
        if args.latest:
            # Find latest result file
            pattern = os.path.join(args.results_dir, "*.json")
            files = glob.glob(pattern)
            if not files:
                print(f"No result files found in {args.results_dir}")
                sys.exit(1)
            
            latest_file = max(files, key=os.path.getmtime)
            print(f"📊 Found latest result: {latest_file}")
            result_file = latest_file
            
        elif args.file:
            result_file = args.file
            if not os.path.exists(result_file):
                print(f"File not found: {result_file}")
                sys.exit(1)
        else:
            print("Please specify --latest or --file option")
            sys.exit(1)
        
        # Generate HTML report
        print(f"📊 Generating HTML report from: {result_file}")
        html_path = generate_html_report_from_json(result_file, args.output)
        
        print("✨ HTML report generated successfully!")
        print(f"🌐 Report location: {html_path}")
        
        # Show file size
        file_size = os.path.getsize(html_path) / 1024
        print(f"📏 File size: {file_size:.1f} KB")
        
        print(f"\n🚀 To view the report, open in your browser:")
        print(f"   file://{os.path.abspath(html_path)}")
        
    except Exception as e:
        print(f"Error generating demo report: {e}")
        sys.exit(1)

def html_main():
    """CLI entry point for llm-eval-html command."""
    parser = argparse.ArgumentParser(
        prog="llm-eval-html",
        description="Generate HTML reports from evaluation results",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument("input_file", 
                       help="JSON results file to generate report from")
    parser.add_argument("-o", "--output",
                       help="Output path for HTML report") 
    parser.add_argument("--template", 
                       choices=["professional", "minimal"],
                       default="professional",
                       help="Report template to use")
    
    args = parser.parse_args()
    
    try:
        from .reporting.html_report_generator import generate_html_report_from_json
        
        if not os.path.exists(args.input_file):
            print(f"Input file not found: {args.input_file}")
            sys.exit(1)
        
        print(f"📊 Generating HTML report from: {args.input_file}")
        html_path = generate_html_report_from_json(args.input_file, args.output)
        
        print("✨ HTML report generated successfully!")
        print(f"🌐 Report location: {html_path}")
        
    except Exception as e:
        print(f"Error generating HTML report: {e}")
        sys.exit(1)

def showcase_main():
    """CLI entry point for llm-eval-showcase command."""
    parser = argparse.ArgumentParser(
        prog="llm-eval-showcase",
        description="Showcase the professional HTML reporting capabilities",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument("--reports_dir", default="reports",
                       help="Directory containing HTML reports to showcase")
    
    args = parser.parse_args()
    
    try:
        # Import showcase functionality
        from .showcase import showcase_html_reports
        showcase_html_reports(args.reports_dir)
        
    except ImportError:
        # Fallback to basic showcase
        print("🎯 Professional LLM Evaluation Framework")
        print("=" * 60)
        print("💎 ENHANCED WITH BEAUTIFUL HTML REPORTS")
        print("=" * 60)
        print("\n🌟 Your LLM evaluation tool is now COMMERCIAL-READY!")
        print("\n✨ Features:")
        print("   🎨 Beautiful, modern HTML reports")
        print("   📊 Interactive charts and visualizations")
        print("   📱 Responsive design for all devices")
        print("   💼 Business-ready presentation quality")
        print("   🏆 Performance badges and progress bars")
        print("   📋 Executive summaries with insights")
        print("\n💰 Perfect for paid evaluation services!")
        print("🎪 Ready for client demonstrations!")
        print("📈 Executive-level reporting!")
        
        if os.path.exists(args.reports_dir):
            html_files = [f for f in os.listdir(args.reports_dir) if f.endswith('.html')]
            if html_files:
                print(f"\n📁 Found {len(html_files)} HTML reports in {args.reports_dir}/")
                for file in html_files[:5]:  # Show first 5
                    print(f"   🌐 {file}")
        
    except Exception as e:
        print(f"Error in showcase: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 