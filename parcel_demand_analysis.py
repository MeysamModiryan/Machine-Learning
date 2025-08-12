import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score, mean_squared_error
import warnings
warnings.filterwarnings('ignore')

# Set style for better plots
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")

# Sample data (you can replace this with your actual data file)
data = {
    'Date': ['1404/03/03', '1404/03/03', '1404/03/03', '1404/03/03', '1404/03/03'],
    'Parcel_Type': ['ميني پک', 'ميني پک', 'ميني پک', 'ميني پک', 'ميني پک'],
    'Discount': [0.0, 15.0, 17.0, 18.0, 19.0],
    'Count': [238, 4, 100, 4, 32],
    'Service_Price': [772320.168067, 709400.000000, 736402.800000, 724400.000000, 715025.000000]
}

df = pd.DataFrame(data)

print("=== PARCEL SHIPMENT DATA ANALYSIS ===")
print("\nOriginal Data:")
print(df)
print("\nData Info:")
print(df.info())
print("\nSummary Statistics:")
print(df.describe())

# Calculate effective price (price per parcel)
df['Effective_Price'] = df['Service_Price'] / df['Count']
df['Effective_Price_Rounded'] = df['Effective_Price'].round(2)

print("\n=== PRICE-DEMAND ANALYSIS ===")
print("\nEffective Price per Parcel:")
print(df[['Count', 'Service_Price', 'Effective_Price_Rounded']].sort_values('Effective_Price_Rounded'))

# Create visualizations
fig, axes = plt.subplots(2, 2, figsize=(15, 12))
fig.suptitle('Parcel Shipment: Price-Demand Relationship Analysis', fontsize=16, fontweight='bold')

# 1. Price vs Demand scatter plot
axes[0, 0].scatter(df['Effective_Price'], df['Count'], s=100, alpha=0.7, color='steelblue')
axes[0, 0].set_xlabel('Effective Price per Parcel', fontsize=12)
axes[0, 0].set_ylabel('Demand Count', fontsize=12)
axes[0, 0].set_title('Price vs Demand', fontsize=14, fontweight='bold')
axes[0, 0].grid(True, alpha=0.3)

# Add trend line
z = np.polyfit(df['Effective_Price'], df['Count'], 1)
p = np.poly1d(z)
axes[0, 0].plot(df['Effective_Price'], p(df['Effective_Price']), "r--", alpha=0.8, linewidth=2)

# 2. Discount vs Demand
axes[0, 1].scatter(df['Discount'], df['Count'], s=100, alpha=0.7, color='green')
axes[0, 1].set_xlabel('Discount (%)', fontsize=12)
axes[0, 1].set_ylabel('Demand Count', fontsize=12)
axes[0, 1].set_title('Discount vs Demand', fontsize=14, fontweight='bold')
axes[0, 1].grid(True, alpha=0.3)

# 3. Service Price vs Demand
axes[1, 0].scatter(df['Service_Price'], df['Count'], s=100, alpha=0.7, color='orange')
axes[1, 0].set_xlabel('Total Service Price', fontsize=12)
axes[1, 0].set_ylabel('Demand Count', fontsize=12)
axes[1, 0].set_title('Total Service Price vs Demand', fontsize=14, fontweight='bold')
axes[1, 0].grid(True, alpha=0.3)

# 4. Demand distribution
axes[1, 1].bar(range(len(df)), df['Count'], color='lightcoral', alpha=0.7)
axes[1, 1].set_xlabel('Data Points', fontsize=12)
axes[1, 1].set_ylabel('Demand Count', fontsize=12)
axes[1, 1].set_title('Demand Distribution', fontsize=14, fontweight='bold')
axes[1, 1].set_xticks(range(len(df)))
axes[1, 1].set_xticklabels([f'P{i+1}' for i in range(len(df))])
axes[1, 1].grid(True, alpha=0.3)

plt.tight_layout()
plt.show()

# Linear Demand Model: D(p) = a - b*p
print("\n=== LINEAR DEMAND MODEL ESTIMATION ===")
print("Model: D(p) = a - b*p")
print("Where: D = Demand, p = Effective Price per Parcel")

# Prepare data for regression
X = df['Effective_Price'].values.reshape(-1, 1)
y = df['Count'].values

# Fit linear regression
reg = LinearRegression()
reg.fit(X, y)

# Get coefficients
a = reg.intercept_  # intercept
b = -reg.coef_[0]  # price coefficient (negative because demand decreases with price)

print(f"\nEstimated Model: D(p) = {a:.2f} - {b:.6f}*p")
print(f"Intercept (a): {a:.2f}")
print(f"Price Coefficient (b): {b:.6f}")

