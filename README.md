# Python Assistant

A comprehensive Python development and analysis tool that provides code analysis, debugging, machine learning support, and development assistance.

## Features

### 🔍 Code Analysis
- **Basic Analysis**: Line count, function/class detection, import analysis
- **Deep Analysis**: Cyclomatic complexity, nesting depth, pattern detection
- **Issue Detection**: Performance, security, and style issues
- **Import Validation**: Check if all imports are available

### 🤖 Machine Learning Support
- **Dataset Analysis**: Comprehensive data exploration and quality assessment
- **Data Preparation**: Automated preprocessing and feature engineering
- **Model Training**: Support for regression and classification tasks
- **Visualization**: Automatic generation of plots and charts
- **Reporting**: Detailed ML analysis reports

### 🛠️ Development Tools
- **Code Execution**: Safe code execution with timeout protection
- **Code Formatting**: Automatic code formatting using best practices
- **Improvement Suggestions**: AI-powered code improvement recommendations
- **Workspace Management**: Explore and analyze entire projects

## Installation

1. Clone or download the Python Assistant
2. Install required dependencies:
```bash
pip install -r requirements.txt
```

## Quick Start

### Command Line Interface

```bash
# Analyze Python code
python -m python_assistant analyze my_script.py

# Get improvement suggestions
python -m python_assistant suggest my_script.py

# Analyze dataset for ML
python -m python_assistant ml-analyze data.csv --target price

# Train ML model
python -m python_assistant ml-train data.csv --target price --model-type regression

# Show workspace information
python -m python_assistant workspace
```

### Python API

```python
from python_assistant import PythonAssistant, MLHelper

# Initialize assistant
assistant = PythonAssistant()

# Analyze code
analysis = assistant.analyze_code("my_script.py")
print(f"Functions found: {len(analysis['functions'])}")

# Get suggestions
suggestions = assistant.suggest_improvements("my_script.py")
for suggestion in suggestions:
    print(f"- {suggestion}")

# ML analysis
ml_helper = MLHelper()
dataset_analysis = ml_helper.analyze_dataset("data.csv")
print(f"Dataset shape: {dataset_analysis['shape']}")
```

## Available Commands

### Code Analysis
- `analyze <file>` - Analyze Python code
- `suggest <file>` - Get improvement suggestions
- `format <file>` - Format Python code
- `run "<code>"` - Execute Python code

### Machine Learning
- `ml-analyze <file>` - Analyze dataset
- `ml-train <file> --target <column>` - Train ML model

### Workspace
- `workspace` - Show workspace information
- `help` - Show detailed help

## Examples

### Analyzing Your Existing Notebooks

The Python Assistant can analyze your existing machine learning notebooks:

```bash
# Analyze the Linear Regression notebook
python -m python_assistant analyze "Linear Regression/Linear_Regression_step_by_step.ipynb"

# Analyze the Logistic Regression notebook
python -m python_assistant analyze "Logistic Regression/LogisticRegression-StepByStep.ipynb"

# Analyze the car data for ML
python -m python_assistant ml-analyze "Linear Regression/car data.csv" --target price

# Analyze the leads data for ML
python -m python_assistant ml-analyze "Logistic Regression/Leads.csv" --target converted
```

### Deep Code Analysis

```bash
# Perform deep analysis with advanced metrics
python -m python_assistant analyze my_script.py --deep --output analysis.json
```

### Machine Learning Workflow

```bash
# 1. Analyze dataset
python -m python_assistant ml-analyze data.csv --target target_column

# 2. Train model
python -m python_assistant ml-train data.csv --target target_column --model-type auto

# 3. Generate comprehensive report
python -c "
from python_assistant import MLHelper
ml = MLHelper()
report = ml.generate_report('data.csv', 'target_column')
print(report)
"
```

## Project Structure

```
python_assistant/
├── __init__.py          # Main package initialization
├── assistant.py         # Core PythonAssistant class
├── code_analyzer.py     # Advanced code analysis
├── ml_helper.py         # Machine learning utilities
├── cli.py              # Command-line interface
└── __main__.py         # Module entry point
```

## Requirements

- Python 3.7+
- pandas >= 1.3.0
- numpy >= 1.21.0
- scikit-learn >= 1.0.0
- matplotlib >= 3.5.0
- seaborn >= 0.11.0
- black >= 22.0.0 (optional, for code formatting)

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is open source and available under the MIT License.

## Support

For questions, issues, or contributions, please visit the project repository or create an issue.