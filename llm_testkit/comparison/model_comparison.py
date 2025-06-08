#!/usr/bin/env python3
"""
Model comparison functionality for llm-testkit.
Allows comparing performance between different models using overlaid spider/radar charts.
"""

import json
import os
import glob
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime

def get_comparison_results_dir() -> str:
    """Get the directory for storing comparison results."""
    reports_dir = os.path.join(os.getcwd(), 'comparison_results')
    os.makedirs(reports_dir, exist_ok=True)
    return reports_dir

def save_model_results(results_data: Dict[str, Any], model_name: str) -> str:
    """Save model results for future comparison."""
    comparison_dir = get_comparison_results_dir()
    
    # Extract key information for comparison
    comparison_data = {
        'model_name': model_name,
        'timestamp': datetime.now().isoformat(),
        'results': results_data.get('results', {}),
        'config': results_data.get('config', {}),
        'model_info': extract_model_info_for_comparison(results_data.get('config', {}))
    }
    
    # Save with timestamp to avoid conflicts
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    # Sanitize model name for filename
    safe_model_name = model_name.replace('/', '_').replace('\\', '_').replace(':', '_')
    filename = f"{safe_model_name}_{timestamp}.json"
    filepath = os.path.join(comparison_dir, filename)
    
    with open(filepath, 'w') as f:
        json.dump(comparison_data, f, indent=2)
    
    print(f"✅ Model results saved for comparison: {filepath}")
    return filepath

def extract_model_info_for_comparison(config: Dict[str, Any]) -> Dict[str, str]:
    """Extract essential model info for comparison display."""
    return {
        'name': config.get('model', 'Unknown Model'),
        'type': config.get('model_type', 'Unknown'),
        'architecture': config.get('architecture', 'Unknown'),
        'size': config.get('model_size', 'Unknown')
    }

def get_available_comparison_models() -> List[Dict[str, Any]]:
    """Get list of available models for comparison."""
    comparison_dir = get_comparison_results_dir()
    pattern = os.path.join(comparison_dir, "*.json")
    files = glob.glob(pattern)
    
    models = []
    for file_path in sorted(files, key=os.path.getmtime, reverse=True):  # Most recent first
        try:
            with open(file_path, 'r') as f:
                data = json.load(f)
            
            # Get file modification time for display
            mtime = os.path.getmtime(file_path)
            timestamp = datetime.fromtimestamp(mtime).strftime('%Y-%m-%d %H:%M')
            
            models.append({
                'file_path': file_path,
                'model_name': data.get('model_name', 'Unknown'),
                'timestamp': timestamp,
                'model_info': data.get('model_info', {}),
                'data': data
            })
        except (json.JSONDecodeError, KeyError) as e:
            print(f"⚠️ Skipping invalid comparison file {file_path}: {e}")
            continue
    
    return models

