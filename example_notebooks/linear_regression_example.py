"""
Linear Regression Example for Python Assistant
This demonstrates how to use the Python Assistant for machine learning tasks
"""

# Import necessary libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.preprocessing import StandardScaler

# Create sample data (you can replace this with your own data)
np.random.seed(42)
n_samples = 1000

# Generate features
X1 = np.random.normal(0, 1, n_samples)  # Feature 1
X2 = np.random.normal(0, 1, n_samples)  # Feature 2
X3 = np.random.normal(0, 1, n_samples)  # Feature 3

# Generate target variable with some noise
y = 2 * X1 + 3 * X2 - 1.5 * X3 + np.random.normal(0, 0.5, n_samples)

# Create DataFrame
data = pd.DataFrame({
    'feature_1': X1,
    'feature_2': X2,
    'feature_3': X3,
    'target': y
})

print("=== LINEAR REGRESSION EXAMPLE ===")
print(f"Dataset shape: {data.shape}")
print("\nFirst 5 rows:")
print(data.head())

print("\nDataset info:")
print(data.info())

print("\nBasic statistics:")
print(data.describe())

# Exploratory Data Analysis
plt.figure(figsize=(15, 10))

# 1. Correlation heatmap
plt.subplot(2, 3, 1)
correlation_matrix = data.corr()
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', center=0)
plt.title('Correlation Matrix')

# 2. Feature distributions
plt.subplot(2, 3, 2)
data['feature_1'].hist(bins=30, alpha=0.7)
plt.title('Feature 1 Distribution')
plt.xlabel('Feature 1')
plt.ylabel('Frequency')

plt.subplot(2, 3, 3)
data['feature_2'].hist(bins=30, alpha=0.7)
plt.title('Feature 2 Distribution')
plt.xlabel('Feature 2')
plt.ylabel('Frequency')

plt.subplot(2, 3, 4)
data['feature_3'].hist(bins=30, alpha=0.7)
plt.title('Feature 3 Distribution')
plt.xlabel('Feature 3')
plt.ylabel('Frequency')

# 3. Target distribution
plt.subplot(2, 3, 5)
data['target'].hist(bins=30, alpha=0.7)
plt.title('Target Distribution')
plt.xlabel('Target')
plt.ylabel('Frequency')

# 4. Feature vs Target scatter plots
plt.subplot(2, 3, 6)
plt.scatter(data['feature_1'], data['target'], alpha=0.6)
plt.xlabel('Feature 1')
plt.ylabel('Target')
plt.title('Feature 1 vs Target')

plt.tight_layout()
plt.show()

# Prepare data for modeling
X = data[['feature_1', 'feature_2', 'feature_3']]
y = data['target']

# Split the data
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

print(f"\nTraining set size: {X_train.shape[0]}")
print(f"Test set size: {X_test.shape[0]}")

# Scale the features
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Train the model
model = LinearRegression()
model.fit(X_train_scaled, y_train)

# Make predictions
y_train_pred = model.predict(X_train_scaled)
y_test_pred = model.predict(X_test_scaled)

# Calculate metrics
train_mse = mean_squared_error(y_train, y_train_pred)
test_mse = mean_squared_error(y_test, y_test_pred)
train_r2 = r2_score(y_train, y_train_pred)
test_r2 = r2_score(y_test, y_test_pred)

print("\n=== MODEL PERFORMANCE ===")
print(f"Training MSE: {train_mse:.4f}")
print(f"Test MSE: {test_mse:.4f}")
print(f"Training R²: {train_r2:.4f}")
print(f"Test R²: {test_r2:.4f}")

# Model coefficients
print(f"\nModel coefficients: {model.coef_}")
print(f"Model intercept: {model.intercept_:.4f}")

# Visualize results
plt.figure(figsize=(15, 5))

# 1. Actual vs Predicted (Training)
plt.subplot(1, 3, 1)
plt.scatter(y_train, y_train_pred, alpha=0.6)
plt.plot([y_train.min(), y_train.max()], [y_train.min(), y_train.max()], 'r--', lw=2)
plt.xlabel('Actual')
plt.ylabel('Predicted')
plt.title(f'Training Set\nR² = {train_r2:.4f}')

# 2. Actual vs Predicted (Test)
plt.subplot(1, 3, 2)
plt.scatter(y_test, y_test_pred, alpha=0.6)
plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'r--', lw=2)
plt.xlabel('Actual')
plt.ylabel('Predicted')
plt.title(f'Test Set\nR² = {test_r2:.4f}')

# 3. Residuals
plt.subplot(1, 3, 3)
residuals = y_test - y_test_pred
plt.scatter(y_test_pred, residuals, alpha=0.6)
plt.axhline(y=0, color='r', linestyle='--')
plt.xlabel('Predicted')
plt.ylabel('Residuals')
plt.title('Residual Plot')

plt.tight_layout()
plt.show()

# Feature importance
feature_importance = pd.DataFrame({
    'feature': ['feature_1', 'feature_2', 'feature_3'],
    'coefficient': model.coef_,
    'abs_coefficient': np.abs(model.coef_)
}).sort_values('abs_coefficient', ascending=False)

print("\n=== FEATURE IMPORTANCE ===")
print(feature_importance)

# Plot feature importance
plt.figure(figsize=(8, 6))
sns.barplot(data=feature_importance, x='abs_coefficient', y='feature')
plt.title('Feature Importance (Absolute Coefficients)')
plt.xlabel('Absolute Coefficient Value')
plt.tight_layout()
plt.show()

print("\n=== LINEAR REGRESSION COMPLETE ===")
print("The model has been trained and evaluated successfully!")
print("You can now use this model to make predictions on new data.")