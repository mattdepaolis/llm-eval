#!/usr/bin/env python3
"""
Professional HTML Report Generator for LLM Evaluation
Creates visually appealing and interactive HTML evaluation reports.
"""

import os
import json
import base64
from datetime import datetime
from typing import Optional, Dict, Any, List, Union, Tuple
import numpy as np
from collections import defaultdict
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

# Import enhanced model configuration utilities
from ..models.model_config import get_comprehensive_model_info, get_model_architecture_info

# Define CET timezone
try:
    CET = ZoneInfo("Europe/Berlin")
except ZoneInfoNotFoundError:
    print("Warning: Timezone 'Europe/Berlin' not found. Using system default timezone.")
    CET = None

def get_reports_dir():
    """Get the path to the reports directory, creating it if it doesn't exist."""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(os.path.dirname(script_dir))
    reports_dir = os.path.join(parent_dir, "reports")
    os.makedirs(reports_dir, exist_ok=True)
    return reports_dir

def get_html_template() -> str:
    """Get the HTML template with professional styling and interactivity."""
    return """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>LLM Evaluation Report - {model_name}</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/chartjs-adapter-date-fns"></script>
    <style>
        :root {{
            --primary-color: #2563eb;
            --secondary-color: #1e40af;
            --accent-color: #f59e0b;
            --success-color: #10b981;
            --warning-color: #f59e0b;
            --danger-color: #ef4444;
            --background-color: #f8fafc;
            --card-background: #ffffff;
            --text-primary: #1e293b;
            --text-secondary: #64748b;
            --border-color: #e2e8f0;
            --shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
        }}

        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background-color: var(--background-color);
            color: var(--text-primary);
            line-height: 1.6;
        }}

        .header {{
            background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
            color: white;
            padding: 2rem 0;
            box-shadow: var(--shadow);
        }}

        .container {{
            max-width: 1200px;
            margin: 0 auto;
            padding: 0 1rem;
        }}

        .header-content {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
            gap: 1rem;
        }}

        .header h1 {{
            font-size: 2.5rem;
            font-weight: 700;
            margin-bottom: 0.5rem;
        }}

        .header .subtitle {{
            font-size: 1.1rem;
            opacity: 0.9;
        }}

        .header .meta {{
            text-align: right;
        }}

        .header .meta div {{
            margin-bottom: 0.5rem;
        }}

        .main-content {{
            padding: 2rem 0;
        }}

        .card {{
            background: var(--card-background);
            border-radius: 12px;
            padding: 1.5rem;
            margin-bottom: 2rem;
            box-shadow: var(--shadow);
            border: 1px solid var(--border-color);
        }}

        .card h2 {{
            color: var(--primary-color);
            font-size: 1.5rem;
            font-weight: 600;
            margin-bottom: 1rem;
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }}

        .card h3 {{
            color: var(--text-primary);
            font-size: 1.2rem;
            font-weight: 600;
            margin-bottom: 0.75rem;
            margin-top: 1.5rem;
        }}

        .grid {{
            display: grid;
            gap: 1rem;
        }}

        .grid-2 {{
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
        }}

        .grid-3 {{
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
        }}

        .metric-card {{
            background: linear-gradient(135deg, var(--card-background), #f1f5f9);
            border: 1px solid var(--border-color);
            border-radius: 8px;
            padding: 1.25rem;
            text-align: center;
            transition: transform 0.2s, box-shadow 0.2s;
        }}

        .metric-card:hover {{
            transform: translateY(-2px);
            box-shadow: 0 8px 25px -8px rgba(0, 0, 0, 0.2);
        }}

        .metric-value {{
            font-size: 2rem;
            font-weight: 700;
            margin-bottom: 0.5rem;
        }}

        .metric-label {{
            color: var(--text-secondary);
            font-size: 0.9rem;
            font-weight: 500;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }}

        .performance-badge {{
            display: inline-flex;
            align-items: center;
            gap: 0.5rem;
            padding: 0.5rem 1rem;
            border-radius: 20px;
            font-weight: 600;
            font-size: 0.9rem;
            margin: 0.5rem 0;
        }}

        .badge-excellent {{
            background-color: #dcfce7;
            color: #166534;
            border: 1px solid #bbf7d0;
        }}

        .badge-good {{
            background-color: #fef3c7;
            color: #92400e;
            border: 1px solid #fde68a;
        }}

        .badge-needs-improvement {{
            background-color: #fee2e2;
            color: #991b1b;
            border: 1px solid #fecaca;
        }}

        .progress-bar {{
            width: 100%;
            height: 8px;
            background-color: #e5e7eb;
            border-radius: 4px;
            overflow: hidden;
            margin: 0.5rem 0;
        }}

        .progress-fill {{
            height: 100%;
            border-radius: 4px;
            transition: width 0.5s ease;
        }}

        .progress-excellent {{
            background: linear-gradient(90deg, var(--success-color), #34d399);
        }}

        .progress-good {{
            background: linear-gradient(90deg, var(--warning-color), #fbbf24);
        }}

        .progress-poor {{
            background: linear-gradient(90deg, var(--danger-color), #f87171);
        }}

        .table-container {{
            overflow-x: auto;
            border-radius: 8px;
            border: 1px solid var(--border-color);
        }}

        table {{
            width: 100%;
            border-collapse: collapse;
            background: var(--card-background);
        }}

        th, td {{
            padding: 0.75rem 1rem;
            text-align: left;
            border-bottom: 1px solid var(--border-color);
        }}

        th {{
            background-color: #f8fafc;
            font-weight: 600;
            color: var(--text-primary);
            position: sticky;
            top: 0;
        }}

        tr:hover {{
            background-color: #f8fafc;
        }}

        .chart-container {{
            position: relative;
            height: 400px;
            margin: 1rem 0;
        }}

        .code-block {{
            background-color: #1e293b;
            color: #e2e8f0;
            padding: 1rem;
            border-radius: 6px;
            font-family: 'Monaco', 'Consolas', monospace;
            font-size: 0.9rem;
            overflow-x: auto;
            margin: 1rem 0;
        }}

        .sample-card {{
            border: 1px solid var(--border-color);
            border-radius: 8px;
            margin: 1rem 0;
            overflow: hidden;
        }}

        .sample-header {{
            background-color: #f8fafc;
            padding: 0.75rem 1rem;
            font-weight: 600;
            border-bottom: 1px solid var(--border-color);
        }}

        .sample-content {{
            padding: 1rem;
        }}

        .correct {{
            border-left: 4px solid var(--success-color);
        }}

        .incorrect {{
            border-left: 4px solid var(--danger-color);
        }}

        .tabs {{
            display: flex;
            border-bottom: 1px solid var(--border-color);
            margin-bottom: 1rem;
        }}

        .tab {{
            padding: 0.75rem 1.5rem;
            background: none;
            border: none;
            cursor: pointer;
            border-bottom: 2px solid transparent;
            font-weight: 500;
            color: var(--text-secondary);
            transition: all 0.2s;
        }}

        .tab.active {{
            color: var(--primary-color);
            border-bottom-color: var(--primary-color);
        }}

        .tab-content {{
            display: none;
        }}

        .tab-content.active {{
            display: block;
        }}

        .footer {{
            background-color: var(--card-background);
            border-top: 1px solid var(--border-color);
            padding: 2rem 0;
            margin-top: 3rem;
            text-align: center;
            color: var(--text-secondary);
        }}

        .watermark {{
            position: fixed;
            bottom: 20px;
            right: 20px;
            background: var(--primary-color);
            color: white;
            padding: 0.5rem 1rem;
            border-radius: 20px;
            font-size: 0.8rem;
            font-weight: 600;
            box-shadow: var(--shadow);
            z-index: 1000;
        }}

        @media (max-width: 768px) {{
            .header h1 {{
                font-size: 2rem;
            }}
            
            .header-content {{
                text-align: center;
            }}
            
            .container {{
                padding: 0 0.5rem;
            }}
            
            .card {{
                padding: 1rem;
            }}
        }}

        .loading {{
            display: inline-block;
            width: 20px;
            height: 20px;
            border: 3px solid rgba(255,255,255,0.3);
            border-radius: 50%;
            border-top-color: #fff;
            animation: spin 1s ease-in-out infinite;
        }}

        @keyframes spin {{
            to {{ transform: rotate(360deg); }}
        }}

        /* Choice and Answer Styling */
        .choice-list {{
            margin: 1rem 0;
            border: 1px solid var(--border-color);
            border-radius: 8px;
            overflow: hidden;
        }}

        .choice-item {{
            padding: 0.75rem 1rem;
            border-bottom: 1px solid var(--border-color);
            background: var(--card-background);
            transition: all 0.2s;
        }}

        .choice-item:last-child {{
            border-bottom: none;
        }}

        .choice-item:hover {{
            background-color: #f8fafc;
        }}

        .choice-correct {{
            background-color: #f0fdf4 !important;
            border-left: 4px solid var(--success-color);
        }}

        .choice-correct-selected {{
            background-color: #dcfce7 !important;
            border-left: 4px solid var(--success-color);
            box-shadow: 0 0 8px rgba(34, 197, 94, 0.2);
        }}

        .choice-incorrect-selected {{
            background-color: #fef2f2 !important;
            border-left: 4px solid var(--danger-color);
            box-shadow: 0 0 8px rgba(239, 68, 68, 0.2);
        }}

        .answer-highlight {{
            padding: 1rem;
            border-radius: 8px;
            margin: 1rem 0;
            border: 2px solid;
            font-weight: 500;
        }}

        .correct-answer {{
            background-color: #f0fdf4;
            border-color: var(--success-color);
            color: #166534;
        }}

        .correct-response {{
            background-color: #f0fdf4;
            border-color: var(--success-color);
            color: #166534;
        }}

        .incorrect-response {{
            background-color: #fef2f2;
            border-color: var(--danger-color);
            color: #991b1b;
        }}

        .context-block {{
            background-color: #f8fafc;
            border-left: 4px solid var(--primary-color);
            padding: 1rem;
            margin: 1rem 0;
            border-radius: 6px;
            font-style: italic;
        }}

        .activity-label {{
            background-color: var(--primary-color);
            color: white;
            padding: 0.25rem 0.75rem;
            border-radius: 12px;
            font-size: 0.8rem;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            display: inline-block;
            margin-bottom: 0.5rem;
        }}
    </style>
</head>
<body>
    <header class="header">
        <div class="container">
            <div class="header-content">
                <div>
                    <h1>🧠 LLM Evaluation Report</h1>
                    <div class="subtitle">Model: {model_name}</div>
                </div>
                <div class="meta">
                    <div>📅 Generated: {timestamp}</div>
                    <div>⚡ Framework: Professional LLM Eval</div>
                </div>
            </div>
        </div>
    </header>

    <main class="main-content">
        <div class="container">
            {content}
        </div>
    </main>

    <footer class="footer">
        <div class="container">
            <p>Generated by Professional LLM Evaluation Framework</p>
            <p>This report contains comprehensive AI model performance metrics and analysis</p>
        </div>
    </footer>

    <div class="watermark">
        💎 Professional AI Eval
    </div>

    <script>
        // Initialize charts and interactive elements
        document.addEventListener('DOMContentLoaded', function() {{
            initializeCharts();
            initializeTabs();
            animateProgressBars();
        }});

        function initializeCharts() {{
            // Performance overview chart
            const ctx = document.getElementById('performanceChart');
            if (ctx) {{
                new Chart(ctx, {{
                    type: 'radar',
                    data: {chart_data},
                    options: {{
                        responsive: true,
                        maintainAspectRatio: false,
                        plugins: {{
                            legend: {{
                                position: 'top',
                            }},
                            title: {{
                                display: true,
                                text: 'Performance Overview'
                            }}
                        }},
                        scales: {{
                            r: {{
                                beginAtZero: true,
                                max: 100
                            }}
                        }}
                    }}
                }});
            }}

            // Task comparison chart
            const ctx2 = document.getElementById('taskChart');
            if (ctx2) {{
                new Chart(ctx2, {{
                    type: 'bar',
                    data: {task_chart_data},
                    options: {{
                        responsive: true,
                        maintainAspectRatio: false,
                        plugins: {{
                            legend: {{
                                display: false
                            }},
                            title: {{
                                display: true,
                                text: 'Task Performance Breakdown'
                            }}
                        }},
                        scales: {{
                            y: {{
                                beginAtZero: true,
                                max: 100
                            }}
                        }}
                    }}
                }});
            }}
        }}

        function initializeTabs() {{
            const tabs = document.querySelectorAll('.tab');
            const tabContents = document.querySelectorAll('.tab-content');

            tabs.forEach(tab => {{
                tab.addEventListener('click', () => {{
                    const target = tab.dataset.tab;
                    
                    tabs.forEach(t => t.classList.remove('active'));
                    tabContents.forEach(content => content.classList.remove('active'));
                    
                    tab.classList.add('active');
                    document.getElementById(target).classList.add('active');
                }});
            }});
        }}

        function animateProgressBars() {{
            const progressBars = document.querySelectorAll('.progress-fill');
            progressBars.forEach(bar => {{
                const width = bar.style.width;
                bar.style.width = '0%';
                setTimeout(() => {{
                    bar.style.width = width;
                }}, 100);
            }});
        }}
    </script>
</body>
</html>"""