def generate_comparison_chart_data(current_results: Dict[str, Any], comparison_models: List[Dict[str, Any]] = None) -> str:
    """Generate chart data for model comparison with radar chart overlay."""
    
    if comparison_models is None:
        comparison_models = []
    
    # Extract current model performance
    current_metrics = current_results.get('results', {})
    current_scores = extract_task_scores(current_metrics)
    
    if not current_scores:
        return '{}'
    
    # Colors for different models
    colors = [
        'rgba(37, 99, 235, 0.6)',   # Blue - Current model
        'rgba(239, 68, 68, 0.6)',   # Red
        'rgba(16, 185, 129, 0.6)',  # Green
        'rgba(245, 158, 11, 0.6)',  # Orange
        'rgba(139, 92, 246, 0.6)',  # Purple
        'rgba(236, 72, 153, 0.6)',  # Pink
    ]
    
    border_colors = [
        'rgb(37, 99, 235)',
        'rgb(239, 68, 68)',
        'rgb(16, 185, 129)',
        'rgb(245, 158, 11)',
        'rgb(139, 92, 246)',
        'rgb(236, 72, 153)',
    ]
    
    # Get task labels (use current model's tasks as reference)
    task_labels = list(current_scores.keys())
    
    # Create datasets
    datasets = []
    
    # Current model (always first)
    current_model_name = extract_model_info_for_comparison(current_results.get('config', {}))['name']
    datasets.append({
        'label': f"{current_model_name} (Current)",
        'data': [current_scores.get(task, 0) for task in task_labels],
        'borderColor': border_colors[0],
        'backgroundColor': colors[0],
        'borderWidth': 3,
        'pointRadius': 5,
        'pointHoverRadius': 7
    })
    
    # Comparison models
    for i, model in enumerate(comparison_models[:5]):  # Limit to 5 comparison models
        model_data = model.get('data', {})
        model_metrics = model_data.get('results', {})
        model_scores = extract_task_scores(model_metrics)
        
        # Align scores with current model's tasks
        aligned_scores = []
        for task in task_labels:
            # Try to find matching task (handle different naming conventions)
            score = find_matching_task_score(task, model_scores)
            aligned_scores.append(score)
        
        color_index = (i + 1) % len(colors)
        datasets.append({
            'label': model.get('model_name', f'Model {i+1}'),
            'data': aligned_scores,
            'borderColor': border_colors[color_index],
            'backgroundColor': colors[color_index],
            'borderWidth': 2,
            'pointRadius': 4,
            'pointHoverRadius': 6
        })
    
    chart_data = {
        'labels': [format_task_label(task) for task in task_labels],
        'datasets': datasets
    }
    
    return json.dumps(chart_data)

def extract_task_scores(metrics: Dict[str, Any]) -> Dict[str, float]:
    """Extract task scores from metrics."""
    task_scores = {}
    for task, task_metrics in metrics.items():
        for metric_name, value in task_metrics.items():
            if 'acc' in metric_name.lower() and 'stderr' not in metric_name.lower():
                if isinstance(value, (int, float)):
                    task_scores[task] = value * 100
                    break
        
        # Fallback for non-accuracy metrics
        if task not in task_scores:
            for metric_name, value in task_metrics.items():
                if isinstance(value, (int, float)) and 'stderr' not in metric_name.lower():
                    # Normalize to 0-100 scale if needed
                    score = value * 100 if value <= 1 else value
                    task_scores[task] = min(score, 100)  # Cap at 100
                    break
    
    return task_scores

def find_matching_task_score(target_task: str, model_scores: Dict[str, float]) -> float:
    """Find matching task score, handling different naming conventions."""
    # Direct match
    if target_task in model_scores:
        return model_scores[target_task]
    
    # Try normalized matching
    target_normalized = normalize_task_name(target_task)
    for task, score in model_scores.items():
        if normalize_task_name(task) == target_normalized:
            return score
    
    # No match found
    return 0.0

def normalize_task_name(task_name: str) -> str:
    """Normalize task name for matching."""
    return task_name.lower().replace('leaderboard_', '').replace('_', '').replace('-', '')

def format_task_label(task_name: str) -> str:
    """Format task name for display in charts."""
    # Remove leaderboard prefix and format nicely
    formatted = task_name.replace('leaderboard_', '').replace('_', ' ').title()
    
    # Special formatting for known tasks
    if 'bbh' in formatted.lower():
        formatted = formatted.replace('Bbh ', 'BBH ')
    if 'mmlu' in formatted.lower():
        formatted = formatted.replace('Mmlu', 'MMLU')
    if 'gpqa' in formatted.lower():
        formatted = formatted.replace('Gpqa', 'GPQA')
    if 'musr' in formatted.lower():
        formatted = formatted.replace('Musr', 'MUSR')
    
    return formatted

