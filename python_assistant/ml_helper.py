"""
Machine Learning helper functions for Python Assistant
"""

import pandas as pd
import numpy as np
import json
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.metrics import classification_report, confusion_matrix, r2_score, mean_squared_error
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
import warnings
warnings.filterwarnings('ignore')

class MLHelper:
    """
    Machine Learning helper class for data analysis and model building
    """
    
    def __init__(self, workspace_path: str = None):
        """
        Initialize ML Helper
        
        Args:
            workspace_path: Path to the workspace directory
        """
        self.workspace_path = Path(workspace_path) if workspace_path else Path.cwd()
        self.data_cache = {}
        
    def analyze_dataset(self, file_path: str) -> Dict[str, Any]:
        """
        Analyze a dataset and provide comprehensive insights
        
        Args:
            file_path: Path to the dataset file
            
        Returns:
            Dictionary containing dataset analysis
        """
        try:
            file_path = Path(file_path)
            
            # Load data based on file extension
            if file_path.suffix == '.csv':
                df = pd.read_csv(file_path)
            elif file_path.suffix == '.json':
                df = pd.read_json(file_path)
            else:
                return {"error": f"Unsupported file format: {file_path.suffix}"}
            
            analysis = {
                "file_path": str(file_path),
                "shape": df.shape,
                "columns": list(df.columns),
                "data_types": df.dtypes.to_dict(),
                "missing_values": df.isnull().sum().to_dict(),
                "missing_percentage": (df.isnull().sum() / len(df) * 100).to_dict(),
                "numeric_columns": df.select_dtypes(include=[np.number]).columns.tolist(),
                "categorical_columns": df.select_dtypes(include=['object']).columns.tolist(),
                "basic_stats": df.describe().to_dict(),
                "correlation_matrix": df.corr().to_dict() if len(df.select_dtypes(include=[np.number]).columns) > 1 else {},
                "suggestions": []
            }
            
            # Generate suggestions
            analysis["suggestions"] = self._generate_dataset_suggestions(df)
            
            # Cache the data
            self.data_cache[str(file_path)] = df
            
            return analysis
            
        except Exception as e:
            return {"error": f"Error analyzing dataset: {str(e)}"}
    
    def _generate_dataset_suggestions(self, df: pd.DataFrame) -> List[str]:
        """Generate suggestions for dataset improvement"""
        suggestions = []
        
        # Check for missing values
        missing_cols = df.columns[df.isnull().any()].tolist()
        if missing_cols:
            suggestions.append(f"Found missing values in columns: {missing_cols}")
        
        # Check for high cardinality categorical columns
        for col in df.select_dtypes(include=['object']).columns:
            if df[col].nunique() > len(df) * 0.5:
                suggestions.append(f"Column '{col}' has high cardinality ({df[col].nunique()} unique values)")
        
        # Check for constant columns
        constant_cols = df.columns[df.nunique() == 1].tolist()
        if constant_cols:
            suggestions.append(f"Found constant columns: {constant_cols}")
        
        # Check for highly correlated columns
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        if len(numeric_cols) > 1:
            corr_matrix = df[numeric_cols].corr()
            high_corr_pairs = []
            for i in range(len(corr_matrix.columns)):
                for j in range(i+1, len(corr_matrix.columns)):
                    if abs(corr_matrix.iloc[i, j]) > 0.9:
                        high_corr_pairs.append((corr_matrix.columns[i], corr_matrix.columns[j]))
            
            if high_corr_pairs:
                suggestions.append(f"Found highly correlated columns: {high_corr_pairs}")
        
        return suggestions
    
    def prepare_data(self, file_path: str, target_column: str, 
                    test_size: float = 0.2, random_state: int = 42) -> Dict[str, Any]:
        """
        Prepare data for machine learning
        
        Args:
            file_path: Path to the dataset file
            target_column: Name of the target column
            test_size: Proportion of data for testing
            random_state: Random state for reproducibility
            
        Returns:
            Dictionary containing prepared data
        """
        try:
            # Load data if not cached
            if str(file_path) not in self.data_cache:
                file_path = Path(file_path)
                if file_path.suffix == '.csv':
                    df = pd.read_csv(file_path)
                elif file_path.suffix == '.json':
                    df = pd.read_json(file_path)
                else:
                    return {"error": f"Unsupported file format: {file_path.suffix}"}
            else:
                df = self.data_cache[str(file_path)]
            
            # Check if target column exists
            if target_column not in df.columns:
                return {"error": f"Target column '{target_column}' not found in dataset"}
            
            # Separate features and target
            X = df.drop(columns=[target_column])
            y = df[target_column]
            
            # Handle missing values
            X = X.fillna(X.mean() if X.select_dtypes(include=[np.number]).shape[1] > 0 else X.mode().iloc[0])
            y = y.fillna(y.mean() if y.dtype in ['int64', 'float64'] else y.mode()[0])
            
            # Encode categorical variables
            categorical_columns = X.select_dtypes(include=['object']).columns
            label_encoders = {}
            
            for col in categorical_columns:
                le = LabelEncoder()
                X[col] = le.fit_transform(X[col].astype(str))
                label_encoders[col] = le
            
            # Encode target if categorical
            if y.dtype == 'object':
                le_target = LabelEncoder()
                y = le_target.fit_transform(y.astype(str))
                label_encoders['target'] = le_target
            
            # Split data
            X_train, X_test, y_train, y_test = train_test_split(
                X, y, test_size=test_size, random_state=random_state
            )
            
            # Scale features
            scaler = StandardScaler()
            X_train_scaled = scaler.fit_transform(X_train)
            X_test_scaled = scaler.transform(X_test)
            
            return {
                "X_train": X_train_scaled,
                "X_test": X_test_scaled,
                "y_train": y_train,
                "y_test": y_test,
                "feature_names": X.columns.tolist(),
                "label_encoders": label_encoders,
                "scaler": scaler,
                "target_column": target_column,
                "data_shape": X.shape
            }
            
        except Exception as e:
            return {"error": f"Error preparing data: {str(e)}"}
    
    def train_model(self, prepared_data: Dict[str, Any], model_type: str = "auto") -> Dict[str, Any]:
        """
        Train a machine learning model
        
        Args:
            prepared_data: Data prepared by prepare_data method
            model_type: Type of model to train ("auto", "regression", "classification")
            
        Returns:
            Dictionary containing trained model and metrics
        """
        try:
            if "error" in prepared_data:
                return prepared_data
            
            X_train = prepared_data["X_train"]
            X_test = prepared_data["X_test"]
            y_train = prepared_data["y_train"]
            y_test = prepared_data["y_test"]
            
            # Determine if it's a regression or classification problem
            if model_type == "auto":
                if len(np.unique(y_train)) < 20:  # Heuristic for classification
                    model_type = "classification"
                else:
                    model_type = "regression"
            
            # Train appropriate model
            if model_type == "regression":
                model = RandomForestRegressor(n_estimators=100, random_state=42)
                model.fit(X_train, y_train)
                
                # Make predictions
                y_pred = model.predict(X_test)
                
                # Calculate metrics
                r2 = r2_score(y_test, y_pred)
                mse = mean_squared_error(y_test, y_pred)
                rmse = np.sqrt(mse)
                
                metrics = {
                    "r2_score": r2,
                    "mse": mse,
                    "rmse": rmse,
                    "model_type": "regression"
                }
                
            else:  # classification
                model = RandomForestClassifier(n_estimators=100, random_state=42)
                model.fit(X_train, y_train)
                
                # Make predictions
                y_pred = model.predict(X_test)
                
                # Calculate metrics
                accuracy = model.score(X_test, y_test)
                report = classification_report(y_test, y_pred, output_dict=True)
                
                metrics = {
                    "accuracy": accuracy,
                    "classification_report": report,
                    "model_type": "classification"
                }
            
            # Feature importance
            feature_importance = None
            if hasattr(model, 'feature_importances_'):
                feature_importance = dict(zip(
                    prepared_data["feature_names"],
                    model.feature_importances_
                ))
            
            return {
                "model": model,
                "metrics": metrics,
                "feature_importance": feature_importance,
                "predictions": y_pred,
                "y_test": y_test
            }
            
        except Exception as e:
            return {"error": f"Error training model: {str(e)}"}
    
    def create_visualizations(self, file_path: str, target_column: str = None) -> Dict[str, str]:
        """
        Create visualizations for the dataset
        
        Args:
            file_path: Path to the dataset file
            target_column: Optional target column for analysis
            
        Returns:
            Dictionary containing paths to generated plots
        """
        try:
            # Load data
            file_path = Path(file_path)
            if file_path.suffix == '.csv':
                df = pd.read_csv(file_path)
            elif file_path.suffix == '.json':
                df = pd.read_json(file_path)
            else:
                return {"error": f"Unsupported file format: {file_path.suffix}"}
            
            plots = {}
            
            # Set style
            plt.style.use('seaborn-v0_8')
            
            # 1. Data distribution
            numeric_cols = df.select_dtypes(include=[np.number]).columns
            if len(numeric_cols) > 0:
                fig, axes = plt.subplots(2, 2, figsize=(15, 10))
                fig.suptitle('Data Distribution Analysis', fontsize=16)
                
                # Histogram
                df[numeric_cols].hist(ax=axes[0, 0], bins=20)
                axes[0, 0].set_title('Histograms')
                
                # Box plots
                df[numeric_cols].boxplot(ax=axes[0, 1])
                axes[0, 1].set_title('Box Plots')
                
                # Correlation heatmap
                if len(numeric_cols) > 1:
                    corr_matrix = df[numeric_cols].corr()
                    sns.heatmap(corr_matrix, annot=True, ax=axes[1, 0], cmap='coolwarm')
                    axes[1, 0].set_title('Correlation Matrix')
                
                # Missing values
                missing_data = df.isnull().sum()
                missing_data = missing_data[missing_data > 0]
                if len(missing_data) > 0:
                    missing_data.plot(kind='bar', ax=axes[1, 1])
                    axes[1, 1].set_title('Missing Values')
                else:
                    axes[1, 1].text(0.5, 0.5, 'No Missing Values', 
                                   ha='center', va='center', transform=axes[1, 1].transAxes)
                    axes[1, 1].set_title('Missing Values')
                
                plt.tight_layout()
                plot_path = self.workspace_path / "data_distribution.png"
                plt.savefig(plot_path, dpi=300, bbox_inches='tight')
                plt.close()
                plots["data_distribution"] = str(plot_path)
            
            # 2. Target variable analysis (if provided)
            if target_column and target_column in df.columns:
                fig, axes = plt.subplots(1, 2, figsize=(15, 5))
                fig.suptitle(f'Target Variable Analysis: {target_column}', fontsize=16)
                
                # Target distribution
                if df[target_column].dtype in ['int64', 'float64']:
                    df[target_column].hist(ax=axes[0], bins=20)
                    axes[0].set_title(f'Distribution of {target_column}')
                else:
                    df[target_column].value_counts().plot(kind='bar', ax=axes[0])
                    axes[0].set_title(f'Distribution of {target_column}')
                    axes[0].tick_params(axis='x', rotation=45)
                
                # Target vs features (if numeric)
                if len(numeric_cols) > 1:
                    # Select first numeric feature for scatter plot
                    feature_col = [col for col in numeric_cols if col != target_column][0]
                    axes[1].scatter(df[feature_col], df[target_column], alpha=0.6)
                    axes[1].set_xlabel(feature_col)
                    axes[1].set_ylabel(target_column)
                    axes[1].set_title(f'{target_column} vs {feature_col}')
                
                plt.tight_layout()
                plot_path = self.workspace_path / "target_analysis.png"
                plt.savefig(plot_path, dpi=300, bbox_inches='tight')
                plt.close()
                plots["target_analysis"] = str(plot_path)
            
            return plots
            
        except Exception as e:
            return {"error": f"Error creating visualizations: {str(e)}"}
    
    def generate_report(self, file_path: str, target_column: str = None) -> str:
        """
        Generate a comprehensive ML report
        
        Args:
            file_path: Path to the dataset file
            target_column: Optional target column for analysis
            
        Returns:
            Generated report as string
        """
        try:
            # Analyze dataset
            analysis = self.analyze_dataset(file_path)
            if "error" in analysis:
                return f"Error analyzing dataset: {analysis['error']}"
            
            # Create visualizations
            plots = self.create_visualizations(file_path, target_column)
            
            # Generate report
            report = f"""
# Machine Learning Analysis Report

## Dataset Overview
- **File**: {analysis['file_path']}
- **Shape**: {analysis['shape'][0]} rows, {analysis['shape'][1]} columns
- **Numeric Columns**: {len(analysis['numeric_columns'])}
- **Categorical Columns**: {len(analysis['categorical_columns'])}

## Data Quality
- **Missing Values**: {sum(analysis['missing_values'].values())} total missing values
- **Columns with Missing Values**: {[col for col, count in analysis['missing_values'].items() if count > 0]}

## Column Information
"""
            
            for col in analysis['columns']:
                report += f"- **{col}**: {analysis['data_types'][col]}"
                if col in analysis['missing_values'] and analysis['missing_values'][col] > 0:
                    report += f" ({analysis['missing_values'][col]} missing, {analysis['missing_percentage'][col]:.1f}%)"
                report += "\n"
            
            report += "\n## Suggestions\n"
            for suggestion in analysis['suggestions']:
                report += f"- {suggestion}\n"
            
            if plots and "error" not in plots:
                report += "\n## Generated Visualizations\n"
                for plot_name, plot_path in plots.items():
                    report += f"- {plot_name}: {plot_path}\n"
            
            return report
            
        except Exception as e:
            return f"Error generating report: {str(e)}"