"""
Command-line interface for Python Assistant
"""

import argparse
import sys
import json
from pathlib import Path
from typing import Dict, Any

from .assistant import PythonAssistant
from .code_analyzer import CodeAnalyzer
from .ml_helper import MLHelper

def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(
        description="Python Assistant - A comprehensive Python development and analysis tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python -m python_assistant analyze my_script.py
  python -m python_assistant run "print('Hello, World!')"
  python -m python_assistant ml-analyze data.csv --target price
  python -m python_assistant suggest my_script.py
  python -m python_assistant format my_script.py
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Analyze command
    analyze_parser = subparsers.add_parser('analyze', help='Analyze Python code')
    analyze_parser.add_argument('file', help='Python file to analyze')
    analyze_parser.add_argument('--deep', action='store_true', help='Perform deep analysis')
    analyze_parser.add_argument('--output', '-o', help='Output file for results (JSON)')
    
    # Run command
    run_parser = subparsers.add_parser('run', help='Execute Python code')
    run_parser.add_argument('code', help='Python code to execute')
    run_parser.add_argument('--timeout', type=int, default=30, help='Timeout in seconds')
    
    # Suggest command
    suggest_parser = subparsers.add_parser('suggest', help='Get improvement suggestions')
    suggest_parser.add_argument('file', help='Python file to analyze')
    suggest_parser.add_argument('--output', '-o', help='Output file for suggestions')
    
    # Format command
    format_parser = subparsers.add_parser('format', help='Format Python code')
    format_parser.add_argument('file', help='Python file to format')
    format_parser.add_argument('--output', '-o', help='Output file for formatted code')
    
    # ML analyze command
    ml_analyze_parser = subparsers.add_parser('ml-analyze', help='Analyze dataset for ML')
    ml_analyze_parser.add_argument('file', help='Dataset file to analyze')
    ml_analyze_parser.add_argument('--target', help='Target column for ML analysis')
    ml_analyze_parser.add_argument('--output', '-o', help='Output file for results')
    
    # ML train command
    ml_train_parser = subparsers.add_parser('ml-train', help='Train ML model')
    ml_train_parser.add_argument('file', help='Dataset file')
    ml_train_parser.add_argument('--target', required=True, help='Target column')
    ml_train_parser.add_argument('--model-type', choices=['auto', 'regression', 'classification'], 
                                default='auto', help='Type of model to train')
    ml_train_parser.add_argument('--output', '-o', help='Output file for model results')
    
    # Workspace command
    workspace_parser = subparsers.add_parser('workspace', help='Show workspace information')
    workspace_parser.add_argument('--path', help='Workspace path (default: current directory)')
    
    # Help command
    help_parser = subparsers.add_parser('help', help='Show detailed help')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    if args.command == 'help':
        show_detailed_help()
        return
    
    try:
        # Initialize assistant
        workspace_path = getattr(args, 'path', None)
        assistant = PythonAssistant(workspace_path)
        code_analyzer = CodeAnalyzer()
        ml_helper = MLHelper(workspace_path)
        
        # Execute command
        result = execute_command(args, assistant, code_analyzer, ml_helper)
        
        # Output results
        if result:
            if hasattr(args, 'output') and args.output:
                output_to_file(result, args.output)
            else:
                print_result(result)
                
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

def execute_command(args, assistant: PythonAssistant, code_analyzer: CodeAnalyzer, 
                   ml_helper: MLHelper) -> Dict[str, Any]:
    """Execute the specified command"""
    
    if args.command == 'analyze':
        if args.deep:
            return code_analyzer.deep_analysis(args.file)
        else:
            return assistant.analyze_code(args.file)
    
    elif args.command == 'run':
        return assistant.run_code(args.code, args.timeout)
    
    elif args.command == 'suggest':
        suggestions = assistant.suggest_improvements(args.file)
        return {"suggestions": suggestions, "file": args.file}
    
    elif args.command == 'format':
        with open(args.file, 'r') as f:
            code = f.read()
        formatted_code = assistant.format_code(code)
        return {"formatted_code": formatted_code, "file": args.file}
    
    elif args.command == 'ml-analyze':
        result = ml_helper.analyze_dataset(args.file)
        if args.target:
            result['target_analysis'] = ml_helper.create_visualizations(args.file, args.target)
        return result
    
    elif args.command == 'ml-train':
        # Prepare data
        prepared_data = ml_helper.prepare_data(args.file, args.target)
        if "error" in prepared_data:
            return prepared_data
        
        # Train model
        model_result = ml_helper.train_model(prepared_data, args.model_type)
        return model_result
    
    elif args.command == 'workspace':
        return assistant.get_workspace_info()
    
    return {}

def output_to_file(result: Dict[str, Any], output_file: str) -> None:
    """Output results to file"""
    output_path = Path(output_file)
    
    if output_path.suffix == '.json':
        with open(output_path, 'w') as f:
            json.dump(result, f, indent=2, default=str)
    else:
        with open(output_path, 'w') as f:
            if isinstance(result, dict):
                for key, value in result.items():
                    f.write(f"{key}: {value}\n")
            else:
                f.write(str(result))

def print_result(result: Dict[str, Any]) -> None:
    """Print results to console"""
    if isinstance(result, dict):
        for key, value in result.items():
            if isinstance(value, (list, dict)):
                print(f"\n{key}:")
                if isinstance(value, list):
                    for item in value:
                        print(f"  - {item}")
                else:
                    for k, v in value.items():
                        print(f"  {k}: {v}")
            else:
                print(f"{key}: {value}")
    else:
        print(result)

def show_detailed_help():
    """Show detailed help information"""
    help_text = """
Python Assistant - Detailed Help

OVERVIEW
--------
Python Assistant is a comprehensive tool for Python development, code analysis,
and machine learning tasks. It provides various commands to help you with
code quality, debugging, and data analysis.

COMMANDS
--------

1. ANALYZE
   Analyze Python code for quality, complexity, and potential issues.
   
   Usage: python -m python_assistant analyze <file> [options]
   
   Options:
   --deep      Perform deep analysis with advanced metrics
   --output    Save results to file (JSON format)
   
   Example:
   python -m python_assistant analyze my_script.py --deep --output analysis.json

2. RUN
   Execute Python code safely with timeout protection.
   
   Usage: python -m python_assistant run "<code>" [options]
   
   Options:
   --timeout   Set timeout in seconds (default: 30)
   
   Example:
   python -m python_assistant run "print('Hello, World!')"

3. SUGGEST
   Get improvement suggestions for Python code.
   
   Usage: python -m python_assistant suggest <file> [options]
   
   Options:
   --output    Save suggestions to file
   
   Example:
   python -m python_assistant suggest my_script.py

4. FORMAT
   Format Python code using best practices.
   
   Usage: python -m python_assistant format <file> [options]
   
   Options:
   --output    Save formatted code to file
   
   Example:
   python -m python_assistant format my_script.py --output formatted.py

5. ML-ANALYZE
   Analyze datasets for machine learning tasks.
   
   Usage: python -m python_assistant ml-analyze <file> [options]
   
   Options:
   --target    Target column for ML analysis
   --output    Save results to file
   
   Example:
   python -m python_assistant ml-analyze data.csv --target price

6. ML-TRAIN
   Train machine learning models on datasets.
   
   Usage: python -m python_assistant ml-train <file> --target <column> [options]
   
   Options:
   --model-type    Type of model (auto/regression/classification)
   --output        Save model results to file
   
   Example:
   python -m python_assistant ml-train data.csv --target price --model-type regression

7. WORKSPACE
   Show information about the current workspace.
   
   Usage: python -m python_assistant workspace [options]
   
   Options:
   --path      Specify workspace path
   
   Example:
   python -m python_assistant workspace --path /path/to/project

FEATURES
--------
- Code quality analysis and metrics
- Performance and security issue detection
- Code formatting and style suggestions
- Machine learning dataset analysis
- Model training and evaluation
- Workspace exploration and management
- Comprehensive reporting and visualization

REQUIREMENTS
------------
- Python 3.7+
- pandas, numpy, scikit-learn, matplotlib, seaborn
- black (optional, for code formatting)

For more information, visit the project repository or use individual command help.
    """
    print(help_text)

if __name__ == '__main__':
    main()