def generate_comparison_dropdown_html(available_models: List[Dict[str, Any]]) -> str:
    """Generate HTML for the model comparison dropdown."""
    if not available_models:
        return '''
        <div class="comparison-section" style="margin-bottom: 1rem;">
            <div class="comparison-info">
                <p style="color: var(--text-secondary); font-style: italic;">
                    📊 No previous benchmarks available for comparison. 
                    Run evaluations on other models to enable comparison features.
                </p>
            </div>
        </div>
        '''
    
    html = ['<div class="comparison-section" style="margin-bottom: 1rem;">']
    html.append('<div class="comparison-controls">')
    html.append('<label for="comparisonSelect" style="display: block; margin-bottom: 0.5rem; font-weight: 600;">📊 Compare with Previous Benchmarks:</label>')
    html.append('<div style="display: flex; gap: 1rem; align-items: center; flex-wrap: wrap;">')
    
    # Dropdown for model selection
    html.append('<select id="comparisonSelect" style="padding: 0.5rem; border: 1px solid var(--border-color); border-radius: 6px; background: white; min-width: 250px;">')
    html.append('<option value="">Select models to compare...</option>')
    
    for model in available_models:
        model_name = model.get('model_name', 'Unknown')
        timestamp = model.get('timestamp', '')
        file_path = model.get('file_path', '')
        
        html.append(f'<option value="{file_path}">{model_name} ({timestamp})</option>')
    
    html.append('</select>')
    
    # Control buttons
    html.append('<button id="addComparison" style="padding: 0.5rem 1rem; background: var(--primary-color); color: white; border: none; border-radius: 6px; cursor: pointer;">Add to Comparison</button>')
    html.append('<button id="clearComparisons" style="padding: 0.5rem 1rem; background: var(--danger-color); color: white; border: none; border-radius: 6px; cursor: pointer;">Clear All</button>')
    html.append('<button id="toggleComparison" style="padding: 0.5rem 1rem; background: var(--accent-color); color: white; border: none; border-radius: 6px; cursor: pointer;">Show Comparison</button>')
    
    html.append('</div>')
    
    # Selected models display
    html.append('<div id="selectedModels" style="margin-top: 1rem;"></div>')
    
    html.append('</div>')
    html.append('</div>')
    
    return '\n'.join(html)

