"""
Logistic Regression Example for Python Assistant
This demonstrates classification using logistic regression
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.datasets import make_classification

# Create sample classification data
np.random.seed(42)
X, y = make_classification(
    n_samples=1000,
    n_features=4,
    n_informative=3,
    n_redundant=1,
    n_classes=2,
    random_state=42
)

# Create DataFrame
data = pd.DataFrame(X, columns=['feature_1', 'feature_2', 'feature_3', 'feature_4'])
data['target'] = y

print("=== LOGISTIC REGRESSION EXAMPLE ===")
print(f"Dataset shape: {data.shape}")
print("\nFirst 5 rows:")
print(data.head())

print("\nDataset info:")
print(data.info())

print("\nTarget distribution:")
print(data['target'].value_counts())
print(f"Class balance: {data['target'].value_counts(normalize=True)}")

# Exploratory Data Analysis
plt.figure(figsize=(15, 10))

# 1. Correlation heatmap
plt.subplot(2, 3, 1)
correlation_matrix = data.corr()
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', center=0)
plt.title('Correlation Matrix')

# 2. Feature distributions by class
plt.subplot(2, 3, 2)
for class_label in data['target'].unique():
    subset = data[data['target'] == class_label]
    plt.hist(subset['feature_1'], alpha=0.7, label=f'Class {class_label}', bins=20)
plt.xlabel('Feature 1')
plt.ylabel('Frequency')
plt.title('Feature 1 by Class')
plt.legend()

plt.subplot(2, 3, 3)
for class_label in data['target'].unique():
    subset = data[data['target'] == class_label]
    plt.hist(subset['feature_2'], alpha=0.7, label=f'Class {class_label}', bins=20)
plt.xlabel('Feature 2')
plt.ylabel('Frequency')
plt.title('Feature 2 by Class')
plt.legend()

plt.subplot(2, 3, 4)
for class_label in data['target'].unique():
    subset = data[data['target'] == class_label]
    plt.hist(subset['feature_3'], alpha=0.7, label=f'Class {class_label}', bins=20)
plt.xlabel('Feature 3')
plt.ylabel('Frequency')
plt.title('Feature 3 by Class')
plt.legend()

plt.subplot(2, 3, 5)
for class_label in data['target'].unique():
    subset = data[data['target'] == class_label]
    plt.hist(subset['feature_4'], alpha=0.7, label=f'Class {class_label}', bins=20)
plt.xlabel('Feature 4')
plt.ylabel('Frequency')
plt.title('Feature 4 by Class')
plt.legend()

# 3. Scatter plot of first two features
plt.subplot(2, 3, 6)
colors = ['red' if label == 0 else 'blue' for label in data['target']]
plt.scatter(data['feature_1'], data['feature_2'], c=colors, alpha=0.6)
plt.xlabel('Feature 1')
plt.ylabel('Feature 2')
plt.title('Feature 1 vs Feature 2')
plt.legend(['Class 0', 'Class 1'])

plt.tight_layout()
plt.show()

# Prepare data for modeling
X = data[['feature_1', 'feature_2', 'feature_3', 'feature_4']]
y = data['target']

# Split the data
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

print(f"\nTraining set size: {X_train.shape[0]}")
print(f"Test set size: {X_test.shape[0]}")
print(f"Training set class distribution: {y_train.value_counts(normalize=True)}")
print(f"Test set class distribution: {y_test.value_counts(normalize=True)}")

# Scale the features
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Train the model
model = LogisticRegression(random_state=42, max_iter=1000)
model.fit(X_train_scaled, y_train)

# Make predictions
y_train_pred = model.predict(X_train_scaled)
y_test_pred = model.predict(X_test_scaled)
y_test_proba = model.predict_proba(X_test_scaled)[:, 1]

# Calculate metrics
train_accuracy = accuracy_score(y_train, y_train_pred)
test_accuracy = accuracy_score(y_test, y_test_pred)

print("\n=== MODEL PERFORMANCE ===")
print(f"Training Accuracy: {train_accuracy:.4f}")
print(f"Test Accuracy: {test_accuracy:.4f}")

print("\nClassification Report (Test Set):")
print(classification_report(y_test, y_test_pred))

# Confusion Matrix
cm = confusion_matrix(y_test, y_test_pred)
print(f"\nConfusion Matrix:")
print(cm)

# Model coefficients
print(f"\nModel coefficients: {model.coef_[0]}")
print(f"Model intercept: {model.intercept_[0]:.4f}")

# Visualize results
plt.figure(figsize=(15, 5))

# 1. Confusion Matrix
plt.subplot(1, 3, 1)
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues')
plt.title('Confusion Matrix')
plt.xlabel('Predicted')
plt.ylabel('Actual')

# 2. ROC Curve
from sklearn.metrics import roc_curve, auc
fpr, tpr, _ = roc_curve(y_test, y_test_proba)
roc_auc = auc(fpr, tpr)

plt.subplot(1, 3, 2)
plt.plot(fpr, tpr, color='darkorange', lw=2, label=f'ROC curve (AUC = {roc_auc:.2f})')
plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--')
plt.xlim([0.0, 1.0])
plt.ylim([0.0, 1.05])
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('ROC Curve')
plt.legend(loc="lower right")

# 3. Feature importance
plt.subplot(1, 3, 3)
feature_importance = pd.DataFrame({
    'feature': ['feature_1', 'feature_2', 'feature_3', 'feature_4'],
    'coefficient': model.coef_[0],
    'abs_coefficient': np.abs(model.coef_[0])
}).sort_values('abs_coefficient', ascending=True)

sns.barplot(data=feature_importance, x='abs_coefficient', y='feature')
plt.title('Feature Importance (Absolute Coefficients)')
plt.xlabel('Absolute Coefficient Value')

plt.tight_layout()
plt.show()

# Probability distribution
plt.figure(figsize=(10, 6))
plt.hist(y_test_proba[y_test == 0], bins=20, alpha=0.7, label='Class 0', color='red')
plt.hist(y_test_proba[y_test == 1], bins=20, alpha=0.7, label='Class 1', color='blue')
plt.axvline(x=0.5, color='black', linestyle='--', label='Decision Threshold')
plt.xlabel('Predicted Probability')
plt.ylabel('Frequency')
plt.title('Distribution of Predicted Probabilities')
plt.legend()
plt.show()

print("\n=== LOGISTIC REGRESSION COMPLETE ===")
print("The classification model has been trained and evaluated successfully!")
print("You can now use this model to make predictions on new data.")