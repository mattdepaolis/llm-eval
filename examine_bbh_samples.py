#!/usr/bin/env python3
"""
Examine BBH samples to test choice extraction.
"""

import json
import re

def examine_bbh_samples():
    """Examine BBH samples to understand their structure."""
    
    print("🔍 Examining BBH Samples")
    print("=" * 50)
    
    # Load the results
    json_path = 'my_results/results_Qwen_Qwen2.5-7B-Instruct_leaderboard_20250608_140345.json'
    with open(json_path, 'r') as f:
        data = json.load(f)
    
    samples = data.get('samples', {})
    
    # Get a few BBH tasks
    bbh_tasks = [name for name in samples.keys() if 'bbh' in name.lower()][:5]
    
    for task_name in bbh_tasks:
        print(f"\n📋 {task_name}")
        print("-" * 40)
        
        sample = samples[task_name][0]
        doc = sample.get('doc', {})
        input_text = doc.get('input', '')
        target = sample.get('target')
        
        print(f"Target: {target}")
        print(f"Input (first 200 chars): {input_text[:200]}...")
        
        # Test choice extraction
        from llm_testkit.reporting.html_report_generator import extract_bbh_choices_from_text
        choice_texts, choice_labels = extract_bbh_choices_from_text(input_text)
        
        if choice_texts:
            print(f"Extracted choices:")
            for label, text in zip(choice_labels, choice_texts):
                print(f"  {label}: {text[:60]}{'...' if len(text) > 60 else ''}")
        else:
            print("No choices extracted - likely direct answer task")
            # Show more of the input to understand the format
            print(f"Full input:\n{input_text}")
        
        print()

if __name__ == "__main__":
    examine_bbh_samples() 