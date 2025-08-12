#!/usr/bin/env python3

# Simple Parcel Demand Analysis
# This script analyzes the relationship between price and demand for parcel shipping

import sys
import math

def calculate_unit_price(service_price, count):
    """Calculate unit price from service price and count"""
    return service_price / count if count > 0 else 0

def calculate_price_after_discount(unit_price, discount):
    """Calculate price after applying discount"""
    return unit_price * (1 - discount/100)

def calculate_correlation(x_values, y_values):
    """Calculate correlation coefficient between two lists"""
    n = len(x_values)
    if n == 0:
        return 0
    
    # Calculate means
    mean_x = sum(x_values) / n
    mean_y = sum(y_values) / n
    
    # Calculate correlation
    numerator = sum((x_values[i] - mean_x) * (y_values[i] - mean_y) for i in range(n))
    
    sum_sq_x = sum((x_values[i] - mean_x) ** 2 for i in range(n))
    sum_sq_y = sum((y_values[i] - mean_y) ** 2 for i in range(n))
    
    denominator = math.sqrt(sum_sq_x * sum_sq_y)
    
    return numerator / denominator if denominator != 0 else 0

def linear_regression(x_values, y_values):
    """Perform simple linear regression and return slope, intercept, r2"""
    n = len(x_values)
    if n == 0:
        return 0, 0, 0
    
    # Calculate means
    mean_x = sum(x_values) / n
    mean_y = sum(y_values) / n
    
    # Calculate slope (b)
    numerator = sum((x_values[i] - mean_x) * (y_values[i] - mean_y) for i in range(n))
    denominator = sum((x_values[i] - mean_x) ** 2 for i in range(n))
    
    slope = numerator / denominator if denominator != 0 else 0
    
    # Calculate intercept (a)
    intercept = mean_y - slope * mean_x
    
    # Calculate R-squared
    y_pred = [intercept + slope * x for x in x_values]
    ss_res = sum((y_values[i] - y_pred[i]) ** 2 for i in range(n))
    ss_tot = sum((y_values[i] - mean_y) ** 2 for i in range(n))
    
    r2 = 1 - (ss_res / ss_tot) if ss_tot != 0 else 0
    
    return slope, intercept, r2

