#!/usr/bin/env python3
"""
Test script to demonstrate the model comparison feature.
"""

import llm_testkit
import json
import os
from llm_testkit.comparison.model_comparison import get_available_comparison_models, save_model_results

def test_comparison_feature():
    """Test the model comparison functionality."""
    
    print("🧪 Testing Model Comparison Feature")
    print("=" * 60)
    
    # First, let's create some mock comparison data for demonstration
    create_mock_comparison_data()
    
    # Generate a report with comparison capabilities
    json_path = 'my_results/results_Qwen_Qwen2.5-7B-Instruct_leaderboard_20250608_140345.json'
    
    print(f"\n🎨 Generating report with comparison features...")
    output_path = llm_testkit.generate_html_report_from_json(
        json_path, 
        'MODEL_COMPARISON_DEMO.html'
    )
    
    print(f"✅ Report with comparison features generated: {output_path}")
    
    # Show available comparison models
    available_models = get_available_comparison_models()
    print(f"\n📊 Available models for comparison: {len(available_models)}")
    for model in available_models:
        print(f"   - {model['model_name']} ({model['timestamp']})")
    
    print(f"\n🌟 Comparison Features Added:")
    print(f"   📊 Dropdown menu to select previous benchmarks")
    print(f"   🎯 Interactive radar chart overlay")
    print(f"   🔄 Toggle between original and comparison views")
    print(f"   ➕ Add/remove models from comparison")
    print(f"   🧹 Clear all comparisons")
    print(f"   💾 Automatic saving of results for future comparisons")
    
    print(f"\n📋 How to Use:")
    print(f"   1. Open the generated HTML report")
    print(f"   2. Look for the 'Compare with Previous Benchmarks' section")
    print(f"   3. Select models from the dropdown")
    print(f"   4. Click 'Add to Comparison' to add them")
    print(f"   5. Click 'Show Comparison' to overlay performance charts")
    print(f"   6. Toggle between original and comparison views")

def create_mock_comparison_data():
    """Create some mock comparison data for demonstration."""
    from llm_testkit.comparison.model_comparison import get_comparison_results_dir
    import datetime
    
    comparison_dir = get_comparison_results_dir()
    
    # Mock data for different models
    mock_models = [
        {
            'model_name': 'GPT-3.5-Turbo',
            'results': {
                'leaderboard_mmlu_pro': {'acc_norm': 0.65},
                'leaderboard_gpqa_diamond': {'acc_norm': 0.45},
                'leaderboard_math_algebra_hard': {'exact_match': 0.35},
                'leaderboard_bbh_boolean_expressions': {'acc_norm': 0.75},
                'leaderboard_musr_murder_mysteries': {'acc_norm': 0.55}
            },
            'config': {'model': 'gpt-3.5-turbo'}
        },
        {
            'model_name': 'Claude-3-Haiku',
            'results': {
                'leaderboard_mmlu_pro': {'acc_norm': 0.72},
                'leaderboard_gpqa_diamond': {'acc_norm': 0.52},
                'leaderboard_math_algebra_hard': {'exact_match': 0.42},
                'leaderboard_bbh_boolean_expressions': {'acc_norm': 0.82},
                'leaderboard_musr_murder_mysteries': {'acc_norm': 0.68}
            },
            'config': {'model': 'claude-3-haiku'}
        },
        {
            'model_name': 'Llama-3-8B',
            'results': {
                'leaderboard_mmlu_pro': {'acc_norm': 0.58},
                'leaderboard_gpqa_diamond': {'acc_norm': 0.38},
                'leaderboard_math_algebra_hard': {'exact_match': 0.28},
                'leaderboard_bbh_boolean_expressions': {'acc_norm': 0.68},
                'leaderboard_musr_murder_mysteries': {'acc_norm': 0.48}
            },
            'config': {'model': 'llama-3-8b'}
        }
    ]
    
    # Save mock models with different timestamps
    for i, mock_model in enumerate(mock_models):
        timestamp = datetime.datetime.now() - datetime.timedelta(days=i+1)
        
        comparison_data = {
            'model_name': mock_model['model_name'],
            'timestamp': timestamp.isoformat(),
            'results': mock_model['results'],
            'config': mock_model['config'],
            'model_info': {
                'name': mock_model['model_name'],
                'type': 'LLM',
                'architecture': 'Transformer',
                'size': 'Unknown'
            }
        }
        
        filename = f"{mock_model['model_name'].replace('-', '_')}_{timestamp.strftime('%Y%m%d_%H%M%S')}.json"
        filepath = os.path.join(comparison_dir, filename)
        
        with open(filepath, 'w') as f:
            json.dump(comparison_data, f, indent=2)
        
        print(f"📁 Created mock comparison data: {filename}")

if __name__ == "__main__":
    test_comparison_feature() 