def extract_model_info(config: Dict[str, Any]) -> Dict[str, Any]:
    """Extract comprehensive model information from config using enhanced model utilities."""
    # Use the comprehensive model info function from models module
    return get_comprehensive_model_info(config)

def create_performance_badge(score: float, threshold_good: float = 70.0, threshold_fair: float = 50.0) -> str:
    """Create a performance badge based on score."""
    if score >= threshold_good:
        return '<span class="performance-badge badge-excellent">🟢 EXCELLENT</span>'
    elif score >= threshold_fair:
        return '<span class="performance-badge badge-good">🟡 GOOD</span>'
    else:
        return '<span class="performance-badge badge-needs-improvement">🔴 NEEDS IMPROVEMENT</span>'

def create_progress_bar(score: float, max_score: float = 100.0) -> str:
    """Create a visual progress bar for scores."""
    percentage = min(score / max_score, 1.0) if max_score > 0 else 0
    
    if percentage >= 0.7:
        bar_class = "progress-excellent"
    elif percentage >= 0.5:
        bar_class = "progress-good"
    else:
        bar_class = "progress-poor"
    
    return f'''
    <div class="progress-bar">
        <div class="progress-fill {bar_class}" style="width: {percentage * 100:.1f}%"></div>
    </div>
    '''