def analyze_parcel_data(data):
    """Main analysis function"""
    print("=== PARCEL DEMAND ANALYSIS ===\n")
    
    # Data preparation
    print("1. DATA PREPARATION")
    print("-" * 20)
    
    unit_prices = []
    prices_after_discount = []
    demands = []
    
    for row in data:
        unit_price = calculate_unit_price(row['Service_Price'], row['Count'])
        price_after_discount = calculate_price_after_discount(unit_price, row['Discount'])
        
        unit_prices.append(unit_price)
        prices_after_discount.append(price_after_discount)
        demands.append(row['Count'])
    
    print(f"Total observations: {len(data)}")
    print(f"Unit price range: {min(unit_prices):.2f} - {max(unit_prices):.2f}")
    print(f"Demand range: {min(demands)} - {max(demands)}")
    print(f"Average discount: {sum(row['Discount'] for row in data)/len(data):.1f}%")
    
    # Correlation analysis
    print("\n2. CORRELATION ANALYSIS")
    print("-" * 25)
    
    corr_price_demand = calculate_correlation(unit_prices, demands)
    corr_discount_price_demand = calculate_correlation(prices_after_discount, demands)
    
    print(f"Correlation (Unit Price vs Demand): {corr_price_demand:.4f}")
    print(f"Correlation (Price After Discount vs Demand): {corr_discount_price_demand:.4f}")
    
    # Linear regression for demand model
    print("\n3. DEMAND MODEL ESTIMATION")
    print("-" * 30)
    
    # Using unit price
    slope, intercept, r2 = linear_regression(unit_prices, demands)
    
    print(f"Estimated Demand Function: D(p) = {intercept:.2f} + ({slope:.4f})*p")
    print(f"In standard form: D(p) = {intercept:.2f} - {-slope:.4f}*p")
    print(f"Intercept (a): {intercept:.4f}")
    print(f"Price Coefficient (b): {-slope:.4f}")
    print(f"R-squared: {r2:.4f}")
    
    # Interpretation
    print("\n4. INTERPRETATION")
    print("-" * 18)
    
    if slope < 0:
        print("✓ Negative slope confirms expected downward-sloping demand curve")
        print(f"  For every 1 unit increase in price, demand decreases by {-slope:.2f} units")
    else:
        print("⚠ Positive slope suggests unusual demand behavior (investigate further)")
    
    if r2 > 0.7:
        print(f"✓ Strong model fit (R² = {r2:.3f}) - price explains {r2*100:.1f}% of demand variation")
    elif r2 > 0.4:
        print(f"◐ Moderate model fit (R² = {r2:.3f}) - price explains {r2*100:.1f}% of demand variation")
    else:
        print(f"⚠ Weak model fit (R² = {r2:.3f}) - other factors may be more important")
    
    # Price elasticity
    mean_price = sum(unit_prices) / len(unit_prices)
    mean_demand = sum(demands) / len(demands)
    elasticity = (slope * mean_price) / mean_demand if mean_demand != 0 else 0
    
    print(f"Price elasticity of demand: {elasticity:.4f}")
    if abs(elasticity) > 1:
        print("  → Demand is price elastic (responsive to price changes)")
    else:
        print("  → Demand is price inelastic (less responsive to price changes)")
    
    # Alternative model with discount prices
    print("\n5. ALTERNATIVE MODEL (Price After Discount)")
    print("-" * 45)
    
    slope_alt, intercept_alt, r2_alt = linear_regression(prices_after_discount, demands)
    
    print(f"D(p) = {intercept_alt:.2f} - {-slope_alt:.4f}*p")
    print(f"R-squared: {r2_alt:.4f}")
    
    if r2_alt > r2:
        print("→ Price after discount provides better model fit")
    else:
        print("→ Unit price provides better model fit")
    
    return {
        'intercept': intercept,
        'slope': slope,
        'r2': r2,
        'correlation': corr_price_demand,
        'elasticity': elasticity
    }

def main():
    """Main function with sample data"""
    
    # Sample data from your example
    sample_data = [
        {'Date': '1404/03/03', 'Parcel_Type': 'ميني پک', 'Discount': 0.0, 'Count': 238, 'Service_Price': 772320.168067},
        {'Date': '1404/03/03', 'Parcel_Type': 'ميني پک', 'Discount': 15.0, 'Count': 4, 'Service_Price': 709400.000000},
        {'Date': '1404/03/03', 'Parcel_Type': 'ميني پک', 'Discount': 17.0, 'Count': 100, 'Service_Price': 736402.800000},
        {'Date': '1404/03/03', 'Parcel_Type': 'ميني پک', 'Discount': 18.0, 'Count': 4, 'Service_Price': 724400.000000},
        {'Date': '1404/03/03', 'Parcel_Type': 'ميني پک', 'Discount': 19.0, 'Count': 32, 'Service_Price': 715025.000000},
    ]
    
    print("Analyzing your parcel shipment data...\n")
    
    results = analyze_parcel_data(sample_data)
    
    print("\n" + "="*50)
    print("SUMMARY")
    print("="*50)
    print(f"Your demand function: D(p) = {results['intercept']:.0f} - {-results['slope']:.4f}*p")
    print(f"Model explains {results['r2']*100:.1f}% of demand variation")
    print(f"Price-demand correlation: {results['correlation']:.3f}")
    
    if results['correlation'] < -0.5:
        print("\n📊 BUSINESS INSIGHT:")
        print("Strong negative correlation confirms that price increases reduce demand.")
        print("This validates your pricing strategy analysis.")
    else:
        print("\n⚠️  NOTE:")
        print("Weak price-demand relationship detected. Consider:")
        print("- Larger dataset needed for robust analysis")
        print("- Other factors affecting demand (season, competition, etc.)")
        print("- Different price ranges or time periods")
    
    print("\n📝 To use with your full dataset:")
    print("1. Save your data as CSV with columns: Date, Parcel_Type, Discount, Count, Service_Price")
    print("2. Modify the sample_data variable in this script")
    print("3. Run the analysis again")
    
    return results

if __name__ == "__main__":
    results = main()