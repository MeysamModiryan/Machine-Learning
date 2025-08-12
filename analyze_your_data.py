#!/usr/bin/env python3

# Parcel Demand Analysis - CSV Data Version
# This script reads your parcel data from a CSV file and performs demand analysis

import sys
import csv

def read_csv_data(filename):
    """Read parcel data from CSV file"""
    data = []
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                # Convert numeric fields
                data.append({
                    'Date': row['Date'],
                    'Parcel_Type': row['Parcel_Type'],
                    'Discount': float(row['Discount']),
                    'Count': int(row['Count']),
                    'Service_Price': float(row['Service_Price'])
                })
        print(f"✓ Successfully loaded {len(data)} records from {filename}")
        return data
    except FileNotFoundError:
        print(f"❌ Error: File '{filename}' not found")
        return None
    except Exception as e:
        print(f"❌ Error reading file: {e}")
        return None

def calculate_unit_price(service_price, count):
    """Calculate unit price from service price and count"""
    return service_price / count if count > 0 else 0

def calculate_price_after_discount(unit_price, discount):
    """Calculate price after applying discount"""
    return unit_price * (1 - discount/100)

def calculate_correlation(x_values, y_values):
    """Calculate correlation coefficient between two lists"""
    import math
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

def analyze_price_changes_over_time(data):
    """Analyze how prices changed over different dates"""
    print("\n📅 PRICE CHANGES OVER TIME")
    print("-" * 30)
    
    # Group by date
    date_summary = {}
    for row in data:
        date = row['Date']
        unit_price = calculate_unit_price(row['Service_Price'], row['Count'])
        
        if date not in date_summary:
            date_summary[date] = {
                'total_demand': 0,
                'prices': [],
                'total_revenue': 0
            }
        
        date_summary[date]['total_demand'] += row['Count']
        date_summary[date]['prices'].append(unit_price)
        date_summary[date]['total_revenue'] += row['Service_Price']
    
    # Sort by date and show summary
    sorted_dates = sorted(date_summary.keys())
    
    print(f"{'Date':<12} {'Avg Price':<12} {'Total Demand':<12} {'Total Revenue':<15}")
    print("-" * 55)
    
    prev_price = None
    for date in sorted_dates:
        avg_price = sum(date_summary[date]['prices']) / len(date_summary[date]['prices'])
        total_demand = date_summary[date]['total_demand']
        total_revenue = date_summary[date]['total_revenue']
        
        price_change = ""
        if prev_price:
            change_pct = ((avg_price - prev_price) / prev_price) * 100
            if change_pct > 5:
                price_change = f"↗ +{change_pct:.1f}%"
            elif change_pct < -5:
                price_change = f"↘ {change_pct:.1f}%"
        
        print(f"{date:<12} {avg_price:<12.0f} {total_demand:<12} {total_revenue:<15.0f} {price_change}")
        prev_price = avg_price
    
    return date_summary