def generate_executive_summary(results_data: Dict[str, Any], model_info: Dict[str, Any]) -> str:
    """Generate an executive summary section."""
    html = ['<div class="card">']
    html.append('<h2>📋 Executive Summary</h2>')
    
    # Calculate overall performance
    metrics = results_data.get('results', {})
    if metrics:
        # Get primary accuracy scores
        scores = []
        task_scores = {}
        
        for task, task_metrics in metrics.items():
            task_score = None
            for metric_name, value in task_metrics.items():
                if 'acc' in metric_name.lower() and 'stderr' not in metric_name.lower():
                    if isinstance(value, (int, float)):
                        score_pct = value * 100  # Convert to percentage
                        scores.append(score_pct)
                        task_scores[task] = score_pct
                        task_score = score_pct
                        break
            
            if task_score is None:
                # Look for other performance metrics
                for metric_name, value in task_metrics.items():
                    if isinstance(value, (int, float)) and 'stderr' not in metric_name.lower():
                        score_pct = value * 100
                        scores.append(score_pct)
                        task_scores[task] = score_pct
                        break
        
        if scores:
            avg_score = np.mean(scores)
            max_score = np.max(scores)
            min_score = np.min(scores)
            
            # Create performance assessment
            performance_badge = create_performance_badge(avg_score)
            
            html.append('<div class="grid grid-3">')
            html.append(f'''
            <div class="metric-card">
                <div class="metric-value" style="color: var(--primary-color);">{avg_score:.1f}%</div>
                <div class="metric-label">Average Score</div>
                {create_progress_bar(avg_score)}
            </div>
            <div class="metric-card">
                <div class="metric-value" style="color: var(--success-color);">{max_score:.1f}%</div>
                <div class="metric-label">Best Performance</div>
                {create_progress_bar(max_score)}
            </div>
            <div class="metric-card">
                <div class="metric-value" style="color: var(--warning-color);">{min_score:.1f}%</div>
                <div class="metric-label">Lowest Performance</div>
                {create_progress_bar(min_score)}
            </div>
            ''')
            html.append('</div>')
            
            html.append(f'<div style="text-align: center; margin: 1.5rem 0;">{performance_badge}</div>')
            
            # Add performance insights
            html.append('<h3>🔍 Key Insights</h3>')
            html.append('<ul>')
            
            if avg_score >= 80:
                html.append('<li>✅ <strong>Strong overall performance</strong> across evaluated tasks</li>')
            elif avg_score >= 60:
                html.append('<li>⚡ <strong>Moderate performance</strong> with room for improvement</li>')
            else:
                html.append('<li>🔧 <strong>Performance below expectations</strong> - consider fine-tuning or model selection</li>')
            
            if max_score - min_score > 30:
                html.append('<li>📊 <strong>High variance</strong> in task performance - model may excel in specific domains</li>')
            else:
                html.append('<li>📊 <strong>Consistent performance</strong> across different task types</li>')
            
            # Find best and worst performing tasks
            if task_scores:
                best_task = max(task_scores.items(), key=lambda x: x[1])
                worst_task = min(task_scores.items(), key=lambda x: x[1])
                html.append(f'<li>🏆 <strong>Best task:</strong> {best_task[0]} ({best_task[1]:.1f}%)</li>')
                html.append(f'<li>🔄 <strong>Improvement opportunity:</strong> {worst_task[0]} ({worst_task[1]:.1f}%)</li>')
            
            html.append('</ul>')
    
    html.append('</div>')
    return '\n'.join(html)

