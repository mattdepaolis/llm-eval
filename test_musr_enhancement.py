#!/usr/bin/env python3
"""
Test script to validate the enhanced MUSR task support.
"""

import json
import llm_testkit

def test_musr_enhancement():
    """Test the enhanced MUSR sample analysis."""
    
    print("🧪 Testing Enhanced MUSR Support")
    print("=" * 50)
    
    # Load the results to check MUSR tasks
    json_path = 'my_results/results_Qwen_Qwen2.5-7B-Instruct_leaderboard_20250608_140345.json'
    with open(json_path, 'r') as f:
        data = json.load(f)

    samples = data.get('samples', {})
    musr_tasks = [task for task in samples.keys() if 'musr' in task.lower()]
    print(f'📊 Found MUSR tasks: {musr_tasks}')

    for task in musr_tasks[:2]:  # Show first 2 MUSR tasks
        task_samples = samples[task]
        if task_samples:
            sample = task_samples[0]
            doc = sample.get('doc', {})
            print(f'\n🎯 Task: {task}')
            print(f'   Narrative present: {bool(doc.get("narrative"))}')
            print(f'   Question present: {bool(doc.get("question"))}')
            print(f'   Choices present: {bool(doc.get("choices"))}')
            print(f'   Choices format: {type(doc.get("choices"))}')
            if doc.get('choices'):
                print(f'   Choices content: {doc.get("choices")[:100]}...')
            
            # Show narrative length
            if doc.get('narrative'):
                narrative_len = len(doc['narrative'])
                print(f'   Narrative length: {narrative_len} characters')
                print(f'   Narrative preview: {doc["narrative"][:150]}...')

    # Generate enhanced report with MUSR support
    print(f'\n🎨 Generating Enhanced MUSR Report...')
    output_path = llm_testkit.generate_html_report_from_json(
        json_path, 
        'musr_enhanced_report.html'
    )
    
    print(f'✅ Enhanced MUSR report generated: {output_path}')
    print(f'\n🌟 MUSR Enhancement Features:')
    print(f'   📚 Narrative Section: Shows the full story context')
    print(f'   ❓ Question Section: Displays the specific question')
    print(f'   📋 Choices Section: Properly parsed choice options')
    print(f'   🤖 Model Response: Shows what the model selected')
    print(f'   ✅ Correct Answer: Displays the right answer')
    print(f'   📊 Confidence Scores: Model\'s confidence for each choice')

if __name__ == "__main__":
    test_musr_enhancement() 