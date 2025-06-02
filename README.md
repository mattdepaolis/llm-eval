# 🚀 LLM-Eval: Professional LLM Evaluation Framework

<div align="center">

![LLM Evaluation Framework](img/thumbnail.jpg)

</div>

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![PyPI version](https://badge.fury.io/py/llm-testkit.svg)](https://pypi.org/project/llm-testkit/)
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

### Installation Options

#### 🤖 **Automatic Installation (Recommended)**

```bash
# Install the package
pip install llm-testkit

# Auto-install PyTorch with CUDA 12.8 for optimal performance
python -c "import llm_testkit; llm_testkit.install_pytorch_for_gpu()"
```

This will:
- 🔍 Detect your GPU automatically
- 📋 Show compatibility information  
- 🚀 Install PyTorch with CUDA 12.8 (optimal for all modern GPUs)
- ✅ Verify the installation

#### 🎯 **Manual Installation**

```bash
# Install PyTorch with CUDA 12.8 support (optimal for all NVIDIA GPUs)
pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu128

# Install LLM Testkit
pip install llm-testkit
```

#### 🖥️ **Quick Installation**

```bash
# Install LLM Testkit (then manually install PyTorch CUDA 12.8)
pip install llm-testkit
```

#### 💻 **CPU-Only Installation**

```bash
# For CPU-only evaluation (no CUDA) - install PyTorch CPU version manually
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu
pip install llm-testkit
```

**🚀 Why CUDA 12.8?**
CUDA 12.8 provides the best performance and is backward compatible with all modern NVIDIA GPUs (RTX 20 series and newer). It's required for RTX 5090+ but optimizes performance for all GPUs.

#### 🔍 **Check GPU Compatibility Only**

```python
import llm_testkit

# Check what GPU you have and get installation recommendations
gpu_info = llm_testkit.check_gpu_compatibility()
print(f"GPUs detected: {gpu_info['gpus_detected']}")
print(f"Recommendation: {gpu_info['recommendation']}")
print(f"Installation command: {gpu_info['installation_command']}")
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
import llm_testkit

# Quick evaluation
results = llm_testkit.quick_eval(
    model_name="mistralai/Mistral-7B-v0.1",
    tasks="arc_easy",
    limit=100
)

# Evaluation with automatic HTML report
results, report_path = llm_testkit.quick_html_report(
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

# GPU detection and PyTorch setup
llm-eval-gpu-setup

# Generate reports from existing results  
llm-eval-demo --latest

# Convert JSON results to HTML
llm-eval-html results.json -o report.html

# Showcase framework capabilities
llm-eval-showcase
```

## 🔧 Requirements

- **Python**: 3.8+
- **PyTorch**: 2.7.0+ with CUDA 12.8 (recommended for all NVIDIA GPUs)
  - **Best Performance**: Install with `--index-url https://download.pytorch.org/whl/cu128`
- **Memory**: 16GB+ RAM for 7B models
- **GPU**: CUDA-capable GPU recommended for optimal performance
  - **CUDA 12.8**: Provides best performance for all modern NVIDIA GPUs (RTX 20 series+)
  - **RTX 5090**: Requires CUDA 12.8 (compute capability sm_120)
  - **Older GPUs**: Still benefit from CUDA 12.8 optimizations

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

## 🔧 Advanced Usage

### Custom Evaluation Pipeline

```python
from llm_testkit import evaluate_model

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

### 📋 Comprehensive Configuration Example

The enhanced LLM Testkit automatically captures **60+ configuration parameters** for detailed reporting. Here's a complete example showcasing all configuration attributes:

```python
import llm_testkit

# 🎯 Complete evaluation with all configuration options
results, report_path = llm_testkit.quick_html_report(
    # Basic Model Configuration
    model_name="mistralai/Mistral-7B-v0.1",
    model_type="vllm",  # or "hf" for HuggingFace
    
    # Evaluation Settings
    tasks="hellaswag,arc_easy,mmlu,gsm8k",
    limit=500,  # samples per task
    
    # Performance & Hardware Configuration
    tensor_parallel_size=2,           # Multi-GPU setup
    gpu_memory_utilization=0.8,       # GPU memory usage
    batch_size=16,                    # Batch processing
    device="cuda",                    # Device selection
    
    # Generation Parameters
    temperature=0.7,                  # Sampling temperature
    top_p=0.9,                       # Nucleus sampling
    top_k=50,                        # Top-k sampling
    max_new_tokens=512,              # Max output length
    do_sample=True,                  # Enable sampling
    repetition_penalty=1.1,          # Prevent repetition
    
    # Advanced Model Configuration
    dtype="auto",                    # Data type optimization
    trust_remote_code=True,          # Enable custom code
    use_flash_attention_2=True,      # Flash attention optimization
    
    # Quantization (for HuggingFace models)
    quantize=True,                   # Enable quantization
    quantization_method="4bit",      # 4-bit quantization
    
    # vLLM Specific Settings
    max_model_len=4096,             # Context length
    swap_space=4,                   # Swap space (GB)
    enable_prefix_caching=True,     # Prefix caching
    
    # Evaluation Configuration
    num_fewshot=0,                  # Few-shot examples
    preserve_default_fewshot=False, # Use task defaults
    
    # Output Settings
    output_dir="comprehensive_reports",
    generate_report=True,
    report_format="professional"
)

print(f"📊 Comprehensive evaluation completed!")
print(f"📄 Professional report: {report_path}")
```

### 📈 What Gets Captured Automatically

The enhanced framework automatically extracts and displays **all configuration details** in beautiful HTML reports:

#### 🔧 **Basic Model Information**
```python
# Automatically detected and displayed:
{
    "name": "mistralai/Mistral-7B-v0.1",
    "architecture": "Mistral (Transformer)", 
    "parameters": "~7 billion",
    "context_length": "32,768 tokens",
    "backend": "VLLM",
    "quantization": "4-bit",
    "data_type": "auto"
}
```

#### 🖥️ **Hardware & Performance Configuration**
```python
# Multi-GPU and performance settings:
{
    "device_mapping": "Multi-GPU (TP=2)",
    "tensor_parallel_size": 2,
    "gpu_memory_utilization": "0.80",
    "max_model_len": "4096",
    "batch_size": "16",
    "evaluation_device": "cuda"
}
```

#### ⚡ **Advanced Features & Optimization**
```python
# Advanced model features captured:
{
    "attention_implementation": "flash_attention_2",
    "use_flash_attention": "True",
    "trust_remote_code": "True",
    "enable_prefix_caching": "True",
    "swap_space": "4 GB",
    "use_cache": "True"
}
```

#### 🎯 **Generation Parameters**
```python
# All generation settings tracked:
{
    "temperature": "0.7",
    "top_p": "0.9", 
    "top_k": "50",
    "max_new_tokens": "512",
    "do_sample": "True",
    "repetition_penalty": "1.1",
    "num_beams": "1"
}
```

#### 🏗️ **Architecture Details**
```python
# Model family specific information:
{
    "family": "Mistral",
    "attention": "Grouped-query attention (GQA) with sliding window",
    "activation": "SwiGLU", 
    "positional_encoding": "RoPE (Rotary Position Embedding)",
    "vocab_size": "32,000",
    "special_features": "Sliding window attention (4096 tokens)"
}
```

### 🎨 Enhanced HTML Reports

The comprehensive configuration example above generates **professional HTML reports** with:

- **📋 Executive Summary** - Overall performance with badges and insights
- **⚙️ Model Configuration** - 6 detailed sections with 60+ parameters:
  - Basic Model Information
  - Hardware & Performance Configuration  
  - Advanced Features & Optimization
  - Generation Parameters
  - Evaluation Configuration
  - Architecture Details
- **📊 Performance Charts** - Interactive radar and bar charts
- **🔍 Sample Analysis** - Detailed per-task breakdowns with proper HellaSwag context display
- **📱 Responsive Design** - Perfect on desktop, tablet, and mobile

### 🚀 Production-Ready Example

For production use with maximum performance:

```python
import llm_testkit

# Production evaluation with optimal settings
results, report_path = llm_testkit.quick_html_report(
    model_name="mistralai/Mistral-7B-v0.1",
    model_type="vllm", 
    tasks="hellaswag,arc_easy,mmlu,truthfulqa",
    
    # High-performance configuration
    tensor_parallel_size=4,           # 4-GPU setup
    gpu_memory_utilization=0.95,      # Max GPU usage
    batch_size=32,                    # Large batches
    max_model_len=8192,              # Extended context
    
    # Optimized generation
    temperature=0.0,                  # Deterministic
    max_new_tokens=256,              # Efficient generation
    enable_prefix_caching=True,       # Speed optimization
    
    # Professional reporting
    limit=1000,                       # Comprehensive evaluation
    report_format="professional",
    output_dir="production_reports"
)

print(f"🎯 Production evaluation complete: {report_path}")
```

**Key Benefits:**
- ✅ **Zero Configuration Loss** - All 60+ parameters automatically captured
- ✅ **Professional Reporting** - Publication-ready HTML with detailed sections  
- ✅ **Architecture Intelligence** - Automatic model family detection and optimization
- ✅ **Performance Optimization** - GPU validation and memory management
- ✅ **Complete Traceability** - Full configuration tracking for reproducibility

### Batch Processing

```python
import llm_testkit

models = [
    "mistralai/Mistral-7B-v0.1",
    "microsoft/DialoGPT-medium",
    "facebook/opt-1.3b"
]

for model in models:
    results, report = llm_testkit.quick_html_report(
        model_name=model,
        tasks="arc_easy,hellaswag",
        output_dir=f"reports/{model.replace('/', '_')}"
    )
```

## 🔧 Troubleshooting

### CUDA Compatibility Issues

**Problem**: Getting a warning like:
```
NVIDIA GeForce RTX 5090 with CUDA capability sm_120 is not compatible with the current PyTorch installation.
The current PyTorch install supports CUDA capabilities sm_50 sm_60 sm_70 sm_75 sm_80 sm_86 sm_90.
```

**Solution**: Install PyTorch with CUDA 12.8 support:
```bash
pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu128
```

**Why CUDA 12.8 for Everyone?**
- ✅ **Required for RTX 5090+**: Only CUDA 12.8 supports compute capability sm_120
- ✅ **Optimal for all GPUs**: Provides best performance even for older GPUs  
- ✅ **Backward Compatible**: Works with RTX 20 series and newer
- ✅ **Latest Optimizations**: Most recent performance improvements from NVIDIA

### Memory Issues

**Problem**: Out of memory errors during evaluation.

**Solutions**:
- Reduce `batch_size` parameter
- Use quantization: `quantize=True, quantization_method="4bit"`
- For vLLM: reduce `gpu_memory_utilization` (default 0.9)
- Use tensor parallelism across multiple GPUs

### Performance Optimization

**For maximum performance**:
- Use vLLM backend for inference: `model_type="vllm"`
- Enable tensor parallelism: `tensor_parallel_size=2` (or higher)
- Use Flash Attention: `use_flash_attention_2=True`
- Optimize memory: `gpu_memory_utilization=0.95`

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