def generate_comparison_javascript() -> str:
    """Generate JavaScript for comparison functionality."""
    return '''
    // Model comparison functionality
    let comparisonModels = [];
    let originalChartData = null;
    let performanceChart = null;
    let comparisonMode = false;

    function initializeComparison() {
        const addBtn = document.getElementById('addComparison');
        const clearBtn = document.getElementById('clearComparisons');
        const toggleBtn = document.getElementById('toggleComparison');
        const select = document.getElementById('comparisonSelect');

        if (addBtn) {
            addBtn.addEventListener('click', addSelectedModel);
        }
        if (clearBtn) {
            clearBtn.addEventListener('click', clearAllComparisons);
        }
        if (toggleBtn) {
            toggleBtn.addEventListener('click', toggleComparisonMode);
        }
    }

    async function addSelectedModel() {
        const select = document.getElementById('comparisonSelect');
        const filePath = select.value;
        
        if (!filePath) {
            alert('Please select a model to add to comparison.');
            return;
        }

        try {
            // Load model data (in a real implementation, this would be an API call)
            const modelData = await loadModelData(filePath);
            
            if (modelData && !comparisonModels.find(m => m.file_path === filePath)) {
                comparisonModels.push({
                    file_path: filePath,
                    model_name: modelData.model_name,
                    data: modelData
                });
                
                updateSelectedModelsDisplay();
                updateComparisonChart();
                
                // Reset selection
                select.value = '';
            }
        } catch (error) {
            console.error('Error loading model data:', error);
            alert('Error loading model data. Please check the file.');
        }
    }

    function clearAllComparisons() {
        comparisonModels = [];
        updateSelectedModelsDisplay();
        if (comparisonMode) {
            resetToOriginalChart();
        }
    }

    function toggleComparisonMode() {
        const toggleBtn = document.getElementById('toggleComparison');
        
        if (comparisonMode) {
            resetToOriginalChart();
            toggleBtn.textContent = 'Show Comparison';
            toggleBtn.style.background = 'var(--accent-color)';
        } else {
            if (comparisonModels.length === 0) {
                alert('Please add some models to compare first.');
                return;
            }
            updateComparisonChart();
            toggleBtn.textContent = 'Show Original';
            toggleBtn.style.background = 'var(--success-color)';
        }
        
        comparisonMode = !comparisonMode;
    }

    function updateSelectedModelsDisplay() {
        const container = document.getElementById('selectedModels');
        if (!container) return;

        if (comparisonModels.length === 0) {
            container.innerHTML = '';
            return;
        }

        let html = '<div style="margin-top: 0.5rem;"><strong>Selected for comparison:</strong></div>';
        html += '<div style="display: flex; flex-wrap: wrap; gap: 0.5rem; margin-top: 0.5rem;">';
        
        comparisonModels.forEach((model, index) => {
            html += `
                <span style="background: var(--background-color); padding: 0.25rem 0.5rem; border-radius: 4px; border: 1px solid var(--border-color); font-size: 0.9rem; display: flex; align-items: center; gap: 0.25rem;">
                    ${model.model_name}
                    <button onclick="removeComparisonModel(${index})" style="background: var(--danger-color); color: white; border: none; border-radius: 50%; width: 18px; height: 18px; cursor: pointer; font-size: 0.7rem; display: flex; align-items: center; justify-content: center;">×</button>
                </span>
            `;
        });
        
        html += '</div>';
        container.innerHTML = html;
    }

    function removeComparisonModel(index) {
        comparisonModels.splice(index, 1);
        updateSelectedModelsDisplay();
        if (comparisonMode) {
            updateComparisonChart();
        }
    }

    function updateComparisonChart() {
        if (!performanceChart) return;

        // In a real implementation, this would generate the comparison chart data
        // For now, we'll simulate it
        const comparisonData = generateComparisonChartData();
        
        performanceChart.data = comparisonData;
        performanceChart.update('none');
    }

    function resetToOriginalChart() {
        if (!performanceChart || !originalChartData) return;
        
        performanceChart.data = originalChartData;
        performanceChart.update('none');
    }

    function generateComparisonChartData() {
        // This would be replaced with actual data from the server/API
        // For demonstration, we'll create sample comparison data
        
        const colors = [
            'rgba(37, 99, 235, 0.6)',   // Blue - Current
            'rgba(239, 68, 68, 0.6)',   // Red
            'rgba(16, 185, 129, 0.6)',  // Green
            'rgba(245, 158, 11, 0.6)',  // Orange
            'rgba(139, 92, 246, 0.6)',  // Purple
        ];
        
        const borderColors = [
            'rgb(37, 99, 235)',
            'rgb(239, 68, 68)',
            'rgb(16, 185, 129)',
            'rgb(245, 158, 11)',
            'rgb(139, 92, 246)',
        ];

        const datasets = [];
        
        // Add current model (preserved from original)
        if (originalChartData && originalChartData.datasets && originalChartData.datasets[0]) {
            const currentDataset = {...originalChartData.datasets[0]};
            currentDataset.label += ' (Current)';
            currentDataset.borderWidth = 3;
            currentDataset.pointRadius = 5;
            datasets.push(currentDataset);
        }

        // Add comparison models with sample data
        comparisonModels.forEach((model, index) => {
            const colorIndex = (index + 1) % colors.length;
            const originalData = originalChartData.datasets[0].data;
            
            // Generate sample comparison data (in real implementation, this comes from model.data)
            const comparisonData = originalData.map(value => {
                const variation = (Math.random() - 0.5) * 20; // ±10% variation
                return Math.max(0, Math.min(100, value + variation));
            });

            datasets.push({
                label: model.model_name,
                data: comparisonData,
                borderColor: borderColors[colorIndex],
                backgroundColor: colors[colorIndex],
                borderWidth: 2,
                pointRadius: 4,
                pointHoverRadius: 6
            });
        });

        return {
            labels: originalChartData.labels,
            datasets: datasets
        };
    }

    // Mock function to simulate loading model data
    async function loadModelData(filePath) {
        // In a real implementation, this would make an API call
        // For demonstration, we'll return mock data
        return new Promise((resolve) => {
            setTimeout(() => {
                resolve({
                    model_name: `Model ${Math.floor(Math.random() * 1000)}`,
                    timestamp: new Date().toISOString(),
                    results: {},
                    config: {}
                });
            }, 100);
        });
    }

    // Store original chart data when chart is created
    function storeOriginalChartData(chart, data) {
        performanceChart = chart;
        originalChartData = JSON.parse(JSON.stringify(data));
    }
    '''