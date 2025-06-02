# 🚀 LLM-Eval: Professional LLM Evaluation Framework

<div align="center">

![LLM Evaluation Framework](img/thumbnail.jpg)

</div>

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![PyPI version](https://badge.fury.io/py/llm-eval.svg)](https://pypi.org/project/llm-eval/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Torch 2.7+](https://img.shields.io/badge/PyTorch-2.7+-red.svg)](https://pytorch.org/)

A **professional-grade LLM evaluation framework** with beautiful HTML reports, designed for researchers, developers, and businesses who need **publication-quality evaluation results**.

## ✨ Features

🎨 **Beautiful HTML Reports** - Interactive, responsive reports with Chart.js visualizations  
📊 **Comprehensive Metrics** - Support for 50+ evaluation tasks and custom metrics  
⚡ **High Performance** - Optimized for GPU evaluation with batch processing  
🔧 **Easy Integration** - Simple Python API and CLI for seamless workflows  
📱 **Mobile-Friendly** - Responsive design for viewing reports on any device  
💼 **Business-Ready** - Professional presentation quality for client deliverables  

## 🚀 Quick Start

### Installation

```bash
pip install llm-eval
```

### CLI Usage

```bash
# Basic evaluation
llm-eval --model hf --model_name mistralai/Mistral-7B-v0.1 --tasks arc_easy --limit 100

# Multiple tasks with professional reports
llm-eval --model hf --model_name microsoft/DialoGPT-small --tasks arc_easy,hellaswag --report_format professional

# GPU-optimized evaluation
llm-eval --model hf --model_name mistralai/Mistral-7B-v0.1 --tasks mmlu --device cuda:0 --batch_size 8
```

### Python API

```python
import llm_eval

# Quick evaluation
results = llm_eval.quick_eval(
    model_name="mistralai/Mistral-7B-v0.1",
    tasks="arc_easy",
    limit=100
)

# Evaluation with automatic HTML report
results, report_path = llm_eval.quick_html_report(
    model_name="mistralai/Mistral-7B-v0.1",
    tasks="arc_easy,hellaswag",
    limit=100
)

print(f"📊 Results: {results['results']}")
print(f"📄 Report: {report_path}")
```

## 📊 Supported Tasks

- **Reasoning**: ARC, HellaSwag, PIQA, SIQA, CommonsenseQA
- **Knowledge**: MMLU, TruthfulQA, LAMBADA  
- **Math**: GSM8K, MATH, MathQA
- **Code**: HumanEval, MBPP
- **Language**: WinoGrande, SuperGLUE
- **And 35+ more tasks**

## 🎨 Sample Reports

The framework generates **publication-quality HTML reports** with:

- 📈 **Interactive Charts** - Performance visualizations with Chart.js
- 🏆 **Performance Badges** - Excellent/Good/Needs Improvement indicators  
- 📋 **Executive Summaries** - Business-ready insights and recommendations
- 🔍 **Detailed Analysis** - Sample-by-sample breakdown with A/B/C/D choice display
- 📱 **Responsive Design** - Perfect viewing on desktop, tablet, and mobile

## 💻 CLI Commands

```bash
# Main evaluation
llm-eval --model hf --model_name MODEL --tasks TASKS

# Generate reports from existing results  
llm-eval-demo --latest

# Convert JSON results to HTML
llm-eval-html results.json -o report.html

# Showcase framework capabilities
llm-eval-showcase
```

## 🔧 Requirements

- **Python**: 3.8+
- **PyTorch**: 2.7.0+ (with CUDA support recommended)
- **Memory**: 16GB+ RAM for 7B models
- **GPU**: CUDA-capable GPU recommended for optimal performance

## 📈 Use Cases

### 🔬 Research & Development
- **Model Comparison**: Compare different model architectures and sizes
- **Performance Analysis**: Detailed task-by-task breakdown and insights
- **Publication Materials**: Professional reports ready for academic papers

### 💼 Commercial Applications  
- **Client Demonstrations**: Impressive HTML reports for stakeholder presentations
- **Consulting Deliverables**: Business-ready evaluation reports and recommendations
- **Proof of Concepts**: Quick evaluation capabilities for rapid prototyping

### 🎓 Educational Use
- **Teaching Materials**: Clear examples and comprehensive documentation
- **Student Projects**: Easy-to-use evaluation framework for coursework
- **Research Training**: Professional-grade tools for academic research

## 🏗️ Advanced Usage

### Custom Evaluation Pipeline

```python
from llm_eval import evaluate_model

# Advanced evaluation with custom settings
results, output_path = evaluate_model(
    model_type="hf",
    model_name="mistralai/Mistral-7B-v0.1",
    tasks=["arc_easy", "hellaswag", "mmlu"],
    num_fewshot=5,
    batch_size=8,
    device="cuda:0",
    generate_report=True,
    report_format="professional"
)
```

### Batch Processing

```python
import llm_eval

models = [
    "mistralai/Mistral-7B-v0.1",
    "microsoft/DialoGPT-medium",
    "facebook/opt-1.3b"
]

for model in models:
    results, report = llm_eval.quick_html_report(
        model_name=model,
        tasks="arc_easy,hellaswag",
        output_dir=f"reports/{model.replace('/', '_')}"
    )
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built on top of the excellent [lm-evaluation-harness](https://github.com/EleutherAI/lm-evaluation-harness)
- Inspired by the need for professional-quality LLM evaluation reports
- Special thanks to the open-source ML community

## 📞 Contact

**Matthias De Paolis**  
- GitHub: [@mattdepaolis](https://github.com/mattdepaolis)
- Blog: [mattdepaolis.github.io/blog](https://mattdepaolis.github.io/blog/)
- HuggingFace: [@llmat](https://huggingface.co/llmat)

---

⭐ **Star this repository if you find it useful!** ⭐
