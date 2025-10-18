from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import subprocess
import sys
import os
import json
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
import seaborn as sns
from io import StringIO
import traceback
import nbformat
from nbconvert import PythonExporter
import plotly
import plotly.graph_objs as go
import plotly.express as px
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.metrics import accuracy_score, mean_squared_error, r2_score
import warnings
warnings.filterwarnings('ignore')

app = Flask(__name__)
CORS(app)

class PythonAssistant:
    def __init__(self):
        self.session_variables = {}
        self.imported_modules = set()
        
    def execute_code(self, code, return_output=True):
        """Execute Python code and return the output"""
        try:
            # Capture stdout
            old_stdout = sys.stdout
            sys.stdout = captured_output = StringIO()
            
            # Execute the code
            exec(code, self.session_variables)
            
            # Get the output
            output = captured_output.getvalue()
            
            # Restore stdout
            sys.stdout = old_stdout
            
            return {
                'success': True,
                'output': output,
                'error': None
            }
        except Exception as e:
            return {
                'success': False,
                'output': '',
                'error': str(e),
                'traceback': traceback.format_exc()
            }
    
    def get_data_info(self, data_name):
        """Get information about a dataset"""
        if data_name in self.session_variables:
            data = self.session_variables[data_name]
            if isinstance(data, pd.DataFrame):
                return {
                    'type': 'DataFrame',
                    'shape': data.shape,
                    'columns': list(data.columns),
                    'dtypes': data.dtypes.to_dict(),
                    'head': data.head().to_dict(),
                    'info': data.info()
                }
            elif isinstance(data, np.ndarray):
                return {
                    'type': 'NumPy Array',
                    'shape': data.shape,
                    'dtype': str(data.dtype),
                    'sample': data.flatten()[:10].tolist()
                }
            else:
                return {
                    'type': type(data).__name__,
                    'value': str(data)[:200]
                }
        return None
    
    def suggest_code(self, task):
        """Suggest code based on the task description"""
        suggestions = {
            'load_csv': '''
# Load CSV file
import pandas as pd
df = pd.read_csv('filename.csv')
print(df.head())
print(df.info())
''',
            'linear_regression': '''
# Linear Regression
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score

# Split data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Create and train model
model = LinearRegression()
model.fit(X_train, y_train)

# Make predictions
y_pred = model.predict(X_test)

# Evaluate
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)
print(f"Mean Squared Error: {mse}")
print(f"R² Score: {r2}")
''',
            'data_visualization': '''
# Data Visualization
import matplotlib.pyplot as plt
import seaborn as sns

# Basic plots
plt.figure(figsize=(10, 6))
sns.scatterplot(data=df, x='column1', y='column2')
plt.title('Scatter Plot')
plt.show()

# Correlation heatmap
plt.figure(figsize=(10, 8))
sns.heatmap(df.corr(), annot=True, cmap='coolwarm')
plt.title('Correlation Heatmap')
plt.show()
''',
            'data_cleaning': '''
# Data Cleaning
# Check for missing values
print(df.isnull().sum())

# Handle missing values
df_cleaned = df.dropna()  # or df.fillna(method='forward')

# Check for duplicates
print(f"Duplicates: {df.duplicated().sum()}")

# Remove duplicates
df_cleaned = df.drop_duplicates()
'''
        }
        
        # Simple keyword matching for suggestions
        task_lower = task.lower()
        for key, suggestion in suggestions.items():
            if key.replace('_', ' ') in task_lower:
                return suggestion
        
        return "I can help you with data analysis, machine learning, and Python programming. What specific task would you like to work on?"

assistant = PythonAssistant()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/execute', methods=['POST'])
def execute_code():
    data = request.get_json()
    code = data.get('code', '')
    
    result = assistant.execute_code(code)
    return jsonify(result)

@app.route('/suggest', methods=['POST'])
def suggest_code():
    data = request.get_json()
    task = data.get('task', '')
    
    suggestion = assistant.suggest_code(task)
    return jsonify({'suggestion': suggestion})

@app.route('/data_info', methods=['POST'])
def get_data_info():
    data = request.get_json()
    data_name = data.get('data_name', '')
    
    info = assistant.get_data_info(data_name)
    return jsonify({'info': info})

@app.route('/variables', methods=['GET'])
def get_variables():
    """Get all variables in the current session"""
    variables = {}
    for name, value in assistant.session_variables.items():
        if not name.startswith('_'):
            variables[name] = {
                'type': type(value).__name__,
                'repr': repr(value)[:100]
            }
    return jsonify({'variables': variables})

@app.route('/clear', methods=['POST'])
def clear_session():
    """Clear the current session"""
    assistant.session_variables.clear()
    return jsonify({'success': True})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)