# 🐍 Python Assistant

A comprehensive web-based Python programming assistant with built-in machine learning capabilities, data analysis tools, and interactive code execution.

## ✨ Features

### 🚀 Core Features
- **Interactive Code Editor**: Execute Python code in real-time
- **Web-based Interface**: Modern, responsive UI with syntax highlighting
- **Session Management**: Persistent variables and data across code executions
- **Error Handling**: Detailed error messages and tracebacks
- **Code Suggestions**: Pre-built templates for common tasks

### 📊 Data Analysis & ML
- **Exploratory Data Analysis**: Quick EDA with visualizations
- **Machine Learning Models**: Linear/Logistic Regression, Random Forest, SVM
- **Data Visualization**: Matplotlib, Seaborn, and Plotly integration
- **Model Evaluation**: Comprehensive metrics and performance analysis
- **Feature Engineering**: Data preprocessing and transformation tools

### 🛠️ Developer Tools
- **Variable Inspector**: View all session variables and their types
- **Code Formatting**: Automatic Python code formatting
- **Keyboard Shortcuts**: Ctrl+Enter to run, Ctrl+K to clear
- **Session Management**: Clear session and reset environment

## 🚀 Quick Start

### Option 1: Using the Launcher (Recommended)
```bash
python run_assistant.py
```

### Option 2: Manual Setup
```bash
# Install dependencies
pip install -r requirements.txt

# Run the application
python app.py
```

Then open your browser and go to `http://localhost:5000`

## 📖 Usage Examples

### Basic Python Programming
```python
# Simple calculations
x = 10
y = 20
result = x + y
print(f"Sum: {result}")

# Data structures
my_list = [1, 2, 3, 4, 5]
squared = [x**2 for x in my_list]
print(squared)
```

### Data Analysis
```python
# Load and explore data
import pandas as pd
import numpy as np

# Create sample data
data = {'x': [1, 2, 3, 4, 5], 'y': [2, 4, 6, 8, 10]}
df = pd.DataFrame(data)

# Basic analysis
print(df.describe())
print(df.corr())

# Visualization
import matplotlib.pyplot as plt
plt.scatter(df['x'], df['y'])
plt.title('Sample Data')
plt.show()
```

### Machine Learning
```python
# Use the ML Assistant utilities
from ml_utils import ml_assistant

# Quick EDA
ml_assistant.quick_eda(df, target_column='y')

# Prepare data
X_train, X_test, y_train, y_test, feature_names = ml_assistant.prepare_data(
    df, target_column='y'
)

# Train models
results = ml_assistant.train_regression_models(X_train, X_test, y_train, y_test)

# Compare models
ml_assistant.plot_model_comparison(results, metric='r2')
```

## 🎯 Quick Actions

The assistant includes quick action buttons for common tasks:

- **Load CSV**: Template for loading and exploring CSV files
- **Linear Regression**: Complete linear regression workflow
- **Data Visualization**: Common plotting templates
- **Data Cleaning**: Data preprocessing templates

## 📁 Project Structure

```
Python Assistant/
├── app.py                          # Main Flask application
├── ml_utils.py                     # Machine learning utilities
├── run_assistant.py               # Application launcher
├── requirements.txt               # Python dependencies
├── templates/
│   └── index.html                 # Web interface
├── static/
│   ├── css/
│   │   └── style.css              # Styling
│   └── js/
│       └── app.js                 # Frontend JavaScript
├── example_notebooks/             # Example scripts
│   ├── linear_regression_example.py
│   └── logistic_regression_example.py
└── README_Python_Assistant.md     # This file
```

## 🔧 API Endpoints

- `POST /execute` - Execute Python code
- `POST /suggest` - Get code suggestions
- `POST /data_info` - Get data information
- `GET /variables` - List session variables
- `POST /clear` - Clear session

## 🎨 Features in Detail

### Code Execution
- Safe code execution in isolated environment
- Real-time output display
- Error handling with detailed tracebacks
- Support for all major Python libraries

### Data Analysis
- Automatic data type detection
- Missing value analysis
- Statistical summaries
- Correlation analysis
- Distribution plots

### Machine Learning
- Multiple algorithm support
- Automated model comparison
- Feature importance analysis
- Performance visualization
- Cross-validation support

### User Interface
- Responsive design
- Syntax highlighting
- Real-time code execution
- Variable inspector
- Session management

## 🛡️ Security Features

- Isolated code execution environment
- Input validation and sanitization
- Safe file operations
- Memory management

## 📚 Dependencies

- **Flask**: Web framework
- **Pandas**: Data manipulation
- **NumPy**: Numerical computing
- **Matplotlib/Seaborn**: Data visualization
- **Scikit-learn**: Machine learning
- **Plotly**: Interactive visualizations

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is open source and available under the MIT License.

## 🆘 Support

For issues and questions:
1. Check the example notebooks
2. Review the API documentation
3. Open an issue on GitHub

---

**Happy Coding with Python Assistant! 🐍✨**