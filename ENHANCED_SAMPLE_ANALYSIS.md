# Enhanced Sample Analysis - Zeno ML Style

## Overview

The sample analysis section has been enhanced to provide a comprehensive, Zeno ML-inspired presentation of evaluation results. Each sample now includes clearly separated sections that make it easy to understand the question, choices, model response, and correct answer.

## Enhanced Features

### 🎯 **Clear Section Separation**

Each sample is now organized into distinct sections:

1. **📚 Narrative Section** (MUSR tasks only)
   - Shows the full story/narrative context for MUSR tasks
   - Styled with special formatting for better readability
   - Scrollable for long narratives with preserved formatting

2. **📖 Question/Context Section**
   - Shows the question text for most tasks
   - Shows context for HellaSwag tasks
   - Shows specific question for MUSR tasks (after narrative)  
   - Handles different question field names (`question`, `input`, `problem`, etc.)

3. **📋 Answer Choices Section**
   - Displays all available answer choices clearly
   - Shows choice labels (A, B, C, D) and full text
   - Highlights the correct answer with ✓ indicator
   - Highlights the model's selection with 🤖 indicator
   - Supports multiple choice formats (dict, list, endings for HellaSwag, etc.)

4. **🤖 Model Response Section**
   - Shows the model's selected answer
   - Clearly indicates if the response is correct ✅ or incorrect ❌
   - Displays both choice label and full text
   - Falls back to raw response if parsing fails

5. **✅ Correct Answer Section**
   - Shows the correct answer clearly
   - Displays both choice label and full text
   - Handles different target formats (letters, indices, text)

6. **📊 Model Confidence Section** (when available)
   - Shows confidence scores for each choice
   - Highlights the model's selected choice
   - Uses monospace font for precise score display

### 🎨 **Zeno ML-Style Visual Design**

- **Professional Cards**: Each sample is displayed in a well-designed card with hover effects
- **Color Coding**: 
  - Green border for correct samples
  - Red border for incorrect samples
  - Green highlighting for correct answers
  - Blue highlighting for model selections
- **Clear Typography**: Section headers with icons and consistent styling
- **Responsive Layout**: Clean grid layout for choices and sections

### 🔧 **Enhanced Task Detection**

The system now properly detects and handles **ALL** task types in your evaluation:

- **📚 MUSR (Multi-Step Reasoning)**: Uses `narrative` for story context, `question` for the specific question, and parses `choices` string format with numbered labels (1, 2, 3)
- **📋 MMLU**: Uses `question` field and `options` list with lettered labels (A, B, C, D)
- **🧠 BBH (Big Bench Hard)**: Uses `input` field with embedded choice extraction from text patterns
- **🔬 GPQA**: Uses `Question` field (capital Q) and `choice1`, `choice2`, `choice3`, `choice4` fields with lettered labels
- **📐 MATH**: Uses `problem` field with direct answer (no multiple choices) - shows as "Mathematical Expression" task
- **📝 IFEVAL**: Uses `prompt` field with direct scoring (no multiple choices) - shows as "Instruction Following" task
- **✨ HellaSwag**: Uses `ctx` fields and `endings` for choices
- **✨ TruthfulQA**: Uses standard `question` and `choices` format
- **✨ GSM8K**: Uses math word problems with step-by-step solutions

### 📊 **Better Choice Handling**

Supports multiple choice formats:
- Dictionary format: `{'text': [...], 'label': [...]}`
- List format: `['option1', 'option2', ...]`
- MUSR string format: `"['choice1', 'choice2', 'choice3']"` (parsed with ast.literal_eval)
- HellaSwag endings: `endings` field
- MMLU options: `options` field
- Automatic label generation (A, B, C, D... or 1, 2, 3... for MUSR)

### 🎯 **Improved Answer Matching**

Enhanced logic for matching model responses to correct answers:
- Handles string targets (labels or full text)
- Handles integer targets (indices)
- Handles letter conversion (A → 0, B → 1, etc.)
- Uses log probabilities to determine model's choice
- Fallback to raw response display when parsing fails

## Usage

The enhanced sample analysis is automatically used when generating HTML reports:

```python
import llm_testkit

# Generate report with enhanced sample analysis
llm_testkit.generate_html_report_from_json(
    "results.json", 
    "enhanced_report.html"
)
```

## Example Output Structure

Each sample card contains:

```
┌─────────────────────────────────────────┐
│ ✅ Sample 1      MUSR_OBJECT_PLACEMENTS │
├─────────────────────────────────────────┤
│ 📚 Narrative                           │
│ [Long story context about studio       │
│  with Ricky, Emma, and Danny...]       │
│                                         │
│ ❓ Question                             │
│ Which location is the most likely      │
│ place Danny would look to find the     │
│ earphones given the story?             │
│                                         │
│ 📋 Answer Choices                       │
│ 1: piano                               │
│ 2: producer's desk      ✓ Correct      │
│                        🤖 Selected     │
│ 3: recording booth                     │
│                                         │
│ 🤖 Model Response                       │
│ ✅ Correct                             │
│ Answer: 2 - producer's desk            │
│                                         │
│ ✅ Correct Answer                       │
│ Answer: 2 - producer's desk            │
│                                         │
│ 📊 Model Confidence                     │
│ 1: -19.25                              │
│ 2: -16.50     ← Selected               │
│ 3: -20.00                              │
└─────────────────────────────────────────┘
```

## Benefits

1. **Better Understanding**: Clear separation makes it easy to understand each component
2. **Quick Analysis**: Visual indicators help quickly identify correct/incorrect responses
3. **Professional Presentation**: Suitable for reports, presentations, and analysis
4. **Comprehensive Data**: Shows all relevant information in one place
5. **Zeno ML Compatibility**: Similar to the professional analysis tools you're familiar with

## Technical Details

The enhanced sample analysis is implemented in:
- `llm_testkit/reporting/html_report_generator.py`
- New functions: `extract_choices_from_doc()`, `determine_correct_answer()`, `determine_model_answer()`
- Enhanced CSS styling for professional appearance
- Comprehensive task type detection and handling 