def generate_model_configuration(model_info: Dict[str, Any], config: Dict[str, Any]) -> str:
    """Generate comprehensive model configuration section."""
    html = ['<div class="card">']
    html.append('<h2>⚙️ Model Configuration</h2>')
    
    # Basic Model Information Section
    html.append('<h3>🔧 Basic Model Information</h3>')
    html.append('<div class="table-container">')
    html.append('<table>')
    html.append('<thead><tr><th>Parameter</th><th>Value</th></tr></thead>')
    html.append('<tbody>')
    
    basic_info = [
        ("Model Name", model_info.get("name", "Unknown")),
        ("Architecture", model_info.get("architecture", "Not specified")),
        ("Parameters", model_info.get("parameters", "Not specified")),
        ("Context Length", model_info.get("context_length", "Not specified")),
        ("Backend", model_info.get("backend", "Unknown")),
        ("Data Type", model_info.get("data_type", "Not specified")),
        ("Quantization", model_info.get("quantization", "None")),
        ("Revision", model_info.get("revision", "main")),
    ]
    
    for param, value in basic_info:
        html.append(f'<tr><td><strong>{param}</strong></td><td>{value}</td></tr>')
    
    html.append('</tbody>')
    html.append('</table>')
    html.append('</div>')
    
    # Hardware and Performance Configuration
    html.append('<h3>🖥️ Hardware & Performance Configuration</h3>')
    html.append('<div class="table-container">')
    html.append('<table>')
    html.append('<thead><tr><th>Parameter</th><th>Value</th></tr></thead>')
    html.append('<tbody>')
    
    hardware_info = [
        ("Device Mapping", model_info.get("device_mapping", "Single GPU")),
        ("Tensor Parallel Size", str(model_info.get("tensor_parallel_size", 1))),
        ("Pipeline Parallel Size", str(model_info.get("pipeline_parallel_size", 1))),
        ("GPU Memory Utilization", model_info.get("gpu_memory_utilization", "Not specified")),
        ("Max Model Length", model_info.get("max_model_len", "Not specified")),
        ("Trust Remote Code", model_info.get("trust_remote_code", "False")),
        ("Evaluation Device", model_info.get("evaluation_device", "Not specified")),
        ("Batch Size", model_info.get("batch_size", "Not specified")),
    ]
    
    for param, value in hardware_info:
        html.append(f'<tr><td><strong>{param}</strong></td><td>{value}</td></tr>')
    
    html.append('</tbody>')
    html.append('</table>')
    html.append('</div>')
    
    # Advanced Features and Optimization
    html.append('<h3>⚡ Advanced Features & Optimization</h3>')
    html.append('<div class="table-container">')
    html.append('<table>')
    html.append('<thead><tr><th>Parameter</th><th>Value</th></tr></thead>')
    html.append('<tbody>')
    
    advanced_info = [
        ("Attention Implementation", model_info.get("attention_implementation", "Not specified")),
        ("Flash Attention", model_info.get("use_flash_attention", "Not specified")),
        ("Low CPU Memory Usage", model_info.get("low_cpu_mem_usage", "Not specified")),
        ("Use Cache", model_info.get("use_cache", "Not specified")),
        ("Cache Directory", model_info.get("cache_dir", "Not specified")),
        ("Offload Folder", model_info.get("offload_folder", "Not specified")),
        ("PEFT Configuration", model_info.get("peft_config", "None")),
        ("LoRA Configuration", model_info.get("lora_config", "None")),
    ]
    
    for param, value in advanced_info:
        html.append(f'<tr><td><strong>{param}</strong></td><td>{value}</td></tr>')
    
    html.append('</tbody>')
    html.append('</table>')
    html.append('</div>')
    
    # Generation Parameters
    html.append('<h3>🎯 Generation Parameters</h3>')
    html.append('<div class="table-container">')
    html.append('<table>')
    html.append('<thead><tr><th>Parameter</th><th>Value</th></tr></thead>')
    html.append('<tbody>')
    
    generation_info = [
        ("Temperature", model_info.get("temperature", "Not specified")),
        ("Top P", model_info.get("top_p", "Not specified")),
        ("Top K", model_info.get("top_k", "Not specified")),
        ("Max Tokens", model_info.get("max_tokens", "Not specified")),
        ("Max New Tokens", model_info.get("max_new_tokens", "Not specified")),
        ("Do Sample", model_info.get("do_sample", "Not specified")),
        ("Num Beams", model_info.get("num_beams", "Not specified")),
        ("Repetition Penalty", model_info.get("repetition_penalty", "Not specified")),
        ("Length Penalty", model_info.get("length_penalty", "Not specified")),
        ("Early Stopping", model_info.get("early_stopping", "Not specified")),
    ]
    
    for param, value in generation_info:
        html.append(f'<tr><td><strong>{param}</strong></td><td>{value}</td></tr>')
    
    html.append('</tbody>')
    html.append('</table>')
    html.append('</div>')
    
    # Evaluation Configuration
    html.append('<h3>📋 Evaluation Configuration</h3>')
    html.append('<div class="table-container">')
    html.append('<table>')
    html.append('<thead><tr><th>Parameter</th><th>Value</th></tr></thead>')
    html.append('<tbody>')
    
    eval_info = [
        ("Evaluated Tasks", model_info.get("evaluated_tasks", "Not specified")),
        ("Number of Few-shot Examples", model_info.get("num_fewshot", "Not specified")),
        ("Samples Per Task", model_info.get("samples_per_task", "All available")),
        ("Evaluation Framework", "lm-evaluation-harness"),
    ]
    
    for param, value in eval_info:
        html.append(f'<tr><td><strong>{param}</strong></td><td>{value}</td></tr>')
    
    html.append('</tbody>')
    html.append('</table>')
    html.append('</div>')
    
    # Architecture Details (if available)
    if model_info.get("name", "Unknown") != "Unknown":
        arch_info = get_model_architecture_info(model_info["name"])
        if arch_info.get("family", "Unknown") != "Unknown":
            html.append('<h3>🏗️ Architecture Details</h3>')
            html.append('<div class="table-container">')
            html.append('<table>')
            html.append('<thead><tr><th>Aspect</th><th>Details</th></tr></thead>')
            html.append('<tbody>')
            
            for key, value in arch_info.items():
                if key != "family":  # Skip family as it's redundant with architecture
                    display_key = key.replace("_", " ").title()
                    html.append(f'<tr><td><strong>{display_key}</strong></td><td>{value}</td></tr>')
            
            html.append('</tbody>')
            html.append('</table>')
            html.append('</div>')
    
    html.append('</div>')
    return '\n'.join(html)

