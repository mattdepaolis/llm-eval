# Model Comparison Feature - Interactive Spider Web Overlay

## Overview

The model comparison feature allows you to compare performance between different models using interactive overlaid spider/radar charts. This provides a visual way to understand how different models perform across various benchmarks.

## Features

### 🎯 **Interactive Radar Chart Overlay**
- View multiple models on the same spider web chart
- Toggle between original and comparison views
- Real-time chart updates with smooth animations
- Color-coded performance lines for each model

### 📊 **Dropdown Model Selection**
- Select from previously benchmarked models
- Models automatically sorted by timestamp (most recent first)
- Clean model name and timestamp display
- Support for multiple model selection

### 🔄 **Interactive Controls**
- **Add to Comparison**: Add selected models to the comparison view
- **Clear All**: Remove all models from comparison
- **Show Comparison**: Toggle between original and comparison radar charts
- **Remove Individual Models**: Click × next to any model to remove it

### 💾 **Automatic Result Storage**
- Results automatically saved for future comparisons
- Persistent storage in `comparison_results/` directory
- Sanitized filenames for cross-platform compatibility
- JSON format for easy data exchange

## How to Use

### 1. Generate Report with Comparison
```python
import llm_testkit

# Generate report with automatic comparison feature
output_path = llm_testkit.generate_html_report_from_json(
    'results.json', 
    'comparison_report.html'
)
```

### 2. Interactive Comparison Process
1. **Open the HTML report** in your browser
2. **Navigate to "Task Performance Results"** section  
3. **Find "Compare with Previous Benchmarks"** dropdown
4. **Select models** from the dropdown menu
5. **Click "Add to Comparison"** to add them to comparison set
6. **Click "Show Comparison"** to overlay on the radar chart
7. **Toggle views** using "Show Original"/"Show Comparison" button

### 3. Visual Analysis
- **Current Model**: Bold line with larger points (always blue)
- **Comparison Models**: Thinner lines with different colors
- **Legend**: Hover to see model names and values
- **Interactive Points**: Hover over chart points for detailed values

## Technical Implementation

### File Structure
```
llm-testkit/
├── llm_testkit/
│   ├── comparison/
│   │   ├── __init__.py
│   │   └── model_comparison.py       # Core comparison functionality
│   └── reporting/
│       └── html_report_generator.py  # Enhanced with comparison
├── comparison_results/               # Auto-created storage directory
│   ├── Model_Name_20240608_143022.json
│   └── Another_Model_20240607_101545.json
└── reports/                         # Generated HTML reports
    └── comparison_report.html       # Reports with comparison features
```

### Data Storage Format
```json
{
  "model_name": "Qwen/Qwen2.5-7B-Instruct",
  "timestamp": "2024-06-08T14:54:04.123456",
  "results": {
    "leaderboard_mmlu_pro": {"acc_norm": 0.72},
    "leaderboard_gpqa_diamond": {"acc_norm": 0.45},
    "leaderboard_math_algebra_hard": {"exact_match": 0.28}
  },
  "config": {
    "model": "Qwen/Qwen2.5-7B-Instruct",
    "model_type": "hf",
    "architecture": "qwen2"
  },
  "model_info": {
    "name": "Qwen/Qwen2.5-7B-Instruct", 
    "type": "LLM",
    "architecture": "Transformer",
    "size": "7B"
  }
}
```

## Chart Visualization

### Radar Chart Overlay
- **Type**: Multi-dataset radar/spider chart
- **Axes**: Task performance (0-100% scale)
- **Lines**: Each model represented by a colored line
- **Points**: Interactive hover with exact values
- **Legend**: Model names with color coding

### Color Scheme
1. **Current Model**: `rgba(37, 99, 235, 0.6)` (Blue) - Bold
2. **Comparison Model 1**: `rgba(239, 68, 68, 0.6)` (Red)
3. **Comparison Model 2**: `rgba(16, 185, 129, 0.6)` (Green)
4. **Comparison Model 3**: `rgba(245, 158, 11, 0.6)` (Orange)
5. **Comparison Model 4**: `rgba(139, 92, 246, 0.6)` (Purple)

## API Reference

### Core Functions

#### `save_model_results(results_data, model_name)`
Automatically saves model results for future comparison.

#### `get_available_comparison_models()`
Returns list of available models for comparison.

#### `generate_comparison_chart_data(current_results, comparison_models)`
Generates Chart.js compatible data for overlaid radar chart.

#### `generate_comparison_dropdown_html(available_models)`
Creates HTML for the interactive dropdown and controls.

## Usage Examples

### Basic Comparison
```python
# Generate report (automatically saves for comparison)
report_path = llm_testkit.generate_html_report_from_json('results.json')

# Open report, select models, click "Show Comparison"
```

### Programmatic Access
```python
from llm_testkit.comparison.model_comparison import get_available_comparison_models

# Get available models
models = get_available_comparison_models()
for model in models:
    print(f"{model['model_name']} - {model['timestamp']}")
```

## Benefits

### 📈 **Performance Analysis**
- **Quick Visual Comparison**: See relative strengths and weaknesses instantly
- **Trend Analysis**: Compare models across multiple benchmarks
- **Decision Support**: Choose the best model for your use case

### 🎮 **Interactive Experience**
- **Real-time Updates**: Smooth chart transitions and animations
- **Flexible Selection**: Add/remove models as needed
- **Professional Presentation**: Publication-ready visualizations

### 🔄 **Workflow Integration**
- **Automatic Storage**: No manual data management required
- **Cross-Session Persistence**: Compare models across different evaluation runs
- **Team Collaboration**: Share results and comparisons easily

## Example Screenshot Flow

1. **Original Chart**: Single model radar chart
2. **Dropdown Selection**: Choose "GPT-3.5-Turbo" and "Claude-3-Haiku"
3. **Add to Comparison**: Click "Add to Comparison" 
4. **Show Comparison**: Toggle to overlay view
5. **Multi-Model Chart**: All models overlaid with different colors

## Limitations & Future Enhancements

### Current Limitations
- Maximum 5 comparison models for chart readability
- Task alignment based on name matching (handles different naming conventions)
- Client-side only (no server-side API yet)

### Planned Enhancements
- **Task Filtering**: Select specific tasks for comparison
- **Export Options**: PNG/PDF export of comparison charts
- **Statistical Analysis**: Add significance testing
- **Model Metadata**: Include more detailed model information
- **Performance Metrics**: Add confidence intervals and error bars

## Troubleshooting

### Common Issues

**Q: No models available for comparison**
A: Run evaluations on different models first. Each evaluation automatically saves results.

**Q: Chart not updating when adding models**
A: Ensure JavaScript is enabled. Check browser console for errors.

**Q: Model names with special characters cause issues**
A: Names are automatically sanitized for filename compatibility.

**Q: Comparison data storage location**
A: Results stored in `comparison_results/` directory in your workspace.

This feature transforms static evaluation reports into dynamic, interactive comparison tools perfect for model selection and performance analysis! 🚀 