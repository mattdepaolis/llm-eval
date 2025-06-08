#!/usr/bin/env python3
"""
Test script to validate comprehensive enhancement for all task types.
"""

import json
import llm_testkit
from collections import defaultdict

def test_comprehensive_enhancement():
    """Test the comprehensive enhancement for all task types."""
    
    print("🧪 Testing Comprehensive Enhancement for All Tasks")
    print("=" * 60)
    
    # Load the results
    json_path = 'my_results/results_Qwen_Qwen2.5-7B-Instruct_leaderboard_20250608_140345.json'
    with open(json_path, 'r') as f:
        data = json.load(f)

    samples = data.get('samples', {})
    
    # Group tasks by category
    categories = defaultdict(list)
    for task_name in samples.keys():
        if 'musr' in task_name.lower():
            categories['MUSR'].append(task_name)
        elif 'mmlu' in task_name.lower():
            categories['MMLU'].append(task_name)
        elif 'bbh' in task_name.lower():
            categories['BBH'].append(task_name)
        elif 'gpqa' in task_name.lower():
            categories['GPQA'].append(task_name)
        elif 'math' in task_name.lower():
            categories['MATH'].append(task_name)
        elif 'ifeval' in task_name.lower():
            categories['IFEVAL'].append(task_name)
        else:
            categories['OTHER'].append(task_name)
    
    print(f"📊 Task Categories:")
    for category, tasks in categories.items():
        print(f"   {category}: {len(tasks)} tasks")
    
    # Test specific examples from each category
    test_cases = []
    
    # Get one example from each category
    for category, tasks in categories.items():
        if tasks and samples.get(tasks[0]):
            sample = samples[tasks[0]][0]
            doc = sample.get('doc', {})
            test_cases.append((category, tasks[0], doc, sample))
    
    print(f"\n🔍 Analyzing Sample Structure for Each Category:")
    for category, task_name, doc, sample in test_cases:
        print(f"\n   🎯 {category} - {task_name}")
        
        # Check question/context
        question_sources = []
        if doc.get('narrative'):
            question_sources.append('narrative')
        if doc.get('Question'):  # GPQA capital Q
            question_sources.append('Question')
        if doc.get('question'):
            question_sources.append('question')
        if doc.get('input'):
            question_sources.append('input')
        if doc.get('problem'):
            question_sources.append('problem')
        if doc.get('prompt'):
            question_sources.append('prompt')
        
        print(f"      Context sources: {', '.join(question_sources) if question_sources else 'None'}")
        
        # Check choices
        choice_sources = []
        if doc.get('choices'):
            choice_sources.append(f'choices ({type(doc["choices"]).__name__})')
        if doc.get('options'):
            choice_sources.append(f'options ({type(doc["options"]).__name__})')
        if doc.get('endings'):
            choice_sources.append('endings')
        if any(f'choice{i}' in doc for i in range(1, 6)):
            choice_sources.append('choice1-4 fields')
        
        print(f"      Choice sources: {', '.join(choice_sources) if choice_sources else 'None (direct answer)'}")
        
        # Check target
        target = sample.get('target')
        print(f"      Target: {str(target)[:50]}{'...' if len(str(target)) > 50 else ''} ({type(target).__name__})")
    
    # Generate comprehensive report
    print(f"\n🎨 Generating Comprehensive Enhanced Report...")
    output_path = llm_testkit.generate_html_report_from_json(
        json_path, 
        'comprehensive_enhanced_report.html'
    )
    
    print(f"✅ Comprehensive enhanced report generated: {output_path}")
    
    print(f"\n🌟 Comprehensive Enhancement Features:")
    print(f"   📚 MUSR: Narrative + Question + Parsed choices")
    print(f"   📋 MMLU: Question + Options list")
    print(f"   🧠 BBH: Input with extracted choices from text")
    print(f"   🔬 GPQA: Question field + choice1-4 fields")
    print(f"   📐 MATH: Problem field + direct answer (no choices)")
    print(f"   📝 IFEVAL: Prompt field + direct answer (no choices)")
    print(f"   ✨ All tasks show:")
    print(f"      - Full context/question")
    print(f"      - Answer choices (when available) or note for direct answers")
    print(f"      - Model's selection/response")
    print(f"      - Correct answer")
    print(f"      - Confidence scores (when available)")

if __name__ == "__main__":
    test_comprehensive_enhancement() 