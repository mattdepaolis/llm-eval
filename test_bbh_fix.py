#!/usr/bin/env python3
"""
Test script to verify BBH web_of_lies task is displayed correctly.
"""

import json
from llm_testkit.reporting.html_report_generator import extract_choices_from_doc, determine_model_answer, determine_correct_answer

def test_bbh_web_of_lies():
    """Test the BBH web_of_lies task specifically."""
    
    print("🧪 Testing BBH Web_of_Lies Task Fix")
    print("=" * 50)
    
    # Load the results
    json_path = 'my_results/results_Qwen_Qwen2.5-7B-Instruct_leaderboard_20250608_140345.json'
    with open(json_path, 'r') as f:
        data = json.load(f)

    samples = data.get('samples', {})
    
    # Get the web_of_lies task
    task_name = 'leaderboard_bbh_web_of_lies'
    if task_name not in samples:
        print(f"❌ Task {task_name} not found")
        return
    
    sample = samples[task_name][0]
    doc = sample.get('doc', {})
    
    print(f"📋 Task: {task_name}")
    print(f"🎯 Question: {doc.get('input', '')}")
    print(f"✅ Target: {sample.get('target')}")
    
    # Test choice extraction
    choices_info = extract_choices_from_doc(doc, is_bbh=True, sample=sample)
    choice_labels = choices_info['labels']
    choice_texts = choices_info['texts']
    
    print(f"\n📋 Extracted Choices:")
    if choice_labels and choice_texts:
        for label, text in zip(choice_labels, choice_texts):
            print(f"   {label}: {text}")
    else:
        print("   No choices extracted")
    
    # Test model answer determination
    model_info = determine_model_answer(sample, choice_labels, choice_texts)
    
    print(f"\n🤖 Model Response:")
    print(f"   Label: {model_info['label']}")
    print(f"   Text: {model_info['text']}")
    print(f"   Index: {model_info['index']}")
    
    # Test correct answer determination
    correct_info = determine_correct_answer(sample.get('target'), choice_labels, choice_texts, doc)
    
    print(f"\n✅ Correct Answer:")
    print(f"   Label: {correct_info['label']}")
    print(f"   Text: {correct_info['text']}")
    print(f"   Index: {correct_info['index']}")
    
    # Analyze arguments and responses
    print(f"\n🔍 Raw Data Analysis:")
    arguments = sample.get('arguments', [])
    filtered_resps = sample.get('filtered_resps', [])
    
    print(f"   Arguments ({len(arguments)}):")
    for i, arg in enumerate(arguments):
        if len(arg) >= 2:
            completion = arg[1]
            print(f"     {i}: {completion}")
    
    print(f"   Filtered Responses ({len(filtered_resps)}):")
    for i, resp in enumerate(filtered_resps):
        if isinstance(resp, list) and len(resp) >= 1:
            log_prob = resp[0]
            print(f"     {i}: {log_prob}")
    
    # Determine which was chosen
    if filtered_resps:
        log_probs = [resp[0] if isinstance(resp, list) and len(resp) >= 1 else float('-inf') for resp in filtered_resps]
        best_idx = log_probs.index(max(log_probs))
        print(f"\n🎯 Analysis:")
        print(f"   Model chose index {best_idx} (highest probability: {max(log_probs)})")
        print(f"   Model's choice: {arguments[best_idx][1] if best_idx < len(arguments) and len(arguments[best_idx]) >= 2 else 'Unknown'}")
        print(f"   Correct answer: {sample.get('target')}")
        print(f"   Result: {'✅ Correct' if arguments[best_idx][1].strip() == sample.get('target') else '❌ Incorrect'}")

if __name__ == "__main__":
    test_bbh_web_of_lies() 