def generate_performance_charts(results_data: Dict[str, Any]) -> Tuple[str, str]:
    """Generate chart data for performance visualization."""
    metrics = results_data.get('results', {})
    
    if not metrics:
        return '{}', '{}'
    
    # Collect task scores
    task_scores = {}
    for task, task_metrics in metrics.items():
        for metric_name, value in task_metrics.items():
            if 'acc' in metric_name.lower() and 'stderr' not in metric_name.lower():
                if isinstance(value, (int, float)):
                    task_scores[task] = value * 100
                    break
    
    if not task_scores:
        return '{}', '{}'
    
    # Generate chart data
    chart_data = {
        "labels": list(task_scores.keys()),
        "datasets": [{
            "label": "Performance (%)",
            "data": list(task_scores.values()),
            "borderColor": "rgb(37, 99, 235)",
            "backgroundColor": "rgba(37, 99, 235, 0.2)",
            "borderWidth": 2
        }]
    }
    
    task_chart_data = {
        "labels": list(task_scores.keys()),
        "datasets": [{
            "label": "Accuracy (%)",
            "data": list(task_scores.values()),
            "backgroundColor": [
                "rgba(16, 185, 129, 0.8)" if score >= 70 else
                "rgba(245, 158, 11, 0.8)" if score >= 50 else
                "rgba(239, 68, 68, 0.8)"
                for score in task_scores.values()
            ],
            "borderColor": [
                "rgb(16, 185, 129)" if score >= 70 else
                "rgb(245, 158, 11)" if score >= 50 else
                "rgb(239, 68, 68)"
                for score in task_scores.values()
            ],
            "borderWidth": 2
        }]
    }
    
    return json.dumps(chart_data), json.dumps(task_chart_data)

