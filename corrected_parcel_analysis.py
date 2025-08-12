#!/usr/bin/env python3
"""
Corrected Parcel Shipment Demand Analysis
This script analyzes the relationship between discount levels and demand for parcel shipments
and estimates a linear demand model: D(d) = a - b*d where d is discount percentage
"""

import math

def main():
    print("=== CORRECTED PARCEL SHIPMENT DEMAND ANALYSIS ===")
    print("Analyzing the relationship between discount levels and demand")
    print("Note: Service_Price represents TOTAL revenue for all parcels, not per-parcel price")
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
    
    # Calculate price per parcel (assuming Service_Price is total revenue)
    print("STEP 1: CALCULATING PRICE PER PARCEL")
    print("Price per Parcel = Service Price / Count")
    print("-" * 60)
    
    for i, row in enumerate(data):
        price_per_parcel = row['service_price'] / row['count']
        row['price_per_parcel'] = price_per_parcel
        print(f"Point {i+1}: {price_per_parcel:.2f} = {row['service_price']:.2f} / {row['count']}")
    
    print("\n" + "="*80)
    
    # Sort by discount for better analysis
    sorted_data = sorted(data, key=lambda x: x['discount'])
    
    print("STEP 2: DATA SORTED BY DISCOUNT LEVEL")
    print("Discount\tCount\tPrice_per_Parcel\tService_Price")
    print("-" * 70)
    for row in sorted_data:
        print(f"{row['discount']}%\t\t{row['count']}\t{row['price_per_parcel']:.2f}\t\t{row['service_price']:.2f}")
    
    print("\n" + "="*80)
    
    # Calculate basic statistics
    print("STEP 3: BASIC STATISTICS")
    print("-" * 30)
    
    discounts = [row['discount'] for row in data]
    counts = [row['count'] for row in data]
    prices_per_parcel = [row['price_per_parcel'] for row in data]
    
    mean_discount = sum(discounts) / len(discounts)
    mean_count = sum(counts) / len(counts)
    mean_price = sum(prices_per_parcel) / len(prices_per_parcel)
    
    print(f"Mean Discount: {mean_discount:.1f}%")
    print(f"Mean Demand Count: {mean_count:.2f}")
    print(f"Mean Price per Parcel: {mean_price:.2f}")
    print(f"Discount Range: {min(discounts):.1f}% to {max(discounts):.1f}%")
    print(f"Demand Range: {min(counts)} to {max(counts)}")
    print(f"Price Range: {min(prices_per_parcel):.2f} to {max(prices_per_parcel):.2f}")
    
    print("\n" + "="*80)
    
    # Analyze the relationship between discount and demand
    print("STEP 4: DISCOUNT-DEMAND RELATIONSHIP ANALYSIS")
    print("-" * 50)
    
    print("Key Observations:")
    print("1. No Discount (0%):")
    print(f"   - Demand: {data[0]['count']} parcels")
    print(f"   - Price per parcel: {data[0]['price_per_parcel']:.2f}")
    print()
    
    print("2. With Discounts (15-19%):")
    for row in data[1:]:
        print(f"   - {row['discount']}% discount: {row['count']} parcels at {row['price_per_parcel']:.2f} per parcel")
    
    print()
    print("3. Analysis:")
    print("   - Highest demand (238) occurs with NO discount (0%)")
    print("   - Lower demand occurs with higher discount levels")
    print("   - This suggests customers prefer the standard price over discounted prices")
    print("   - The relationship appears COUNTER-INTUITIVE to typical economics")
    
    print("\n" + "="*80)
    
    # Try to fit a linear model: D(d) = a - b*d where d is discount
    print("STEP 5: LINEAR DEMAND MODEL - D(d) = a - b*d")
    print("Where: D = Demand, d = Discount Percentage")
    print("-" * 60)
    
    # Calculate regression coefficients for discount vs demand
    n = len(data)
    
    # Calculate sums for regression
    sum_x = sum(discounts)
    sum_y = sum(counts)
    sum_xy = sum(discounts[i] * counts[i] for i in range(n))
    sum_x2 = sum(discounts[i] ** 2 for i in range(n))
    
    # Calculate regression coefficients
    numerator = n * sum_xy - sum_x * sum_y
    denominator = n * sum_x2 - sum_x ** 2
    
    if abs(denominator) < 1e-10:
        print("Error: Denominator is too small for regression")
        return
    
    b_discount = numerator / denominator
    a_discount = (sum_y - b_discount * sum_x) / n
    
    print(f"Discount-based model coefficients:")
    print(f"a (intercept) = {a_discount:.2f}")
    print(f"b (discount coefficient) = {b_discount:.4f}")
    print(f"Estimated model: D(d) = {a_discount:.2f} - {b_discount:.4f}*d")
    
    print("\n" + "="*80)
    
    # Model evaluation for discount model
    print("STEP 6: DISCOUNT MODEL EVALUATION")
    print("-" * 40)
    
    # Calculate predicted values and residuals
    predicted_counts_discount = []
    residuals_discount = []
    
    for i, row in enumerate(data):
        pred = a_discount - b_discount * row['discount']
        predicted_counts_discount.append(pred)
        residual = row['count'] - pred
        residuals_discount.append(residual)
    
    # Calculate R-squared
    ss_res = sum(r**2 for r in residuals_discount)
    ss_tot = sum((counts[i] - mean_count)**2 for i in range(n))
    r_squared_discount = 1 - (ss_res / ss_tot) if ss_tot > 0 else 0
    
    # Calculate correlation coefficient
    sum_xy_dev = sum((discounts[i] - mean_discount) * (counts[i] - mean_count) for i in range(n))
    sum_x_dev2 = sum((discounts[i] - mean_discount)**2 for i in range(n))
    sum_y_dev2 = sum((counts[i] - mean_count)**2 for i in range(n))
    
    correlation_discount = sum_xy_dev / math.sqrt(sum_x_dev2 * sum_y_dev2) if (sum_x_dev2 * sum_y_dev2) > 0 else 0
    
    print(f"R-squared: {r_squared_discount:.4f}")
    print(f"Correlation coefficient: {correlation_discount:.4f}")
    print(f"Root Mean Square Error: {math.sqrt(ss_res/n):.2f}")
    
    print("\n" + "="*80)
    
    # Try price per parcel model as well
    print("STEP 7: PRICE PER PARCEL MODEL - D(p) = a - b*p")
    print("Where: D = Demand, p = Price per Parcel")
    print("-" * 60)
    
    # Calculate regression coefficients for price vs demand
    sum_x = sum(prices_per_parcel)
    sum_y = sum(counts)
    sum_xy = sum(prices_per_parcel[i] * counts[i] for i in range(n))
    sum_x2 = sum(prices_per_parcel[i] ** 2 for i in range(n))
    
    # Calculate regression coefficients
    numerator = n * sum_xy - sum_x * sum_y
    denominator = n * sum_x2 - sum_x ** 2
    
    if abs(denominator) < 1e-10:
        print("Error: Denominator is too small for regression")
        return
    
    b_price = numerator / denominator
    a_price = (sum_y - b_price * sum_x) / n
    
    print(f"Price-based model coefficients:")
    print(f"a (intercept) = {a_price:.2f}")
    print(f"b (price coefficient) = {b_price:.6f}")
    print(f"Estimated model: D(p) = {a_price:.2f} - {b_price:.6f}*p")
    
    # Model evaluation for price model
    predicted_counts_price = []
    residuals_price = []
    
    for i, row in enumerate(data):
        pred = a_price - b_price * row['price_per_parcel']
        predicted_counts_price.append(pred)
        residual = row['count'] - pred
        residuals_price.append(residual)
    
    # Calculate R-squared for price model
    ss_res_price = sum(r**2 for r in residuals_price)
    r_squared_price = 1 - (ss_res_price / ss_tot) if ss_tot > 0 else 0
    
    # Calculate correlation coefficient for price model
    sum_xy_dev_price = sum((prices_per_parcel[i] - mean_price) * (counts[i] - mean_count) for i in range(n))
    sum_x_dev2_price = sum((prices_per_parcel[i] - mean_price)**2 for i in range(n))
    
    correlation_price = sum_xy_dev_price / math.sqrt(sum_x_dev2_price * sum_y_dev2) if (sum_x_dev2_price * sum_y_dev2) > 0 else 0
    
    print(f"\nPrice Model Performance:")
    print(f"R-squared: {r_squared_price:.4f}")
    print(f"Correlation coefficient: {correlation_price:.4f}")
    print(f"Root Mean Square Error: {math.sqrt(ss_res_price/n):.2f}")
    
    print("\n" + "="*80)
    
    # Answer the specific question
    print("STEP 8: ANSWERING YOUR SPECIFIC QUESTION")
    print("-" * 50)
    print("Q: What happens to demand (count) when we increased the service price?")
    print()
    
    print("Analysis:")
    print("1. The data shows a COUNTER-INTUITIVE pattern:")
    print(f"   - NO discount (0%): {data[0]['count']} parcels at {data[0]['price_per_parcel']:.2f} per parcel")
    print(f"   - WITH discounts (15-19%): Lower demand at lower prices")
    
    print("\n2. Possible Explanations:")
    print("   - Quality perception: Customers may associate higher prices with better service")
    print("   - Brand positioning: Standard pricing may signal reliability")
    print("   - Market segmentation: Different customer segments respond differently to pricing")
    print("   - Limited data: Only 5 data points may not capture the full relationship")
    
    print("\n3. Key Finding:")
    print("   - In your data, INCREASING the price (removing discounts) actually INCREASED demand")
    print("   - This contradicts the typical economic law of demand")
    
    print("\n" + "="*80)
    
    # Summary and recommendations
    print("STEP 9: SUMMARY AND RECOMMENDATIONS")
    print("-" * 40)
    
    print("1. Model Results:")
    print(f"   - Discount Model: D(d) = {a_discount:.2f} - {b_discount:.4f}*d")
    print(f"   - Price Model: D(p) = {a_price:.2f} - {b_price:.6f}*p")
    
    print("\n2. Key Insights:")
    print("   - Higher prices (no discounts) lead to HIGHER demand in your data")
    print("   - This suggests a unique market dynamic or data limitation")
    
    print("\n3. Recommendations:")
    print("   - Collect more data points across different price levels and time periods")
    print("   - Analyze customer segments and their price sensitivity")
    print("   - Consider other factors: seasonality, competition, service quality")
    print("   - Test different pricing strategies systematically")
    print("   - The current data suggests premium pricing might be more effective")
    
    print("\n4. Data Limitations:")
    print("   - Only 5 data points (insufficient for robust statistical analysis)")
    print("   - All data from same date (no time variation)")
    print("   - Limited price range variation")
    print("   - No control for other variables affecting demand")
    
    print("\n" + "="*80)
    print("Analysis Complete!")
    print("\nIMPORTANT: The counter-intuitive results suggest either:")
    print("1. A unique market dynamic where higher prices increase demand")
    print("2. Insufficient data to capture the true price-demand relationship")
    print("3. Other factors are driving demand more than price")

if __name__ == "__main__":
    main()