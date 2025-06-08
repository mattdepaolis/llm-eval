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

# Import comparison functionality
try:
    from ..comparison.model_comparison import (
        save_model_results, get_available_comparison_models, 
        generate_comparison_dropdown_html, generate_comparison_javascript,
        generate_comparison_chart_data, extract_model_info_for_comparison
    )
    COMPARISON_AVAILABLE = True
except ImportError:
    COMPARISON_AVAILABLE = False
    print("⚠️ Comparison functionality not available. Model comparison features will be disabled.")

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

        .grid-4 {{
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
        }}

        .config-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
            gap: 1.5rem;
            margin: 1rem 0;
        }}

        .config-card {{
            background: var(--card-background);
            border: 1px solid var(--border-color);
            border-radius: 8px;
            overflow: hidden;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        }}

        .config-header {{
            background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
            color: white;
            padding: 0.75rem 1rem;
            font-weight: 600;
            font-size: 0.9rem;
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }}

        .config-body {{
            padding: 0;
        }}

        .compact-table {{
            width: 100%;
            border-collapse: collapse;
            font-size: 0.85rem;
        }}

        .compact-table th,
        .compact-table td {{
            padding: 0.5rem 0.75rem;
            text-align: left;
            border-bottom: 1px solid var(--border-color);
        }}

        .compact-table th {{
            background-color: #f8fafc;
            font-weight: 600;
            color: var(--text-primary);
            width: 40%;
        }}

        .compact-table td {{
            color: var(--text-secondary);
        }}

        .compact-table tr:last-child th,
        .compact-table tr:last-child td {{
            border-bottom: none;
        }}

        .compact-table tr:hover {{
            background-color: #f8fafc;
        }}

        @media (max-width: 768px) {{
            .config-grid {{
                grid-template-columns: 1fr;
                gap: 1rem;
            }}
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

        /* ZENO-Style Professional Sample Analysis */
        .zeno-sample-card {{
            background: var(--card-background);
            border: 1px solid var(--border-color);
            border-radius: 12px;
            margin: 1.5rem 0;
            overflow: hidden;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
            transition: all 0.3s ease;
        }}

        .zeno-sample-card:hover {{
            transform: translateY(-2px);
            box-shadow: 0 4px 16px rgba(0, 0, 0, 0.15);
        }}

        .zeno-sample-card.correct {{
            border-left: 5px solid var(--success-color);
        }}

        .zeno-sample-card.incorrect {{
            border-left: 5px solid var(--danger-color);
        }}

        .zeno-sample-header {{
            background: linear-gradient(135deg, #f8fafc, #e2e8f0);
            padding: 1rem 1.5rem;
            border-bottom: 1px solid var(--border-color);
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}

        .sample-status {{
            font-weight: 600;
            font-size: 1rem;
            color: var(--text-primary);
        }}

        .sample-task {{
            background: var(--primary-color);
            color: white;
            padding: 0.25rem 0.75rem;
            border-radius: 20px;
            font-size: 0.75rem;
            font-weight: 600;
            letter-spacing: 0.5px;
        }}

        .zeno-sample-content {{
            padding: 1.5rem;
        }}

        .narrative-section {{
            margin-bottom: 1.5rem;
        }}

        .narrative-text {{
            background: #f1f5f9;
            border: 2px solid #e2e8f0;
            border-radius: 12px;
            padding: 1.5rem;
            line-height: 1.7;
            font-size: 0.95rem;
            color: var(--text-primary);
            max-height: 300px;
            overflow-y: auto;
            font-family: Georgia, serif;
        }}

        .question-section {{
            margin-bottom: 1.5rem;
        }}

        .section-label {{
            color: var(--primary-color);
            font-size: 1rem;
            font-weight: 600;
            margin-bottom: 0.75rem;
            display: flex;
            align-items: center;
            gap: 0.5rem;
            border-bottom: 2px solid var(--border-color);
            padding-bottom: 0.5rem;
        }}

        .question-text {{
            background: #f8fafc;
            border: 1px solid var(--border-color);
            border-radius: 8px;
            padding: 1rem;
            line-height: 1.6;
            font-size: 0.95rem;
            color: var(--text-primary);
        }}

        .activity-badge {{
            background: linear-gradient(135deg, var(--accent-color), #f59e0b);
            color: white;
            padding: 0.5rem 1rem;
            border-radius: 20px;
            font-size: 0.8rem;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            display: inline-block;
            margin-bottom: 1rem;
            box-shadow: 0 2px 4px rgba(245, 158, 11, 0.3);
        }}

        .choices-section {{
            margin: 1.5rem 0;
        }}

        .zeno-choice-grid {{
            display: grid;
            gap: 0.75rem;
            margin-top: 1rem;
        }}

        .zeno-choice-option {{
            background: var(--card-background);
            border: 2px solid var(--border-color);
            border-radius: 10px;
            padding: 1rem;
            transition: all 0.2s ease;
            position: relative;
            overflow: hidden;
        }}

        .zeno-choice-option:hover {{
            border-color: var(--primary-color);
            transform: translateX(4px);
        }}

        .zeno-choice-option.choice-correct {{
            background: linear-gradient(135deg, #f0fdf4, #dcfce7);
            border-color: var(--success-color);
            box-shadow: 0 0 12px rgba(34, 197, 94, 0.2);
        }}

        .zeno-choice-option.choice-selected {{
            background: linear-gradient(135deg, #eff6ff, #dbeafe);
            border-color: var(--primary-color);
            box-shadow: 0 0 12px rgba(37, 99, 235, 0.2);
        }}

        .zeno-choice-option.choice-correct.choice-selected {{
            background: linear-gradient(135deg, #f0fdf4, #bbf7d0);
            border-color: var(--success-color);
            box-shadow: 0 0 16px rgba(34, 197, 94, 0.3);
        }}

        .choice-label {{
            font-weight: 700;
            font-size: 1.1rem;
            color: var(--primary-color);
            margin-bottom: 0.5rem;
            display: inline-block;
            background: rgba(37, 99, 235, 0.1);
            padding: 0.25rem 0.5rem;
            border-radius: 6px;
        }}

        .choice-text {{
            color: var(--text-primary);
            line-height: 1.5;
            margin-bottom: 0.5rem;
        }}

        .choice-indicators {{
            font-size: 0.8rem;
            font-weight: 600;
            color: var(--text-secondary);
            margin-top: 0.5rem;
            padding-top: 0.5rem;
            border-top: 1px solid rgba(0, 0, 0, 0.1);
        }}

        .direct-answer-note {{
            background: #fef3c7;
            border: 1px solid #f59e0b;
            border-radius: 8px;
            padding: 1rem;
            color: #92400e;
            font-style: italic;
            text-align: center;
        }}

        /* Enhanced Response Section Styles */
        .response-section {{
            margin: 1.5rem 0;
        }}

        .model-response {{
            background: var(--card-background);
            border: 1px solid var(--border-color);
            border-radius: 8px;
            overflow: hidden;
        }}

        .model-response.response-correct {{
            border-color: var(--success-color);
            background: linear-gradient(135deg, #f0fdf4, #dcfce7);
        }}

        .model-response.response-incorrect {{
            border-color: var(--danger-color);
            background: linear-gradient(135deg, #fef2f2, #fee2e2);
        }}

        .response-header {{
            padding: 0.75rem 1rem;
            background: rgba(0, 0, 0, 0.02);
            border-bottom: 1px solid var(--border-color);
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }}

        .response-icon {{
            font-size: 1.1rem;
        }}

        .response-status {{
            font-weight: 600;
            color: var(--text-primary);
        }}

        .response-content {{
            padding: 1rem;
            line-height: 1.5;
        }}

        /* Correct Answer Section Styles */
        .correct-answer-section {{
            margin: 1.5rem 0;
        }}

        .correct-answer {{
            background: linear-gradient(135deg, #f0fdf4, #dcfce7);
            border: 1px solid var(--success-color);
            border-radius: 8px;
            padding: 1rem;
        }}

        .answer-content {{
            line-height: 1.5;
            color: var(--text-primary);
        }}

        /* Confidence Section Styles */
        .confidence-section {{
            margin: 1.5rem 0;
        }}

        .confidence-scores {{
            background: var(--card-background);
            border: 1px solid var(--border-color);
            border-radius: 8px;
            padding: 1rem;
        }}

        .confidence-item {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 0.5rem 0;
            border-bottom: 1px solid rgba(0, 0, 0, 0.1);
        }}

        .confidence-item:last-child {{
            border-bottom: none;
        }}

        .confidence-item.selected-confidence {{
            background: rgba(37, 99, 235, 0.1);
            margin: 0 -0.5rem;
            padding: 0.5rem;
            border-radius: 6px;
            border-bottom: 1px solid rgba(37, 99, 235, 0.2);
        }}

        .conf-label {{
            font-weight: 600;
            color: var(--text-primary);
        }}

        .conf-score {{
            font-family: 'Courier New', monospace;
            background: #f8fafc;
            padding: 0.25rem 0.5rem;
            border-radius: 4px;
            font-size: 0.9rem;
        }}

        .results-section {{
            margin-top: 2rem;
            padding-top: 1.5rem;
            border-top: 2px solid var(--border-color);
        }}

        .result-item {{
            background: var(--card-background);
            border: 1px solid var(--border-color);
            border-radius: 8px;
            margin-bottom: 1rem;
            overflow: hidden;
        }}

        .result-item.correct-result {{
            border-color: var(--success-color);
            background: linear-gradient(135deg, #f0fdf4, #dcfce7);
        }}

        .result-item.incorrect-result {{
            border-color: var(--danger-color);
            background: linear-gradient(135deg, #fef2f2, #fee2e2);
        }}

        .result-item.raw-result {{
            border-color: var(--text-secondary);
            background: linear-gradient(135deg, #f8fafc, #e2e8f0);
        }}

        .result-header {{
            background: rgba(0, 0, 0, 0.03);
            padding: 0.75rem 1rem;
            border-bottom: 1px solid var(--border-color);
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }}

        .result-icon {{
            font-size: 1.2rem;
        }}

        .result-label {{
            font-weight: 600;
            color: var(--text-primary);
        }}

        .result-content {{
            padding: 1rem;
            font-size: 0.95rem;
            line-height: 1.5;
        }}

        .raw-content {{
            font-family: 'Monaco', 'Consolas', monospace;
            background: #1e293b;
            color: #e2e8f0;
            padding: 1rem;
            border-radius: 6px;
            font-size: 0.85rem;
            overflow-x: auto;
        }}

        .confidence-scores {{
            margin-top: 1rem;
            padding: 1rem;
            background: rgba(0, 0, 0, 0.02);
            border-radius: 6px;
            border: 1px solid var(--border-color);
        }}

        .confidence-scores h5 {{
            margin-bottom: 0.75rem;
            color: var(--text-primary);
            font-size: 0.9rem;
            font-weight: 600;
        }}

        .confidence-item {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 0.5rem;
            margin-bottom: 0.25rem;
            border-radius: 4px;
            background: var(--card-background);
            border: 1px solid transparent;
        }}

        .confidence-item.selected-confidence {{
            background: linear-gradient(135deg, #eff6ff, #dbeafe);
            border-color: var(--primary-color);
            font-weight: 600;
        }}

        .conf-label {{
            font-weight: 500;
            color: var(--text-primary);
        }}

        .conf-score {{
            font-family: 'Monaco', 'Consolas', monospace;
            font-size: 0.85rem;
            color: var(--text-secondary);
            background: rgba(0, 0, 0, 0.05);
            padding: 0.25rem 0.5rem;
            border-radius: 4px;
        }}

        .more-samples-note {{
            text-align: center;
            color: var(--text-secondary);
            font-style: italic;
            margin: 2rem 0;
            padding: 1rem;
            background: #f8fafc;
            border: 1px solid var(--border-color);
            border-radius: 8px;
        }}

        /* Legacy support for old styles */
        .sample-card {{
            /* Keep for backward compatibility */
        }}

        .sample-header {{
            /* Keep for backward compatibility */
        }}

        .sample-content {{
            /* Keep for backward compatibility */
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
            initializeComparison();
        }});

        function initializeCharts() {{
            // Performance overview chart
            const ctx = document.getElementById('performanceChart');
            if (ctx) {{
                const chartData = {chart_data};
                const chart = new Chart(ctx, {{
                    type: 'radar',
                    data: chartData,
                    options: {{
                        responsive: true,
                        maintainAspectRatio: false,
                        plugins: {{
                            legend: {{
                                position: 'top',
                            }},
                            title: {{
                                display: true,
                                text: 'Performance Overview - Interactive Comparison Available'
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
                
                // Store original chart data for comparison
                storeOriginalChartData(chart, chartData);
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

        {comparison_javascript}
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
    """Generate comprehensive model configuration section with space-efficient multi-column layout."""
    html = ['<div class="card">']
    html.append('<h2>⚙️ Model Configuration</h2>')
    
    # Use multi-column grid layout for space efficiency
    html.append('<div class="config-grid">')
    
    # Basic Model Information Card
    html.append('<div class="config-card">')
    html.append('<div class="config-header">🔧 Basic Model Information</div>')
    html.append('<div class="config-body">')
    html.append('<table class="compact-table">')
    
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
        html.append(f'<tr><th>{param}</th><td>{value}</td></tr>')
    
    html.append('</table>')
    html.append('</div>')
    html.append('</div>')
    
    # Hardware & Performance Configuration Card
    html.append('<div class="config-card">')
    html.append('<div class="config-header">🖥️ Hardware & Performance Configuration</div>')
    html.append('<div class="config-body">')
    html.append('<table class="compact-table">')
    
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
        html.append(f'<tr><th>{param}</th><td>{value}</td></tr>')
    
    html.append('</table>')
    html.append('</div>')
    html.append('</div>')
    
    # Advanced Features & Optimization Card
    html.append('<div class="config-card">')
    html.append('<div class="config-header">⚡ Advanced Features & Optimization</div>')
    html.append('<div class="config-body">')
    html.append('<table class="compact-table">')
    
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
        html.append(f'<tr><th>{param}</th><td>{value}</td></tr>')
    
    html.append('</table>')
    html.append('</div>')
    html.append('</div>')
    
    # Generation Parameters Card
    html.append('<div class="config-card">')
    html.append('<div class="config-header">🎯 Generation Parameters</div>')
    html.append('<div class="config-body">')
    html.append('<table class="compact-table">')
    
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
        html.append(f'<tr><th>{param}</th><td>{value}</td></tr>')
    
    html.append('</table>')
    html.append('</div>')
    html.append('</div>')
    
    # Evaluation Configuration Card
    html.append('<div class="config-card">')
    html.append('<div class="config-header">📋 Evaluation Configuration</div>')
    html.append('<div class="config-body">')
    html.append('<table class="compact-table">')
    
    eval_info = [
        ("Evaluated Tasks", model_info.get("evaluated_tasks", "Not specified")),
        ("Number of Few-shot Examples", model_info.get("num_fewshot", "Not specified")),
        ("Samples Per Task", model_info.get("samples_per_task", "All available")),
        ("Evaluation Framework", "lm-evaluation-harness"),
    ]
    
    for param, value in eval_info:
        html.append(f'<tr><th>{param}</th><td>{value}</td></tr>')
    
    html.append('</table>')
    html.append('</div>')
    html.append('</div>')
    
    # Architecture Details Card (if available)
    if model_info.get("name", "Unknown") != "Unknown":
        arch_info = get_model_architecture_info(model_info["name"])
        if arch_info.get("family", "Unknown") != "Unknown":
            html.append('<div class="config-card">')
            html.append('<div class="config-header">🏗️ Architecture Details</div>')
            html.append('<div class="config-body">')
            html.append('<table class="compact-table">')
            
            for key, value in arch_info.items():
                if key != "family":  # Skip family as it's redundant with architecture
                    display_key = key.replace("_", " ").title()
                    html.append(f'<tr><th>{display_key}</th><td>{value}</td></tr>')
            
            html.append('</table>')
            html.append('</div>')
            html.append('</div>')
    
    # Close the grid layout
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
    
    # Add model comparison controls if available
    if COMPARISON_AVAILABLE:
        try:
            available_models = get_available_comparison_models()
            comparison_html = generate_comparison_dropdown_html(available_models)
            html.append(comparison_html)
        except Exception as e:
            print(f"⚠️ Error generating comparison controls: {e}")
    
    # Add performance charts
    html.append('<div class="chart-container">')
    html.append('<canvas id="taskChart"></canvas>')
    html.append('</div>')
    
    # Performance radar chart with comparison capability
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
    """Generate sample analysis section with tabs and enhanced Zeno-style presentation."""
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
        display_name = task.replace('leaderboard_', '').replace('_', ' ').title()
        html.append(f'<button class="tab {active_class}" data-tab="task-{i}">{display_name}</button>')
    html.append('</div>')
    
    # Tab contents
    for i, (task, task_samples) in enumerate(samples.items()):
        active_class = 'active' if i == 0 else ''
        html.append(f'<div id="task-{i}" class="tab-content {active_class}">')
        
        # Detect task type for proper formatting
        is_hellaswag = 'hellaswag' in task.lower()
        is_mmlu = 'mmlu' in task.lower() 
        is_bbh = 'bbh' in task.lower()
        is_math = 'math' in task.lower()
        is_gsm8k = 'gsm8k' in task.lower()
        is_truthfulqa = 'truthfulqa' in task.lower()
        is_musr = 'musr' in task.lower()
        is_gpqa = 'gpqa' in task.lower()
        is_ifeval = 'ifeval' in task.lower()
        
        # Show up to 5 samples per task
        displayed_samples = 0
        max_samples = 5
        
        for sample in task_samples[:max_samples]:
            if displayed_samples >= max_samples:
                break
            
            # Extract all the information we need
            doc = sample.get('doc', {})
            target = sample.get('target')
            
            # Get question/context text
            question_text = ""
            narrative_text = ""
            
            if is_musr:
                # MUSR tasks have both narrative and question
                narrative_text = doc.get('narrative', '')
                question_text = doc.get('question', '')
            elif is_hellaswag:
                # HellaSwag uses ctx field
                question_text = doc.get('ctx', '') or doc.get('ctx_a', '')
                if 'ctx_b' in doc and doc['ctx_b']:
                    question_text += " " + doc['ctx_b']
            elif is_gpqa:
                # GPQA uses 'Question' field (capital Q)
                question_text = doc.get('Question', '')
            elif is_math:
                # MATH tasks use 'problem' field
                question_text = doc.get('problem', '')
            elif is_ifeval:
                # IFEVAL uses 'prompt' field
                question_text = doc.get('prompt', '')
            elif 'question' in doc:
                question_text = doc['question']
            elif 'input' in doc:
                question_text = doc['input']
            
            # Get answer choices
            choices_info = extract_choices_from_doc(doc, is_hellaswag, is_mmlu, is_bbh, is_musr, is_gpqa, is_math, is_ifeval, sample)
            choice_labels = choices_info['labels']
            choice_texts = choices_info['texts']
            
            # Determine correct answer
            correct_info = determine_correct_answer(target, choice_labels, choice_texts, doc)
            correct_choice_label = correct_info['label']
            correct_choice_text = correct_info['text']
            correct_choice_index = correct_info['index']
            
            # Determine model's answer
            model_info = determine_model_answer(sample, choice_labels, choice_texts)
            model_choice_label = model_info['label']
            model_choice_text = model_info['text'] 
            model_choice_index = model_info['index']
            model_raw_response = model_info['raw_response']
            
            # Check if correct
            is_correct = (model_choice_index == correct_choice_index) if (model_choice_index is not None and correct_choice_index is not None) else False
            
            # Generate ZENO-style sample card
            correctness_class = 'correct' if is_correct else 'incorrect'
            correctness_icon = '✅' if is_correct else '❌'
            
            html.append(f'<div class="zeno-sample-card {correctness_class}">')
            html.append(f'<div class="zeno-sample-header">')
            html.append(f'<span class="sample-status">{correctness_icon} Sample {displayed_samples + 1}</span>')
            
            # Add task-specific badges
            task_badge = task.replace('leaderboard_', '').upper()
            html.append(f'<span class="sample-task">{task_badge}</span>')
            
            # Add activity label for hellaswag
            if is_hellaswag and 'activity_label' in doc:
                html.append(f'<span class="activity-badge">{doc["activity_label"]}</span>')
            
            html.append('</div>')
            
            html.append('<div class="zeno-sample-content">')
            
            # SECTION 1: Narrative (for MUSR tasks)
            if is_musr and narrative_text:
                html.append('<div class="narrative-section">')
                html.append(f'<h4 class="section-label">📚 Narrative</h4>')
                html.append(f'<div class="narrative-text">{narrative_text}</div>')
                html.append('</div>')
            
            # SECTION 2: Question/Context
            html.append('<div class="question-section">')
            if is_musr:
                section_label = "❓ Question"
            elif is_hellaswag:
                section_label = "📖 Context"
            else:
                section_label = "❓ Question"
            html.append(f'<h4 class="section-label">{section_label}</h4>')
            if question_text:
                html.append(f'<div class="question-text">{question_text}</div>')
            else:
                html.append('<div class="question-text"><em>No question text available</em></div>')
            html.append('</div>')
            
            # SECTION 3: Answer Choices (if available)
            if choice_labels and choice_texts:
                html.append('<div class="choices-section">')
                html.append(f'<h4 class="section-label">📋 Answer Choices</h4>')
                html.append('<div class="zeno-choice-grid">')
                
                for idx, (label, text) in enumerate(zip(choice_labels, choice_texts)):
                    choice_classes = ["zeno-choice-option"]
                    choice_indicators = []
                    
                    # Highlight correct answer
                    if idx == correct_choice_index:
                        choice_classes.append("choice-correct")
                        choice_indicators.append("✓ Correct")
                    
                    # Highlight model's choice  
                    if idx == model_choice_index:
                        choice_classes.append("choice-selected")
                        choice_indicators.append("🤖 Selected")
                    
                    indicator_text = " • ".join(choice_indicators) if choice_indicators else ""
                    
                    html.append(f'<div class="{" ".join(choice_classes)}">')
                    html.append(f'<div class="choice-label">{label}</div>')
                    html.append(f'<div class="choice-text">{text}</div>')
                    if indicator_text:
                        html.append(f'<div class="choice-indicators">{indicator_text}</div>')
                    html.append('</div>')
                
                html.append('</div>')  # End zeno-choice-grid
                html.append('</div>')  # End choices-section
            elif is_math or is_ifeval:
                # For direct answer tasks, show a note
                html.append('<div class="choices-section">')
                html.append(f'<h4 class="section-label">📋 Answer Type</h4>')
                task_type = "Mathematical Expression" if is_math else "Instruction Following"
                html.append(f'<div class="direct-answer-note">This is a direct answer task ({task_type}) - no multiple choice options.</div>')
                html.append('</div>')  # End choices-section
            
            # SECTION 4: Model Response
            html.append('<div class="response-section">')
            html.append(f'<h4 class="section-label">🤖 Model Response</h4>')
            
            response_class = "response-correct" if is_correct else "response-incorrect"
            result_icon = "✅" if is_correct else "❌"
            result_status = "Correct" if is_correct else "Incorrect"
            
            html.append(f'<div class="model-response {response_class}">')
            html.append('<div class="response-header">')
            html.append(f'<span class="response-icon">{result_icon}</span>')
            html.append(f'<span class="response-status">{result_status}</span>')
            html.append('</div>')
            
            if model_choice_label and model_choice_text:
                html.append(f'<div class="response-content">')
                html.append(f'<strong>Answer:</strong> {model_choice_label} - {model_choice_text}')
                html.append('</div>')
            elif model_raw_response:
                html.append(f'<div class="response-content">')
                html.append(f'<strong>Raw Response:</strong> {model_raw_response}')
                html.append('</div>')
            else:
                html.append('<div class="response-content"><em>No response available</em></div>')
            
            html.append('</div>')
            html.append('</div>')  # End response-section
            
            # SECTION 5: Correct Answer
            html.append('<div class="correct-answer-section">')
            html.append(f'<h4 class="section-label">✅ Correct Answer</h4>')
            
            html.append('<div class="correct-answer">')
            if correct_choice_label and correct_choice_text:
                html.append(f'<div class="answer-content">')
                html.append(f'<strong>Answer:</strong> {correct_choice_label} - {correct_choice_text}')
                html.append('</div>')
            elif target:
                html.append(f'<div class="answer-content">')
                html.append(f'<strong>Target:</strong> {target}')
                html.append('</div>')
            else:
                html.append('<div class="answer-content"><em>No correct answer available</em></div>')
            html.append('</div>')
            html.append('</div>')  # End correct-answer-section
            
            # SECTION 6: Confidence Scores (if available)
            if 'filtered_resps' in sample and sample['filtered_resps'] and choice_labels:
                html.append('<div class="confidence-section">')
                html.append(f'<h4 class="section-label">📊 Model Confidence</h4>')
                html.append('<div class="confidence-scores">')
                
                for idx, resp in enumerate(sample['filtered_resps'][:len(choice_labels)]):
                    if isinstance(resp, list) and len(resp) >= 1:
                        prob = resp[0]
                        label = choice_labels[idx] if idx < len(choice_labels) else f"Option {idx+1}"
                        confidence = f"{prob:.4f}"
                        highlight = "selected-confidence" if idx == model_choice_index else ""
                        html.append(f'<div class="confidence-item {highlight}">')
                        html.append(f'<span class="conf-label">{label}:</span>')
                        html.append(f'<span class="conf-score">{confidence}</span>')
                        html.append('</div>')
                
                html.append('</div>')
                html.append('</div>')  # End confidence-section
            
            html.append('</div>')  # End zeno-sample-content
            html.append('</div>')  # End zeno-sample-card
            
            displayed_samples += 1
        
        if len(task_samples) > max_samples:
            html.append(f'<p class="more-samples-note"><em>... and {len(task_samples) - max_samples} more samples</em></p>')
        
        html.append('</div>')
    
    html.append('</div>')
    
    return '\n'.join(html)

def extract_bbh_choices_from_text(input_text: str) -> tuple:
    """Extract choices from BBH input text."""
    import re
    
    choice_texts = []
    choice_labels = []
    
    # Look for common patterns in BBH tasks
    patterns = [
        r'Options:\s*\n(.*?)(?:\n\n|\Z)',  # Options: followed by choices
        r'Answer Choices:\s*\n(.*?)(?:\n\n|\Z)',  # Answer Choices: followed by choices
        r'\n((?:(?:\([A-F]\)|[A-F]\.?)\s+.*?\n)+)',  # (A) or A. style choices
        r'\n((?:(?:- .*?\n)+))',  # - style choices
    ]
    
    for pattern in patterns:
        match = re.search(pattern, input_text, re.DOTALL | re.MULTILINE)
        if match:
            choices_section = match.group(1).strip()
            
            # Extract individual choices
            choice_lines = []
            for line in choices_section.split('\n'):
                line = line.strip()
                if line and (re.match(r'^[(-]|^[A-F][\.\)]', line) or line.startswith('-')):
                    choice_lines.append(line)
            
            if choice_lines:
                for line in choice_lines:
                    # Extract label and text
                    if re.match(r'^\([A-F]\)', line):
                        label = line[1]
                        text = line[3:].strip()
                    elif re.match(r'^[A-F][\.\)]', line):
                        label = line[0]
                        text = line[2:].strip() if line[1] == '.' else line[1:].strip()
                    elif line.startswith('- '):
                        label = chr(65 + len(choice_labels))  # A, B, C...
                        text = line[2:].strip()
                    else:
                        continue
                    
                    choice_labels.append(label)
                    choice_texts.append(text)
                break
    
    return choice_texts, choice_labels


def extract_choices_from_doc(doc: Dict, is_hellaswag: bool = False, is_mmlu: bool = False, is_bbh: bool = False, is_musr: bool = False, is_gpqa: bool = False, is_math: bool = False, is_ifeval: bool = False, sample: Dict = None) -> Dict:
    """Extract choice labels and texts from document."""
    choice_labels = []
    choice_texts = []
    
    if is_musr and 'choices' in doc:
        # MUSR choices are stored as a string representation of a list
        choices_str = doc['choices']
        try:
            # Parse the string representation of the list
            import ast
            choice_texts = ast.literal_eval(choices_str)
            choice_labels = [f"{i+1}" for i in range(len(choice_texts))]  # 1, 2, 3...
        except:
            # Fallback if parsing fails
            choice_texts = [choices_str]
            choice_labels = ["1"]
    elif is_gpqa:
        # GPQA has choice1, choice2, choice3, choice4 fields
        choices = []
        for i in range(1, 5):  # Usually 4 choices
            choice_key = f'choice{i}'
            if choice_key in doc and doc[choice_key]:
                choices.append(doc[choice_key])
        if choices:
            choice_texts = choices
            choice_labels = [chr(65 + i) for i in range(len(choices))]  # A, B, C, D
    elif is_bbh:
        # BBH tasks have choices embedded in the input text OR in arguments
        input_text = doc.get('input', '')
        choice_texts, choice_labels = extract_bbh_choices_from_text(input_text)
        
        # If no choices found in input text, check arguments field
        if not choice_texts and sample and 'arguments' in sample:
            arguments = sample.get('arguments', [])
            if arguments and len(arguments) >= 2:
                # Extract the completion text from arguments
                choice_texts = []
                for arg in arguments:
                    if len(arg) >= 2:
                        completion = arg[1]
                        if isinstance(completion, str):
                            choice_texts.append(completion.strip())
                        else:
                            choice_texts.append(str(completion).strip())
                
                if choice_texts:
                    choice_labels = [chr(65 + i) for i in range(len(choice_texts))]  # A, B, C...
    elif is_math or is_ifeval:
        # MATH and IFEVAL tasks don't have multiple choices - they're direct answer tasks
        choice_texts = []
        choice_labels = []
    elif is_hellaswag and 'endings' in doc:
        # HellaSwag uses endings
        choice_texts = doc['endings']
        choice_labels = [f"Option {i+1}" for i in range(len(choice_texts))]
    elif is_mmlu and 'options' in doc:
        # MMLU uses options
        choice_texts = doc['options']
        choice_labels = [chr(65 + i) for i in range(len(choice_texts))]  # A, B, C, D...
    elif 'choices' in doc:
        choices = doc['choices']
        if isinstance(choices, dict):
            if 'text' in choices and 'label' in choices:
                # Dictionary format: {'text': [...], 'label': [...]}
                choice_labels = choices['label']
                choice_texts = choices['text']
            elif 'text' in choices:
                choice_texts = choices['text']
                choice_labels = [chr(65 + i) for i in range(len(choice_texts))]
        elif isinstance(choices, list):
            # List format: ['option1', 'option2', ...]
            choice_texts = choices
            choice_labels = [chr(65 + i) for i in range(len(choice_texts))]
    elif 'options' in doc:
        # Generic options field
        choice_texts = doc['options']
        choice_labels = [chr(65 + i) for i in range(len(choice_texts))]
    
    return {
        'labels': choice_labels,
        'texts': choice_texts
    }

def determine_correct_answer(target, choice_labels: list, choice_texts: list, doc: Dict) -> Dict:
    """Determine the correct answer from target and choices."""
    correct_choice_label = None
    correct_choice_text = None
    correct_choice_index = None
    
    if target is not None and choice_labels and choice_texts:
        # Try to match target to choice
        if isinstance(target, str):
            # Target might be a label (A, B, C) or text
            if target in choice_labels:
                correct_choice_index = choice_labels.index(target)
                correct_choice_label = target
                correct_choice_text = choice_texts[correct_choice_index] if correct_choice_index < len(choice_texts) else ""
            elif target in choice_texts:
                correct_choice_index = choice_texts.index(target)
                correct_choice_text = target
                correct_choice_label = choice_labels[correct_choice_index] if correct_choice_index < len(choice_labels) else f"Option {correct_choice_index + 1}"
            else:
                # Try converting letter to index
                if len(target) == 1 and target.upper() in 'ABCDEFGHIJ':
                    idx = ord(target.upper()) - ord('A')
                    if idx < len(choice_labels) and idx < len(choice_texts):
                        correct_choice_index = idx
                        correct_choice_label = choice_labels[idx]
                        correct_choice_text = choice_texts[idx]
        elif isinstance(target, int):
            # Target is an index
            if 0 <= target < len(choice_labels) and target < len(choice_texts):
                correct_choice_index = target
                correct_choice_label = choice_labels[target]
                correct_choice_text = choice_texts[target]
    
    # If we couldn't parse it from choices, just use the raw target
    if correct_choice_label is None and target is not None:
        correct_choice_label = str(target)
        correct_choice_text = str(target)
    
    return {
        'label': correct_choice_label,
        'text': correct_choice_text,
        'index': correct_choice_index
    }

def determine_model_answer(sample: Dict, choice_labels: list, choice_texts: list) -> Dict:
    """Determine the model's answer from the sample data."""
    model_choice_label = None
    model_choice_text = None
    model_choice_index = None
    model_raw_response = None
    
    # Special handling for BBH tasks with arguments
    arguments = sample.get('arguments', [])
    filtered_resps = sample.get('filtered_resps', [])
    
    if arguments and filtered_resps and len(arguments) == len(filtered_resps):
        # For BBH tasks, find the argument/response with highest probability
        log_probs = []
        for resp in filtered_resps:
            if isinstance(resp, list) and len(resp) >= 1:
                log_probs.append(resp[0])  # First element is log probability
            else:
                log_probs.append(float('-inf'))
        
        if log_probs:
            # Model choice is the one with highest log probability (least negative)
            model_choice_index = log_probs.index(max(log_probs))
            
            # Get the completion from arguments
            if model_choice_index < len(arguments) and len(arguments[model_choice_index]) >= 2:
                completion = arguments[model_choice_index][1]
                if isinstance(completion, str):
                    model_choice_text = completion.strip()
                else:
                    model_choice_text = str(completion).strip()
                
                # Match to choice labels if available
                if model_choice_index < len(choice_labels):
                    model_choice_label = choice_labels[model_choice_index]
                else:
                    model_choice_label = chr(65 + model_choice_index)  # A, B, C...
    
    # Standard handling for other tasks with regular choices
    elif filtered_resps and choice_labels and choice_texts:
        log_probs = []
        for resp in filtered_resps:
            if isinstance(resp, list) and len(resp) >= 1:
                log_probs.append(resp[0])  # First element is log probability
            else:
                log_probs.append(float('-inf'))
        
        if log_probs:
            # Model choice is the one with highest log probability (least negative)
            model_choice_index = log_probs.index(max(log_probs))
            if model_choice_index < len(choice_labels) and model_choice_index < len(choice_texts):
                model_choice_label = choice_labels[model_choice_index]
                model_choice_text = choice_texts[model_choice_index]
    
    # Get raw response for fallback
    if filtered_resps:
        model_raw_response = str(filtered_resps)
        if len(model_raw_response) > 200:
            model_raw_response = model_raw_response[:200] + "..."
    elif 'resps' in sample:
        model_raw_response = str(sample['resps'])
        if len(model_raw_response) > 200:
            model_raw_response = model_raw_response[:200] + "..."
    
    return {
        'label': model_choice_label,
        'text': model_choice_text,
        'index': model_choice_index,
        'raw_response': model_raw_response
    }

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
    
    # Generate comparison JavaScript if available
    comparison_javascript = ""
    if COMPARISON_AVAILABLE:
        try:
            comparison_javascript = generate_comparison_javascript()
        except Exception as e:
            print(f"⚠️ Error generating comparison JavaScript: {e}")
    
    # Save model results for future comparison
    if COMPARISON_AVAILABLE:
        try:
            save_model_results(results_data, model_name)
        except Exception as e:
            print(f"⚠️ Error saving model results for comparison: {e}")
    
    # Generate final HTML
    template = get_html_template()
    html_content = template.format(
        model_name=model_name,
        timestamp=timestamp,
        content=content,
        chart_data=chart_data,
        task_chart_data=task_chart_data,
        comparison_javascript=comparison_javascript
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