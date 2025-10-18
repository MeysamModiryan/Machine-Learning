#!/usr/bin/env python3
"""
Example usage of Python Assistant
"""

from python_assistant import PythonAssistant, MLHelper, CodeAnalyzer

def main():
    print("🐍 Python Assistant - Example Usage\n")
    
    # Initialize assistants
    assistant = PythonAssistant()
    ml_helper = MLHelper()
    code_analyzer = CodeAnalyzer()
    
    print("1. Workspace Information")
    print("=" * 30)
    workspace_info = assistant.get_workspace_info()
    print(f"Workspace: {workspace_info['workspace_path']}")
    print(f"Python files: {len(workspace_info['python_files'])}")
    print(f"Notebook files: {len(workspace_info['notebook_files'])}")
    print(f"Data files: {len(workspace_info['data_files'])}")
    print()
    
    # Analyze existing notebooks if they exist
    notebook_files = [
        "Linear Regression/Linear_Regression_step_by_step.ipynb",
        "Logistic Regression/LogisticRegression-StepByStep.ipynb"
    ]
    
    for notebook in notebook_files:
        try:
            print(f"2. Analyzing {notebook}")
            print("=" * 30)
            analysis = assistant.analyze_code(notebook)
            if "error" not in analysis:
                print(f"Lines of code: {analysis['lines_of_code']}")
                print(f"Functions: {len(analysis['functions'])}")
                print(f"Classes: {len(analysis['classes'])}")
                print(f"Imports: {len(analysis['imports'])}")
            else:
                print(f"Note: {analysis['error']}")
            print()
        except Exception as e:
            print(f"Could not analyze {notebook}: {e}")
            print()
    
    # Analyze data files
    data_files = [
        "Linear Regression/car data.csv",
        "Logistic Regression/Leads.csv"
    ]
    
    for data_file in data_files:
        try:
            print(f"3. Analyzing {data_file}")
            print("=" * 30)
            analysis = ml_helper.analyze_dataset(data_file)
            if "error" not in analysis:
                print(f"Shape: {analysis['shape']}")
                print(f"Columns: {len(analysis['columns'])}")
                print(f"Numeric columns: {len(analysis['numeric_columns'])}")
                print(f"Categorical columns: {len(analysis['categorical_columns'])}")
                print(f"Missing values: {sum(analysis['missing_values'].values())}")
                
                if analysis['suggestions']:
                    print("Suggestions:")
                    for suggestion in analysis['suggestions']:
                        print(f"  - {suggestion}")
            else:
                print(f"Error: {analysis['error']}")
            print()
        except Exception as e:
            print(f"Could not analyze {data_file}: {e}")
            print()
    
    # Example code execution
    print("4. Code Execution Example")
    print("=" * 30)
    example_code = """
import pandas as pd
import numpy as np

# Create sample data
data = {'x': [1, 2, 3, 4, 5], 'y': [2, 4, 6, 8, 10]}
df = pd.DataFrame(data)

print("Sample DataFrame:")
print(df)
print(f"\\nMean of y: {df['y'].mean()}")
"""
    
    result = assistant.run_code(example_code)
    if result['success']:
        print("Code executed successfully:")
        print(result['stdout'])
    else:
        print(f"Error: {result.get('error', result['stderr'])}")
    print()
    
    # Show help
    print("5. Available Commands")
    print("=" * 30)
    help_text = assistant.help()
    print(help_text)

if __name__ == "__main__":
    main()