def generate_task_results(results_data: Dict[str, Any]) -> str:
    """Generate detailed task results section."""
    html = ['<div class="card">']
    html.append('<h2>📊 Task Performance Results</h2>')
    
    metrics = results_data.get('results', {})
    if not metrics:
        html.append('<p>No task results available.</p>')
        html.append('</div>')
        return '\n'.join(html)
    
    # Add performance charts
    html.append('<div class="chart-container">')
    html.append('<canvas id="taskChart"></canvas>')
    html.append('</div>')
    
    # Performance radar chart
    html.append('<div class="chart-container">')
    html.append('<canvas id="performanceChart"></canvas>')
    html.append('</div>')
    
    # Detailed results table
    html.append('<h3>📋 Detailed Results</h3>')
    html.append('<div class="table-container">')
    html.append('<table>')
    html.append('<thead><tr><th>Task</th><th>Metric</th><th>Score</th><th>Performance</th></tr></thead>')
    html.append('<tbody>')
    
    for task, task_metrics in metrics.items():
        first_metric = True
        for metric_name, value in task_metrics.items():
            if 'stderr' not in metric_name.lower():
                if isinstance(value, (int, float)):
                    score_pct = value * 100 if 'acc' in metric_name.lower() else value
                    performance_badge = create_performance_badge(score_pct) if score_pct <= 100 else f'{score_pct:.2f}'
                    
                    task_display = task if first_metric else ''
                    html.append(f'<tr><td>{task_display}</td><td>{metric_name}</td><td>{score_pct:.2f}%</td><td>{performance_badge}</td></tr>')
                    first_metric = False
    
    html.append('</tbody>')
    html.append('</table>')
    html.append('</div>')
    html.append('</div>')
    
    return '\n'.join(html)