# Model evaluation
y_pred = reg.predict(X)
r2 = r2_score(y, y_pred)
rmse = np.sqrt(mean_squared_error(y, y_pred))

print(f"\nModel Performance:")
print(f"R² Score: {r2:.4f}")
print(f"RMSE: {rmse:.2f}")

# Statistical significance test
slope, intercept, r_value, p_value, std_err = stats.linregress(df['Effective_Price'], df['Count'])

print(f"\nStatistical Significance:")
print(f"Correlation Coefficient (r): {r_value:.4f}")
print(f"P-value: {p_value:.4f}")
print(f"Standard Error: {std_err:.4f}")

# Price elasticity of demand
print(f"\n=== PRICE ELASTICITY ANALYSIS ===")
mean_price = df['Effective_Price'].mean()
mean_demand = df['Count'].mean()

# Point elasticity at mean values
elasticity = -b * (mean_price / mean_demand)
print(f"Price Elasticity of Demand at mean values: {elasticity:.4f}")

if abs(elasticity) > 1:
    print("Demand is ELASTIC (|elasticity| > 1)")
elif abs(elasticity) < 1:
    print("Demand is INELASTIC (|elasticity| < 1)")
else:
    print("Demand is UNIT ELASTIC (|elasticity| = 1)")

# Demand prediction for different price levels
print(f"\n=== DEMAND PREDICTIONS ===")
price_range = np.linspace(df['Effective_Price'].min(), df['Effective_Price'].max(), 10)
demand_predictions = a - b * price_range

prediction_df = pd.DataFrame({
    'Price_per_Parcel': price_range.round(2),
    'Predicted_Demand': demand_predictions.round(2)
})

print("Demand Predictions for Different Price Levels:")
print(prediction_df)

# Visualization of the demand model
plt.figure(figsize=(12, 8))

# Scatter plot of actual data
plt.scatter(df['Effective_Price'], df['Count'], s=150, alpha=0.8, color='steelblue', 
           label='Actual Data Points', zorder=5)

# Demand curve
plt.plot(price_range, demand_predictions, 'r-', linewidth=3, alpha=0.8, 
         label=f'Demand Model: D(p) = {a:.1f} - {b:.6f}*p')

# Confidence interval (simplified)
# For demonstration, we'll show the trend line with some uncertainty
plt.fill_between(price_range, demand_predictions * 0.8, demand_predictions * 1.2, 
                alpha=0.2, color='red', label='Approximate Confidence Region')

plt.xlabel('Effective Price per Parcel', fontsize=14)
plt.ylabel('Demand Count', fontsize=14)
plt.title('Linear Demand Model: D(p) = a - b*p', fontsize=16, fontweight='bold')
plt.legend(fontsize=12)
plt.grid(True, alpha=0.3)
plt.axhline(y=0, color='black', linestyle='-', alpha=0.3)
plt.axvline(x=0, color='black', linestyle='-', alpha=0.3)

# Add annotations for key insights
plt.annotate(f'Price Elasticity: {elasticity:.3f}', 
            xy=(0.7, 0.9), xycoords='axes fraction',
            bbox=dict(boxstyle="round,pad=0.3", facecolor="yellow", alpha=0.7),
            fontsize=10)

plt.annotate(f'R² = {r2:.3f}', 
            xy=(0.7, 0.8), xycoords='axes fraction',
            bbox=dict(boxstyle="round,pad=0.3", facecolor="lightgreen", alpha=0.7),
            fontsize=10)

plt.tight_layout()
plt.show()

# Summary of findings
print(f"\n=== SUMMARY OF FINDINGS ===")
print(f"1. The estimated demand model is: D(p) = {a:.2f} - {b:.6f}*p")
print(f"2. Price coefficient (b) = {b:.6f} indicates that for each unit increase in price,")
print(f"   demand decreases by approximately {b:.6f} units")
print(f"3. Price elasticity of demand = {elasticity:.4f}")
print(f"4. Model fit (R²) = {r2:.4f}")
print(f"5. The relationship between price and demand appears to be {'strong' if abs(r_value) > 0.7 else 'moderate' if abs(r_value) > 0.5 else 'weak'}")

if p_value < 0.05:
    print(f"6. The relationship is statistically significant (p-value = {p_value:.4f} < 0.05)")
else:
    print(f"6. The relationship is not statistically significant (p-value = {p_value:.4f} >= 0.05)")

print(f"\nNote: This analysis is based on limited data points. For more robust conclusions,")
print(f"consider collecting data across more price levels and time periods.")