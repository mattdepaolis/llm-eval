#!/usr/bin/env python3
"""
Basic Usage Example for llm-eval Package

This example demonstrates how to use the llm-eval package for evaluating language models.
"""

def main():
    print("🚀 LLM-Eval Basic Usage Example")
    print("=" * 50)
    
    # Example 1: Package information
    print("\n📦 Example 1: Package Information")
    try:
        import llm_eval
        info = llm_eval.get_package_info()
        print(f"Package: {info['name']} v{info['version']}")
        print(f"Author: {info['author']}")
        print(f"URL: {info['url']}")
        print(f"Description: {info['description']}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Example 2: CLI Usage Demo
    print("\n🖥️ Example 2: CLI Usage Examples")
    print("You can run evaluations using the command line:")
    print("  llm-eval --model hf --model_name microsoft/DialoGPT-small --tasks arc_easy --limit 10")
    print("  llm-eval-demo --latest")
    print("  llm-eval-showcase")
    
    # Example 3: Available CLI Commands
    print("\n📋 Example 3: Available CLI Commands")
    try:
        import subprocess
        
        commands = [
            ("llm-eval", "Main evaluation command"),
            ("llm-eval-demo", "Demo command for report generation"),
            ("llm-eval-html", "HTML report generation"),
            ("llm-eval-showcase", "Showcase command")
        ]
        
        for cmd, desc in commands:
            result = subprocess.run(["which", cmd], capture_output=True, text=True)
            if result.returncode == 0:
                print(f"✅ {cmd}: {desc}")
            else:
                print(f"❌ {cmd}: Not found")
                
    except Exception as e:
        print(f"❌ Error checking commands: {e}")
    
    # Example 4: Direct imports
    print("\n🐍 Example 4: Direct Python Imports")
    try:
        from llm_eval.evaluation import evaluator
        from llm_eval.reporting import report_generator
        from llm_eval.tasks import task_config
        
        print("✅ Successfully imported core modules:")
        print("  - llm_eval.evaluation.evaluator")
        print("  - llm_eval.reporting.report_generator") 
        print("  - llm_eval.tasks.task_config")
        
        # Show available tasks
        print(f"\n📋 Available task groups: {len(task_config.TASK_NAME_MAPPING)}")
        for group in list(task_config.TASK_NAME_MAPPING.keys())[:5]:
            print(f"  - {group}")
        if len(task_config.TASK_NAME_MAPPING) > 5:
            print(f"  ... and {len(task_config.TASK_NAME_MAPPING) - 5} more")
            
    except Exception as e:
        print(f"❌ Error importing modules: {e}")

if __name__ == "__main__":
    main() 