def generate_sample_analysis(results_data: Dict[str, Any]) -> str:
    """Generate sample analysis section with tabs and proper hellaswag context handling."""
    html = ['<div class="card">']
    html.append('<h2>🔍 Sample Analysis</h2>')
    
    samples = results_data.get('samples', {})
    if not samples:
        html.append('<p>No sample data available for analysis.</p>')
        html.append('</div>')
        return '\n'.join(html)
    
    # Create tabs for different tasks
    task_names = list(samples.keys())
    if not task_names:
        html.append('<p>No sample data available for analysis.</p>')
        html.append('</div>')
        return '\n'.join(html)
    
    html.append('<div class="tabs">')
    for i, task in enumerate(task_names):
        active_class = 'active' if i == 0 else ''
        html.append(f'<button class="tab {active_class}" data-tab="task-{i}">{task}</button>')
    html.append('</div>')
    
    # Tab contents
    for i, (task, task_samples) in enumerate(samples.items()):
        active_class = 'active' if i == 0 else ''
        html.append(f'<div id="task-{i}" class="tab-content {active_class}">')
        
        # Check if this is a hellaswag task
        is_hellaswag = 'hellaswag' in task.lower()
        
        # Show up to 5 samples per task
        displayed_samples = 0
        max_samples = 5
        
        for sample in task_samples[:max_samples]:
            if displayed_samples >= max_samples:
                break
            
            # Determine if sample is correct based on target and model selection
            is_correct = False
            model_choice_index = None
            model_choice_label = None
            model_choice_text = None
            
            # Get the correct answer information
            target_index = sample.get('target')
            correct_choice_label = None
            correct_choice_text = None
            
            if 'doc' in sample and sample['doc'].get('choices'):
                choices = sample['doc']['choices']
                labels = []
                texts = []
                
                # Handle different choice formats
                if isinstance(choices, dict) and 'text' in choices and 'label' in choices:
                    # Dictionary format: {'text': [...], 'label': [...]}
                    labels = choices['label']
                    texts = choices['text']
                elif isinstance(choices, list):
                    # List format: ['option1', 'option2', ...]
                    texts = choices
                    labels = [chr(65 + i) for i in range(len(choices))]  # A, B, C, D...
                else:
                    # For hellaswag, choices might be in 'endings' field
                    if is_hellaswag and 'endings' in sample['doc']:
                        texts = sample['doc']['endings']
                        labels = [chr(65 + i) for i in range(len(texts))]
                    else:
                        # Fallback for other formats
                        labels = []
                        texts = []
                
                # Get correct answer
                if target_index is not None and target_index < len(labels) and target_index < len(texts):
                    correct_choice_label = labels[target_index]
                    correct_choice_text = texts[target_index]
                
                # Determine model's choice from filtered_resps (highest log probability)
                if 'filtered_resps' in sample and sample['filtered_resps']:
                    log_probs = []
                    for resp in sample['filtered_resps']:
                        if isinstance(resp, list) and len(resp) >= 1:
                            log_probs.append(resp[0])  # First element is log probability
                        else:
                            log_probs.append(float('-inf'))
                    
                    if log_probs:
                        # Model choice is the one with highest log probability (least negative)
                        model_choice_index = log_probs.index(max(log_probs))
                        if model_choice_index < len(labels) and model_choice_index < len(texts):
                            model_choice_label = labels[model_choice_index]
                            model_choice_text = texts[model_choice_index]
                            
                        # Check if model's choice matches target
                        is_correct = model_choice_index == target_index
            
            correctness_class = 'correct' if is_correct else 'incorrect'
            correctness_icon = '✅' if is_correct else '❌'
            
            html.append(f'<div class="sample-card {correctness_class}">')
            html.append(f'<div class="sample-header">{correctness_icon} Sample {displayed_samples + 1}</div>')
            html.append('<div class="sample-content">')
            
            # Show activity label for hellaswag
            if is_hellaswag and 'doc' in sample and 'activity_label' in sample['doc']:
                html.append(f'<div class="activity-label">{sample["doc"]["activity_label"]}</div>')
            
            # Show the question or context based on task type
            if is_hellaswag:
                # For hellaswag, show the context (ctx) field
                if 'doc' in sample:
                    doc = sample['doc']
                    context = ""
                    
                    # HellaSwag can have context in different fields
                    if 'ctx' in doc:
                        context = doc['ctx']
                    elif 'ctx_a' in doc:
                        # Some versions split context into ctx_a and ctx_b
                        context = doc['ctx_a']
                        if 'ctx_b' in doc and doc['ctx_b']:
                            context += " " + doc['ctx_b']
                    
                    if context:
                        html.append(f'<h4>📝 Context:</h4>')
                        html.append(f'<div class="context-block">{context}</div>')
            else:
                # For other tasks, show the question field
                if 'doc' in sample and 'question' in sample['doc']:
                    html.append(f'<h4>❓ Question:</h4>')
                    html.append(f'<div class="code-block">{sample["doc"]["question"]}</div>')
            
            # Show answer choices
            if 'doc' in sample:
                doc = sample['doc']
                choices = None
                labels = []
                texts = []
                
                # Get choices from appropriate field
                if 'choices' in doc:
                    choices = doc['choices']
                elif is_hellaswag and 'endings' in doc:
                    choices = doc['endings']
                
                if choices:
                    # Handle different choice formats
                    if isinstance(choices, dict) and 'text' in choices and 'label' in choices:
                        # Dictionary format: {'text': [...], 'label': [...]}
                        labels = choices['label']
                        texts = choices['text']
                    elif isinstance(choices, list):
                        # List format: ['option1', 'option2', ...]
                        texts = choices
                        labels = [chr(65 + i) for i in range(len(choices))]  # A, B, C, D...
                
                if labels and texts:
                    html.append(f'<h4>📋 Answer Choices:</h4>')
                    html.append('<div class="choice-list">')
                    
                    for idx, (label, text) in enumerate(zip(labels, texts)):
                        choice_class = ""
                        choice_icon = ""
                        
                        # Highlight correct answer
                        if idx == target_index:
                            choice_class = " choice-correct"
                            choice_icon = " ✅"
                        
                        # Highlight model's choice  
                        if idx == model_choice_index:
                            if idx == target_index:
                                choice_class = " choice-correct-selected"
                                choice_icon = " ✅🎯"  # Correct and selected
                            else:
                                choice_class = " choice-incorrect-selected"
                                choice_icon = " ❌🤖"  # Incorrect but selected
                        
                        html.append(f'<div class="choice-item{choice_class}">')
                        html.append(f'<strong>{label}.</strong> {text}{choice_icon}')
                        html.append('</div>')
                    
                    html.append('</div>')
            
            # Show correct answer clearly
            if correct_choice_label and correct_choice_text:
                html.append(f'<h4>✅ Correct Answer:</h4>')
                html.append(f'<div class="answer-highlight correct-answer">')
                html.append(f'<strong>{correct_choice_label}</strong> - {correct_choice_text}')
                html.append('</div>')
            
            # Show model's choice clearly
            if model_choice_label and model_choice_text:
                response_class = "correct-response" if is_correct else "incorrect-response"
                response_icon = "✅" if is_correct else "❌"
                html.append(f'<h4>🤖 Model Response ({response_icon} {"Correct" if is_correct else "Incorrect"}):</h4>')
                html.append(f'<div class="answer-highlight {response_class}">')
                html.append(f'<strong>{model_choice_label}</strong> - {model_choice_text}')
                html.append('</div>')
            else:
                # Fallback to show raw response if parsing fails
                if 'filtered_resps' in sample and sample['filtered_resps']:
                    html.append(f'<h4>🤖 Model Response (Raw):</h4>')
                    html.append(f'<div class="code-block">{sample["filtered_resps"][:100]}{"..." if len(str(sample["filtered_resps"])) > 100 else ""}</div>')
            
            html.append('</div>')
            html.append('</div>')
            
            displayed_samples += 1
        
        if len(task_samples) > max_samples:
            html.append(f'<p><em>... and {len(task_samples) - max_samples} more samples</em></p>')
        
        html.append('</div>')
    
    html.append('</div>')
    
    return '\n'.join(html)

