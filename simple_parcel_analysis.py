#!/usr/bin/env python3
"""
Simple Parcel Shipment Demand Analysis
This script analyzes the relationship between price and demand for parcel shipments
and estimates a linear demand model: D(p) = a - b*p
"""

import math

def main():
    print("=== PARCEL SHIPMENT DEMAND ANALYSIS ===")
    print("Analyzing the relationship between price and demand")
    print()
    
    # Your data
    data = [
        {'date': '1404/03/03', 'parcel_type': 'ميني پک', 'discount': 0.0, 'count': 238, 'service_price': 772320.168067},
        {'date': '1404/03/03', 'parcel_type': 'ميني پک', 'discount': 15.0, 'count': 4, 'service_price': 709400.000000},
        {'date': '1404/03/03', 'parcel_type': 'ميني پک', 'discount': 17.0, 'count': 100, 'service_price': 736402.800000},
        {'date': '1404/03/03', 'parcel_type': 'ميني پک', 'discount': 18.0, 'count': 4, 'service_price': 724400.000000},
        {'date': '1404/03/03', 'parcel_type': 'ميني پک', 'discount': 19.0, 'count': 32, 'service_price': 715025.000000}
    ]
    
    print("Original Data:")
    print("Date\t\tParcel_Type\tDiscount\tCount\tService_Price")
    print("-" * 80)
    for row in data:
        print(f"{row['date']}\t{row['parcel_type']}\t{row['discount']}%\t\t{row['count']}\t{row['service_price']:.2f}")
    
    print("\n" + "="*80)
    
    # Calculate effective price per parcel
    print("STEP 1: CALCULATING EFFECTIVE PRICE PER PARCEL")
    print("Effective Price = Service Price / Count")
    print("-" * 60)
    
    for i, row in enumerate(data):
        effective_price = row['service_price'] / row['count']
        row['effective_price'] = effective_price
        print(f"Point {i+1}: {effective_price:.2f} = {row['service_price']:.2f} / {row['count']}")
    
    print("\n" + "="*80)
    
    # Sort by effective price for better analysis
    sorted_data = sorted(data, key=lambda x: x['effective_price'])
    
    print("STEP 2: DATA SORTED BY EFFECTIVE PRICE")
    print("Price\t\tCount\tDiscount\tService_Price")
    print("-" * 60)
    for row in sorted_data:
        print(f"{row['effective_price']:.2f}\t\t{row['count']}\t{row['discount']}%\t\t{row['service_price']:.2f}")
    
    print("\n" + "="*80)
    
    # Calculate basic statistics
    print("STEP 3: BASIC STATISTICS")
    print("-" * 30)
    
    prices = [row['effective_price'] for row in data]
    counts = [row['count'] for row in data]
    
    mean_price = sum(prices) / len(prices)
    mean_count = sum(counts) / len(counts)
    
    print(f"Mean Effective Price: {mean_price:.2f}")
    print(f"Mean Demand Count: {mean_count:.2f}")
    print(f"Price Range: {min(prices):.2f} to {max(prices):.2f}")
    print(f"Demand Range: {min(counts)} to {max(counts)}")
    
    print("\n" + "="*80)
    
    # Manual linear regression calculation
    print("STEP 4: LINEAR REGRESSION - D(p) = a - b*p")
    print("Using least squares method to estimate a and b")
    print("-" * 60)
    
    # Calculate means
    n = len(data)
    
    # Calculate sums for regression
    sum_x = sum(prices)
    sum_y = sum(counts)
    sum_xy = sum(prices[i] * counts[i] for i in range(n))
    sum_x2 = sum(prices[i] ** 2 for i in range(n))
    
    # Calculate regression coefficients
    # b = (n*sum_xy - sum_x*sum_y) / (n*sum_x2 - sum_x^2)
    # a = (sum_y - b*sum_x) / n
    
    numerator = n * sum_xy - sum_x * sum_y
    denominator = n * sum_x2 - sum_x ** 2
    
    if abs(denominator) < 1e-10:
        print("Error: Denominator is too small for regression")
        return
    
    b = numerator / denominator
    a = (sum_y - b * sum_x) / n
    
    print(f"Calculated coefficients:")
    print(f"a (intercept) = {a:.2f}")
    print(f"b (price coefficient) = {b:.6f}")
    print(f"Estimated model: D(p) = {a:.2f} - {b:.6f}*p")
    
    print("\n" + "="*80)
    
    # Model evaluation
    print("STEP 5: MODEL EVALUATION")
    print("-" * 30)
    
    # Calculate predicted values and residuals
    predicted_counts = []
    residuals = []
    
    for i, row in enumerate(data):
        pred = a - b * row['effective_price']
        predicted_counts.append(pred)
        residual = row['count'] - pred
        residuals.append(residual)
    
    # Calculate R-squared
    ss_res = sum(r**2 for r in residuals)
    ss_tot = sum((counts[i] - mean_count)**2 for i in range(n))
    r_squared = 1 - (ss_res / ss_tot) if ss_tot > 0 else 0
    
    # Calculate correlation coefficient
    sum_xy_dev = sum((prices[i] - mean_price) * (counts[i] - mean_count) for i in range(n))
    sum_x_dev2 = sum((prices[i] - mean_price)**2 for i in range(n))
    sum_y_dev2 = sum((counts[i] - mean_count)**2 for i in range(n))
    
    correlation = sum_xy_dev / math.sqrt(sum_x_dev2 * sum_y_dev2) if (sum_x_dev2 * sum_y_dev2) > 0 else 0
    
    print(f"R-squared: {r_squared:.4f}")
    print(f"Correlation coefficient: {correlation:.4f}")
    print(f"Root Mean Square Error: {math.sqrt(ss_res/n):.2f}")
    
    print("\n" + "="*80)
    
    # Price elasticity analysis
    print("STEP 6: PRICE ELASTICITY ANALYSIS")
    print("-" * 40)
    
    # Point elasticity at mean values
    elasticity = -b * (mean_price / mean_count)
    print(f"Price Elasticity of Demand at mean values: {elasticity:.4f}")
    
    if abs(elasticity) > 1:
        print("Demand is ELASTIC (|elasticity| > 1)")
        print("A 1% increase in price leads to more than 1% decrease in demand")
    elif abs(elasticity) < 1:
        print("Demand is INELASTIC (|elasticity| < 1)")
        print("A 1% increase in price leads to less than 1% decrease in demand")
    else:
        print("Demand is UNIT ELASTIC (|elasticity| = 1)")
        print("A 1% increase in price leads to exactly 1% decrease in demand")
    
    print("\n" + "="*80)
    
    # Demand predictions
    print("STEP 7: DEMAND PREDICTIONS")
    print("Using the estimated model for different price levels")
    print("-" * 60)
    
    min_price = min(prices)
    max_price = max(prices)
    price_step = (max_price - min_price) / 9
    
    print("Price\t\tPredicted Demand")
    print("-" * 30)
    
    for i in range(10):
        price = min_price + i * price_step
        predicted_demand = a - b * price
        print(f"{price:.2f}\t\t{predicted_demand:.1f}")
    
    print("\n" + "="*80)
    
    # Analysis of your specific question
    print("STEP 8: ANSWERING YOUR SPECIFIC QUESTION")
    print("-" * 50)
    print("Q: What happens to demand (count) when we increased the service price?")
    print()
    
    # Find the relationship between price and demand
    print("Analysis of the data:")
    print("1. When discount = 0% (no discount):")
    print(f"   - Price per parcel: {data[0]['effective_price']:.2f}")
    print(f"   - Demand: {data[0]['count']} parcels")
    print()
    
    print("2. When discount = 15-19% (price reduction):")
    for row in data[1:]:
        print(f"   - Discount {row['discount']}%: Price {row['effective_price']:.2f}, Demand {row['count']}")
    
    print()
    print("3. Key Observations:")
    print(f"   - Highest demand ({data[0]['count']} parcels) at highest price ({data[0]['effective_price']:.2f})")
    print(f"   - Lower demand at lower prices (with discounts)")
    print(f"   - This suggests an INVERSE relationship between price and demand")
    
    print("\n" + "="*80)
    
    # Summary and recommendations
    print("STEP 9: SUMMARY AND RECOMMENDATIONS")
    print("-" * 40)
    
    print(f"1. Estimated Demand Model: D(p) = {a:.2f} - {b:.6f}*p")
    print(f"2. Price coefficient (b) = {b:.6f}")
    print(f"   - For each unit increase in price, demand decreases by {b:.6f} units")
    print(f"3. Price elasticity = {elasticity:.4f}")
    print(f"4. Model fit (R²) = {r_squared:.4f}")
    
    print("\n5. Business Implications:")
    if b > 0:
        print("   - Increasing price will decrease demand")
        print("   - The magnitude of this effect is captured by b")
    else:
        print("   - The model suggests an unusual relationship")
        print("   - Consider reviewing the data or model assumptions")
    
    print("\n6. Recommendations:")
    print("   - Collect more data points across different price levels")
    print("   - Consider seasonal and time-based factors")
    print("   - Analyze other factors that might affect demand")
    print("   - Use the model for pricing strategy decisions")
    
    print("\n" + "="*80)
    print("Analysis Complete!")

if __name__ == "__main__":
    main()