def analyze_parcel_data(data):
    """Main analysis function"""
    print("🚚 PARCEL DEMAND ANALYSIS")
    print("=" * 40)
    
    # Data preparation
    print("\n📊 DATA OVERVIEW")
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
    
    print(f"📈 Total observations: {len(data)}")
    print(f"💰 Unit price range: {min(unit_prices):,.0f} - {max(unit_prices):,.0f}")
    print(f"📦 Demand range: {min(demands)} - {max(demands)}")
    print(f"🏷️  Average discount: {sum(row['Discount'] for row in data)/len(data):.1f}%")
    print(f"📅 Date range: {min(row['Date'] for row in data)} to {max(row['Date'] for row in data)}")
    
    # Unique parcel types
    parcel_types = list(set(row['Parcel_Type'] for row in data))
    print(f"📋 Parcel types: {', '.join(parcel_types)}")
    
    # Time analysis
    analyze_price_changes_over_time(data)
    
    # Correlation analysis
    print("\n🔗 CORRELATION ANALYSIS")
    print("-" * 25)
    
    corr_price_demand = calculate_correlation(unit_prices, demands)
    corr_discount_price_demand = calculate_correlation(prices_after_discount, demands)
    
    print(f"📊 Unit Price ↔ Demand: {corr_price_demand:.4f}")
    print(f"📊 Price After Discount ↔ Demand: {corr_discount_price_demand:.4f}")
    
    # Interpretation
    if corr_price_demand < -0.7:
        print("   → Strong negative relationship ✅")
    elif corr_price_demand < -0.4:
        print("   → Moderate negative relationship ◐")
    elif corr_price_demand < -0.1:
        print("   → Weak negative relationship ⚠️")
    else:
        print("   → No clear negative relationship ❌")
    
    # Linear regression for demand model
    print("\n🎯 DEMAND MODEL ESTIMATION")
    print("-" * 30)
    
    # Using unit price
    slope, intercept, r2 = linear_regression(unit_prices, demands)
    
    print(f"📐 Estimated Demand Function: D(p) = {intercept:.2f} - {-slope:.6f}*p")
    print(f"📊 Intercept (a): {intercept:.4f}")
    print(f"📉 Price Coefficient (b): {-slope:.6f}")
    print(f"📈 R-squared: {r2:.4f} ({r2*100:.1f}% explained)")
    
    # Model quality assessment
    if r2 > 0.7:
        print("   → Excellent model fit! 🌟")
    elif r2 > 0.5:
        print("   → Good model fit ✅")
    elif r2 > 0.3:
        print("   → Moderate model fit ◐")
    else:
        print("   → Weak model fit - consider other factors ⚠️")
    
    # Price elasticity
    mean_price = sum(unit_prices) / len(unit_prices)
    mean_demand = sum(demands) / len(demands)
    elasticity = (slope * mean_price) / mean_demand if mean_demand != 0 else 0
    
    print(f"\n🎚️  PRICE ELASTICITY: {elasticity:.4f}")
    if abs(elasticity) > 1:
        print("   → Elastic demand (price-sensitive customers) 🔄")
    else:
        print("   → Inelastic demand (less price-sensitive) 🔒")
    
    # Business recommendations
    print(f"\n💡 BUSINESS INSIGHTS")
    print("-" * 20)
    
    if corr_price_demand < -0.5 and r2 > 0.3:
        print("✅ Price-demand relationship confirmed!")
        print("✅ Linear model provides reasonable fit")
        
        if abs(elasticity) < 1:
            print("💰 Opportunity: Modest price increases may boost revenue")
        else:
            print("⚠️  Caution: Customers are price-sensitive")
            
    elif len(data) < 10:
        print("📊 Recommendation: Collect more data for robust analysis")
        print("🔍 Current sample size may limit statistical confidence")
    
    else:
        print("🔍 Consider additional factors affecting demand:")
        print("   • Seasonal patterns")
        print("   • Marketing campaigns") 
        print("   • Competitor pricing")
        print("   • Service quality changes")
    
    return {
        'intercept': intercept,
        'slope': slope,
        'r2': r2,
        'correlation': corr_price_demand,
        'elasticity': elasticity,
        'n_observations': len(data)
    }

def main():
    """Main function"""
    print("🚚 PARCEL DEMAND ANALYZER")
    print("=" * 30)
    
    # Check command line argument for CSV file
    if len(sys.argv) > 1:
        csv_file = sys.argv[1]
    else:
        csv_file = 'data_template.csv'  # Default file
    
    print(f"📁 Loading data from: {csv_file}")
    
    # Load data
    data = read_csv_data(csv_file)
    if not data:
        print("\n❌ Could not load data. Please check your CSV file.")
        print("📋 Expected format:")
        print("   Date,Parcel_Type,Discount,Count,Service_Price")
        print("   1404/03/03,ميني پک,0.0,238,772320.168067")
        return None
    
    # Run analysis
    results = analyze_parcel_data(data)
    
    # Final summary
    print("\n" + "="*50)
    print("📋 ANALYSIS SUMMARY")
    print("="*50)
    print(f"🎯 Your demand function: D(p) = {results['intercept']:.0f} - {-results['slope']:.6f}*p")
    print(f"📊 Model explains {results['r2']*100:.1f}% of demand variation")
    print(f"🔗 Price-demand correlation: {results['correlation']:.3f}")
    print(f"📊 Based on {results['n_observations']} observations")
    
    if results['correlation'] < -0.5:
        print("\n🎉 SUCCESS: Strong price-demand relationship confirmed!")
        print("💼 Your pricing strategy analysis is statistically supported.")
    else:
        print("\n💭 INSIGHT: Consider expanding your dataset or examining other demand factors.")
    
    return results

if __name__ == "__main__":
    results = main()