def generate_html_report(results_data: Dict[str, Any], output_path: Optional[str] = None) -> str:
    """
    Generate a professional HTML report from evaluation results.
    
    Args:
        results_data: The evaluation results data
        output_path: Optional specific output path for the report
    
    Returns:
        Path to the generated HTML report
    """
    # Extract model information
    config = results_data.get('config', {})
    model_info = extract_model_info(config)
    model_name = model_info["name"]
    
    # Generate timestamp
    now = datetime.now(CET) if CET else datetime.now()
    timestamp = now.strftime('%Y-%m-%d %H:%M:%S')
    
    # Generate chart data
    chart_data, task_chart_data = generate_performance_charts(results_data)
    
    # Generate content sections
    content_sections = []
    content_sections.append(generate_executive_summary(results_data, model_info))
    content_sections.append(generate_model_configuration(model_info, config))
    content_sections.append(generate_task_results(results_data))
    content_sections.append(generate_sample_analysis(results_data))
    
    content = '\n'.join(content_sections)
    
    # Generate final HTML
    template = get_html_template()
    html_content = template.format(
        model_name=model_name,
        timestamp=timestamp,
        content=content,
        chart_data=chart_data,
        task_chart_data=task_chart_data
    )
    
    # Determine output path if not specified
    if not output_path:
        reports_dir = get_reports_dir()
        timestamp_file = now.strftime('%Y%m%d_%H%M%S')
        output_path = os.path.join(reports_dir, f"report_{model_name}_{timestamp_file}.html")
    
    # Save HTML to file
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"✨ Professional HTML report generated: {output_path}")
    return output_path

def generate_html_report_from_json(json_path: str, output_path: Optional[str] = None) -> str:
    """
    Generate an HTML report from a JSON results file.
    
    Args:
        json_path: Path to the JSON results file
        output_path: Optional specific output path for the report
        
    Returns:
        Path to the generated HTML report
    """
    try:
        with open(json_path, 'r') as f:
            results_data = json.load(f)
        
        if not output_path:
            # Generate output path based on JSON filename
            base_name = os.path.splitext(os.path.basename(json_path))[0]
            reports_dir = get_reports_dir()
            output_path = os.path.join(reports_dir, f"{base_name}.html")
        
        return generate_html_report(results_data, output_path)
        
    except Exception as e:
        print(f"❌ Error generating HTML report from JSON: {e}")
        raise 