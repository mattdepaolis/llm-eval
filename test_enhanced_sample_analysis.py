#!/usr/bin/env python3
"""
Test script to demonstrate the enhanced sample analysis functionality.
"""

import json
import os
from llm_testkit.reporting.html_report_generator import generate_html_report_from_json

def test_enhanced_sample_analysis():
    """Test the enhanced sample analysis with the provided JSON file."""
    
    print("🧪 Testing Enhanced Sample Analysis")
    print("=" * 50)
    
    # Path to the results file
    json_path = "my_results/results_Qwen_Qwen2.5-7B-Instruct_leaderboard_20250608_140345.json"
    
    if not os.path.exists(json_path):
        print(f"❌ Results file not found: {json_path}")
        return
    
    print(f"📁 Loading results from: {json_path}")
    
    # Load and examine the structure
    with open(json_path, 'r') as f:
        data = json.load(f)
    
    samples = data.get('samples', {})
    print(f"📊 Found {len(samples)} task types with samples")
    
    # Show sample structure for first few tasks
    for task_name, task_samples in list(samples.items())[:3]:
        print(f"\n🎯 Task: {task_name}")
        print(f"   Samples: {len(task_samples)}")
        
        if task_samples:
            sample = task_samples[0]
            print(f"   Sample structure:")
            print(f"     - doc: {bool(sample.get('doc'))}")
            print(f"     - target: {sample.get('target')}")
            print(f"     - filtered_resps: {bool(sample.get('filtered_resps'))}")
            
            # Show doc structure
            if 'doc' in sample:
                doc = sample['doc']
                doc_keys = list(doc.keys())[:5]  # First 5 keys
                print(f"     - doc keys: {doc_keys}")
    
    # Generate enhanced HTML report
    print(f"\n🎨 Generating Enhanced HTML Report...")
    output_path = "enhanced_sample_analysis_demo.html"
    
    try:
        result_path = generate_html_report_from_json(json_path, output_path)
        print(f"✅ Enhanced report generated: {result_path}")
        
        # Show what's enhanced
        print(f"\n🌟 Enhanced Features:")
        print(f"   ✨ Clear section separation:")
        print(f"      📖 Question/Context Section")
        print(f"      📋 Answer Choices Section") 
        print(f"      🤖 Model Response Section")
        print(f"      ✅ Correct Answer Section")
        print(f"      📊 Model Confidence Section")
        print(f"   ✨ Zeno ML-style presentation")
        print(f"   ✨ Better task type detection")
        print(f"   ✨ Enhanced choice highlighting")
        print(f"   ✨ Professional visual styling")
        
    except Exception as e:
        print(f"❌ Error generating report: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_enhanced_sample_analysis() 