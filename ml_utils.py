"""
Machine Learning Utilities for Python Assistant
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.svm import SVC, SVR
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
from sklearn.preprocessing import StandardScaler, LabelEncoder
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import warnings
warnings.filterwarnings('ignore')

class MLAssistant:
    def __init__(self):
        self.models = {}
        self.scalers = {}
        self.encoders = {}
        
    def quick_eda(self, df, target_column=None):
        """Quick Exploratory Data Analysis"""
        print("=== QUICK EDA REPORT ===")
        print(f"Dataset Shape: {df.shape}")
        print(f"Memory Usage: {df.memory_usage(deep=True).sum() / 1024**2:.2f} MB")
        print("\n=== DATA TYPES ===")
        print(df.dtypes)
        
        print("\n=== MISSING VALUES ===")
        missing = df.isnull().sum()
        missing_pct = (missing / len(df)) * 100
        missing_df = pd.DataFrame({
            'Missing Count': missing,
            'Missing %': missing_pct
        }).sort_values('Missing %', ascending=False)
        print(missing_df[missing_df['Missing Count'] > 0])
        
        print("\n=== BASIC STATISTICS ===")
        print(df.describe())
        
        if target_column and target_column in df.columns:
            print(f"\n=== TARGET VARIABLE ANALYSIS: {target_column} ===")
            if df[target_column].dtype == 'object':
                print("Value Counts:")
                print(df[target_column].value_counts())
            else:
                print(f"Mean: {df[target_column].mean():.2f}")
                print(f"Median: {df[target_column].median():.2f}")
                print(f"Std: {df[target_column].std():.2f}")
                print(f"Min: {df[target_column].min():.2f}")
                print(f"Max: {df[target_column].max():.2f}")
        
        return df
    
    def plot_correlation_matrix(self, df, figsize=(12, 8)):
        """Plot correlation matrix"""
        plt.figure(figsize=figsize)
        correlation_matrix = df.corr()
        sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', center=0,
                   square=True, linewidths=0.5)
        plt.title('Correlation Matrix')
        plt.tight_layout()
        plt.show()
    
    def plot_distributions(self, df, columns=None, figsize=(15, 10)):
        """Plot distributions of numeric columns"""
        if columns is None:
            columns = df.select_dtypes(include=[np.number]).columns
        
        n_cols = 3
        n_rows = (len(columns) + n_cols - 1) // n_cols
        
        fig, axes = plt.subplots(n_rows, n_cols, figsize=figsize)
        axes = axes.flatten() if n_rows > 1 else [axes] if n_rows == 1 else axes
        
        for i, col in enumerate(columns):
            if i < len(axes):
                df[col].hist(bins=30, ax=axes[i], alpha=0.7)
                axes[i].set_title(f'Distribution of {col}')
                axes[i].set_xlabel(col)
                axes[i].set_ylabel('Frequency')
        
        # Hide empty subplots
        for i in range(len(columns), len(axes)):
            axes[i].set_visible(False)
        
        plt.tight_layout()
        plt.show()
    
    def prepare_data(self, df, target_column, test_size=0.2, random_state=42):
        """Prepare data for machine learning"""
        # Separate features and target
        X = df.drop(columns=[target_column])
        y = df[target_column]
        
        # Handle categorical variables
        categorical_columns = X.select_dtypes(include=['object']).columns
        for col in categorical_columns:
            le = LabelEncoder()
            X[col] = le.fit_transform(X[col].astype(str))
            self.encoders[col] = le
        
        # Handle missing values
        X = X.fillna(X.mean())
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size, random_state=random_state
        )
        
        # Scale features
        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(X_train)
        X_test_scaled = scaler.transform(X_test)
        self.scalers['main'] = scaler
        
        return X_train_scaled, X_test_scaled, y_train, y_test, X.columns
    
    def train_classification_models(self, X_train, X_test, y_train, y_test):
        """Train multiple classification models"""
        models = {
            'Logistic Regression': LogisticRegression(random_state=42),
            'Random Forest': RandomForestClassifier(random_state=42),
            'SVM': SVC(random_state=42)
        }
        
        results = {}
        
        for name, model in models.items():
            print(f"\n=== Training {name} ===")
            
            # Train model
            model.fit(X_train, y_train)
            
            # Make predictions
            y_pred = model.predict(X_test)
            
            # Calculate metrics
            accuracy = accuracy_score(y_test, y_pred)
            
            print(f"Accuracy: {accuracy:.4f}")
            print("\nClassification Report:")
            print(classification_report(y_test, y_pred))
            
            # Store model and results
            self.models[name] = model
            results[name] = {
                'accuracy': accuracy,
                'predictions': y_pred,
                'model': model
            }
        
        return results
    
    def train_regression_models(self, X_train, X_test, y_train, y_test):
        """Train multiple regression models"""
        models = {
            'Linear Regression': LinearRegression(),
            'Random Forest': RandomForestRegressor(random_state=42),
            'SVM': SVR()
        }
        
        results = {}
        
        for name, model in models.items():
            print(f"\n=== Training {name} ===")
            
            # Train model
            model.fit(X_train, y_train)
            
            # Make predictions
            y_pred = model.predict(X_test)
            
            # Calculate metrics
            mse = mean_squared_error(y_test, y_pred)
            rmse = np.sqrt(mse)
            mae = mean_absolute_error(y_test, y_pred)
            r2 = r2_score(y_test, y_pred)
            
            print(f"RMSE: {rmse:.4f}")
            print(f"MAE: {mae:.4f}")
            print(f"R² Score: {r2:.4f}")
            
            # Store model and results
            self.models[name] = model
            results[name] = {
                'mse': mse,
                'rmse': rmse,
                'mae': mae,
                'r2': r2,
                'predictions': y_pred,
                'model': model
            }
        
        return results
    
    def plot_model_comparison(self, results, metric='accuracy'):
        """Plot model comparison"""
        model_names = list(results.keys())
        metric_values = [results[name][metric] for name in model_names]
        
        plt.figure(figsize=(10, 6))
        bars = plt.bar(model_names, metric_values, color='skyblue', alpha=0.7)
        plt.title(f'Model Comparison - {metric.title()}')
        plt.ylabel(metric.title())
        plt.xticks(rotation=45)
        
        # Add value labels on bars
        for bar, value in zip(bars, metric_values):
            plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.01,
                    f'{value:.4f}', ha='center', va='bottom')
        
        plt.tight_layout()
        plt.show()
    
    def feature_importance(self, model_name, feature_names):
        """Plot feature importance"""
        if model_name not in self.models:
            print(f"Model {model_name} not found!")
            return
        
        model = self.models[model_name]
        
        if hasattr(model, 'feature_importances_'):
            importances = model.feature_importances_
        elif hasattr(model, 'coef_'):
            importances = np.abs(model.coef_[0])
        else:
            print(f"Model {model_name} doesn't support feature importance!")
            return
        
        # Create feature importance dataframe
        feature_imp = pd.DataFrame({
            'feature': feature_names,
            'importance': importances
        }).sort_values('importance', ascending=False)
        
        # Plot
        plt.figure(figsize=(10, 8))
        sns.barplot(data=feature_imp.head(15), x='importance', y='feature')
        plt.title(f'Feature Importance - {model_name}')
        plt.xlabel('Importance')
        plt.tight_layout()
        plt.show()
        
        return feature_imp

# Create a global instance
ml_assistant = MLAssistant()