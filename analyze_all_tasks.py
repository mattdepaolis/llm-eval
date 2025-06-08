#!/usr/bin/env python3
"""
Comprehensive analysis of all task types in the results to ensure proper handling.
"""

import json
from collections import defaultdict

def analyze_all_tasks():
    """Analyze all task types and their data structures."""
    
    print("🔍 Comprehensive Task Analysis")
    print("=" * 60)
    
    # Load the results
    json_path = 'my_results/results_Qwen_Qwen2.5-7B-Instruct_leaderboard_20250608_140345.json'
    with open(json_path, 'r') as f:
        data = json.load(f)

    samples = data.get('samples', {})
    print(f"📊 Total task types found: {len(samples)}")
    
    # Analyze each task type
    task_analysis = {}
    
    for task_name, task_samples in samples.items():
        if not task_samples:
            continue
            
        sample = task_samples[0]  # Analyze first sample
        doc = sample.get('doc', {})
        
        # Categorize task type
        task_category = "unknown"
        if 'musr' in task_name.lower():
            task_category = "musr"
        elif 'mmlu' in task_name.lower():
            task_category = "mmlu"
        elif 'bbh' in task_name.lower():
            task_category = "bbh"
        elif 'hellaswag' in task_name.lower():
            task_category = "hellaswag"
        elif 'math' in task_name.lower():
            task_category = "math"
        elif 'gsm8k' in task_name.lower():
            task_category = "gsm8k"
        elif 'truthfulqa' in task_name.lower():
            task_category = "truthfulqa"
        elif 'ifeval' in task_name.lower():
            task_category = "ifeval"
        elif 'gpqa' in task_name.lower():
            task_category = "gpqa"
        
        # Analyze document structure
        analysis = {
            'category': task_category,
            'doc_fields': list(doc.keys()),
            'has_question': 'question' in doc,
            'has_input': 'input' in doc,
            'has_narrative': 'narrative' in doc,
            'has_choices': 'choices' in doc,
            'has_options': 'options' in doc,
            'has_endings': 'endings' in doc,
            'target': sample.get('target'),
            'target_type': type(sample.get('target')).__name__,
            'choice_format': None,
            'sample_count': len(task_samples)
        }
        
        # Analyze choice format
        if 'choices' in doc:
            choices = doc['choices']
            if isinstance(choices, str):
                analysis['choice_format'] = 'string'
                analysis['choice_sample'] = choices[:100] + '...' if len(choices) > 100 else choices
            elif isinstance(choices, list):
                analysis['choice_format'] = 'list'
                analysis['choice_sample'] = str(choices[:3]) + '...' if len(choices) > 3 else str(choices)
            elif isinstance(choices, dict):
                analysis['choice_format'] = 'dict'
                analysis['choice_sample'] = str(dict(list(choices.items())[:2]))
        elif 'options' in doc:
            options = doc['options']
            analysis['choice_format'] = f'options_{type(options).__name__}'
            analysis['choice_sample'] = str(options[:3]) + '...' if len(options) > 3 else str(options)
        elif 'endings' in doc:
            endings = doc['endings']
            analysis['choice_format'] = f'endings_{type(endings).__name__}'
            analysis['choice_sample'] = str(endings[:2]) + '...' if len(endings) > 2 else str(endings)
        
        task_analysis[task_name] = analysis
    
    # Group by category and analyze
    categories = defaultdict(list)
    for task_name, analysis in task_analysis.items():
        categories[analysis['category']].append((task_name, analysis))
    
    print(f"\n📋 Task Categories Found:")
    for category, tasks in categories.items():
        print(f"   {category.upper()}: {len(tasks)} tasks")
    
    # Detailed analysis by category
    for category, tasks in categories.items():
        print(f"\n🎯 {category.upper()} TASKS ({len(tasks)} tasks)")
        print("-" * 50)
        
        # Show representative examples
        for task_name, analysis in tasks[:3]:  # Show first 3 of each category
            print(f"\n   📌 {task_name}")
            print(f"      Doc fields: {', '.join(analysis['doc_fields'])}")
            print(f"      Question field: {'question' if analysis['has_question'] else 'input' if analysis['has_input'] else 'narrative' if analysis['has_narrative'] else 'none'}")
            print(f"      Choice format: {analysis['choice_format']}")
            if analysis.get('choice_sample'):
                print(f"      Choice sample: {analysis['choice_sample']}")
            print(f"      Target: {analysis['target']} ({analysis['target_type']})")
            print(f"      Samples: {analysis['sample_count']}")
        
        if len(tasks) > 3:
            print(f"   ... and {len(tasks) - 3} more {category} tasks")
    
    # Identify potential issues
    print(f"\n⚠️  POTENTIAL ISSUES:")
    issues_found = False
    
    for task_name, analysis in task_analysis.items():
        issues = []
        
        # Check for missing question/context
        if not any([analysis['has_question'], analysis['has_input'], analysis['has_narrative']]):
            issues.append("No question/context field found")
        
        # Check for missing choices
        if not any([analysis['has_choices'], analysis['has_options'], analysis['has_endings']]):
            issues.append("No choice field found")
        
        # Check for unknown format
        if analysis['choice_format'] is None and any([analysis['has_choices'], analysis['has_options'], analysis['has_endings']]):
            issues.append("Unknown choice format")
        
        if issues:
            issues_found = True
            print(f"   ❌ {task_name}: {', '.join(issues)}")
    
    if not issues_found:
        print("   ✅ No issues found - all tasks have proper structure")
    
    return task_analysis

if __name__ == "__main__":
    analyze_all_tasks() 