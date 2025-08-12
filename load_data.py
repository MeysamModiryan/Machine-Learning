import pandas as pd
import numpy as np
from parcel_demand_analysis import ParcelDemandAnalysis

def load_data_from_csv(filepath):
    """Load data from CSV file"""
    try:
        df = pd.read_csv(filepath)
        print(f"Successfully loaded {len(df)} rows from {filepath}")
        return df
    except Exception as e:
        print(f"Error loading CSV: {e}")
        return None

def load_data_from_excel(filepath, sheet_name=None):
    """Load data from Excel file"""
    try:
        df = pd.read_excel(filepath, sheet_name=sheet_name)
        print(f"Successfully loaded {len(df)} rows from {filepath}")
        return df
    except Exception as e:
        print(f"Error loading Excel: {e}")
        return None

def create_sample_extended_data():
    """Create a more comprehensive sample dataset for demonstration"""
    np.random.seed(42)
    
    # Generate dates for a month (Persian calendar)
    dates = ['1404/03/{:02d}'.format(i) for i in range(1, 31) for _ in range(10)]
    
    # Create sample data with price variations
    sample_data = []
    base_price = 3000
    
    for i, date in enumerate(dates):
        # Simulate price increase in the middle of the month
        day = int(date.split('/')[-1])
        if day <= 15:
            price_multiplier = 1.0  # Normal price
        else:
            price_multiplier = 1.2  # 20% price increase
            
        unit_price = base_price * price_multiplier
        
        # Simulate demand response to price (higher price = lower demand)
        base_demand = 50
        price_effect = -0.01 * (unit_price - base_price)  # Price elasticity
        
        # Add some randomness
        demand = max(1, int(base_demand + price_effect + np.random.normal(0, 10)))
        
        # Random discount
        discount = np.random.choice([0, 5, 10, 15, 17, 18, 19], p=[0.4, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1])
        
        # Calculate service price
        service_price = unit_price * demand
        
        sample_data.append({
            'Date': date,
            'Parcel_Type': np.random.choice(['ميني پک', 'استاندارد', 'سريع'], p=[0.6, 0.3, 0.1]),
            'Discount': discount,
            'Count': demand,
            'Service_Price': service_price
        })
    
    return pd.DataFrame(sample_data)

def validate_data_format(df):
    """Validate that the dataframe has the required columns"""
    required_columns = ['Date', 'Parcel_Type', 'Discount', 'Count', 'Service_Price']
    
    missing_columns = [col for col in required_columns if col not in df.columns]
    
    if missing_columns:
        print(f"Error: Missing required columns: {missing_columns}")
        print(f"Available columns: {list(df.columns)}")
        return False
    
    print("Data format validation successful!")
    return True

def run_analysis_with_data(df):
    """Run the complete demand analysis with the provided data"""
    if not validate_data_format(df):
        return None
    
    print("Starting Parcel Demand Analysis...")
    print("=" * 50)
    
    # Initialize and run analysis
    analysis = ParcelDemandAnalysis(df)
    
    # Run complete analysis
    print("\n1. Exploring data...")
    analysis.explore_data()
    
    print("\n2. Analyzing price changes...")
    daily_data = analysis.analyze_price_changes()
    
    print("\n3. Analyzing demand-price relationship...")
    correlations = analysis.analyze_demand_price_relationship()
    
    print("\n4. Estimating demand model...")
    model_results = analysis.estimate_demand_model()
    
    print("\n5. Creating visualizations...")
    analysis.create_visualizations(model_results)
    
    print("\n6. Generating report...")
    analysis.generate_report(model_results)
    
    print("\n" + "="*50)
    print("Analysis completed successfully!")
    print("Generated files:")
    print("- demand_analysis_plots.png")
    print("- discount_analysis_plots.png") 
    print("- demand_analysis_report.txt")
    
    return analysis, model_results

def main():
    """Main function with options to load data from different sources"""
    print("Parcel Demand Analysis Tool")
    print("=" * 30)
    print("Options:")
    print("1. Use sample data (demonstration)")
    print("2. Load from CSV file")
    print("3. Load from Excel file")
    print("4. Use provided sample data")
    
    # For automatic execution, let's use the extended sample data
    print("\nUsing extended sample data for demonstration...")
    
    # Create extended sample data
    df = create_sample_extended_data()
    print(f"Created sample dataset with {len(df)} observations")
    print(f"Date range: {df['Date'].min()} to {df['Date'].max()}")
    print(f"Parcel types: {', '.join(df['Parcel_Type'].unique())}")
    
    # Run analysis
    analysis, results = run_analysis_with_data(df)
    
    return analysis, results

if __name__ == "__main__":
    analysis, results = main()