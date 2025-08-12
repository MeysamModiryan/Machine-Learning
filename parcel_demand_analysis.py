import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
from scipy import stats
import warnings
warnings.filterwarnings('ignore')

# Set up matplotlib for better visualization
plt.style.use('seaborn-v0_8')
plt.rcParams['figure.figsize'] = (12, 8)

class ParcelDemandAnalysis:
    def __init__(self, data):
        """Initialize the analysis with parcel data"""
        self.data = data.copy()
        self.prepare_data()
        
    def prepare_data(self):
        """Prepare and clean the data for analysis"""
        # Convert Date to datetime if needed
        if self.data['Date'].dtype == 'object':
            # Handle Persian date format if necessary
            print("Date column detected as object type")
            
        # Calculate actual unit price (service_price / count)
        self.data['Unit_Price'] = self.data['Service_Price'] / self.data['Count']
        
        # Calculate price after discount
        self.data['Price_After_Discount'] = self.data['Unit_Price'] * (1 - self.data['Discount']/100)
        
        print("Data preparation completed")
        print(f"Dataset shape: {self.data.shape}")
        print(f"Date range: {self.data['Date'].min()} to {self.data['Date'].max()}")
        
    def explore_data(self):
        """Explore the dataset structure and basic statistics"""
        print("=== DATA EXPLORATION ===")
        print("\nDataset Info:")
        print(self.data.info())
        
        print("\nBasic Statistics:")
        print(self.data.describe())
        
        print("\nParcel Types:")
        print(self.data['Parcel_Type'].value_counts())
        
        print("\nDiscount Distribution:")
        print(self.data['Discount'].value_counts().sort_index())
        
        return self.data.describe()
    
    def analyze_price_changes(self):
        """Analyze price changes over time"""
        print("\n=== PRICE CHANGE ANALYSIS ===")
        
        # Group by date to see daily aggregates
        daily_data = self.data.groupby('Date').agg({
            'Count': 'sum',
            'Service_Price': 'sum',
            'Unit_Price': 'mean',
            'Price_After_Discount': 'mean'
        }).reset_index()
        
        print("\nDaily Summary Statistics:")
        print(daily_data.describe())
        
        # Identify potential price increase points
        daily_data['Price_Change'] = daily_data['Unit_Price'].diff()
        price_increases = daily_data[daily_data['Price_Change'] > 0]
        
        if len(price_increases) > 0:
            print(f"\nDetected {len(price_increases)} days with price increases:")
            print(price_increases[['Date', 'Unit_Price', 'Price_Change']])
        
        return daily_data
    
    def analyze_demand_price_relationship(self):
        """Analyze the relationship between price and demand"""
        print("\n=== DEMAND-PRICE RELATIONSHIP ANALYSIS ===")
        
        # Calculate correlation between price and demand
        price_demand_corr = self.data['Unit_Price'].corr(self.data['Count'])
        print(f"Correlation between Unit Price and Count: {price_demand_corr:.4f}")
        
        price_after_discount_corr = self.data['Price_After_Discount'].corr(self.data['Count'])
        print(f"Correlation between Price After Discount and Count: {price_after_discount_corr:.4f}")
        
        # Group by price levels to see demand patterns
        price_bins = pd.cut(self.data['Unit_Price'], bins=10)
        price_demand_summary = self.data.groupby(price_bins).agg({
            'Count': ['mean', 'sum', 'std'],
            'Unit_Price': 'mean'
        }).round(2)
        
        print("\nDemand by Price Ranges:")
        print(price_demand_summary)
        
        return price_demand_corr, price_after_discount_corr
    
    def estimate_demand_model(self):
        """Estimate the linear demand model D(p) = a - b*p"""
        print("\n=== DEMAND MODEL ESTIMATION ===")
        
        # Prepare data for regression
        X = self.data[['Unit_Price']]  # Independent variable (price)
        y = self.data['Count']  # Dependent variable (demand)
        
        # Fit linear regression model
        model = LinearRegression()
        model.fit(X, y)
        
        # Get predictions
        y_pred = model.predict(X)
        
        # Extract coefficients
        intercept = model.intercept_  # a
        slope = model.coef_[0]  # -b (should be negative for downward sloping demand)
        
        # Calculate model performance metrics
        r2 = r2_score(y, y_pred)
        
        # Perform statistical tests
        n = len(y)
        residuals = y - y_pred
        mse = np.mean(residuals**2)
        std_error = np.sqrt(mse)
        
        print(f"Estimated Demand Function: D(p) = {intercept:.2f} - {-slope:.2f}*p")
        print(f"Intercept (a): {intercept:.4f}")
        print(f"Price Coefficient (b): {-slope:.4f}")
        print(f"R-squared: {r2:.4f}")
        print(f"Standard Error: {std_error:.4f}")
        
        # Also try with price after discount
        X_discount = self.data[['Price_After_Discount']]
        model_discount = LinearRegression()
        model_discount.fit(X_discount, y)
        y_pred_discount = model_discount.predict(X_discount)
        r2_discount = r2_score(y, y_pred_discount)
        
        print(f"\nAlternative Model (Price After Discount):")
        print(f"D(p) = {model_discount.intercept_:.2f} - {-model_discount.coef_[0]:.2f}*p")
        print(f"R-squared: {r2_discount:.4f}")
        
        return {
            'model': model,
            'intercept': intercept,
            'slope': slope,
            'r2': r2,
            'model_discount': model_discount,
            'r2_discount': r2_discount
        }
    
    def create_visualizations(self, model_results):
        """Create visualizations for the analysis"""
        print("\n=== CREATING VISUALIZATIONS ===")
        
        fig, axes = plt.subplots(2, 2, figsize=(15, 12))
        
        # 1. Scatter plot: Price vs Demand
        axes[0,0].scatter(self.data['Unit_Price'], self.data['Count'], alpha=0.6)
        axes[0,0].set_xlabel('Unit Price')
        axes[0,0].set_ylabel('Demand (Count)')
        axes[0,0].set_title('Price vs Demand Relationship')
        
        # Add regression line
        X_range = np.linspace(self.data['Unit_Price'].min(), self.data['Unit_Price'].max(), 100)
        y_range = model_results['intercept'] + model_results['slope'] * X_range
        axes[0,0].plot(X_range, y_range, 'r-', linewidth=2, 
                      label=f'D(p) = {model_results["intercept"]:.0f} - {-model_results["slope"]:.2f}*p')
        axes[0,0].legend()
        
        # 2. Time series: Demand over time
        daily_data = self.data.groupby('Date')['Count'].sum().reset_index()
        axes[0,1].plot(daily_data['Date'], daily_data['Count'], marker='o')
        axes[0,1].set_xlabel('Date')
        axes[0,1].set_ylabel('Total Daily Demand')
        axes[0,1].set_title('Demand Over Time')
        axes[0,1].tick_params(axis='x', rotation=45)
        
        # 3. Time series: Price over time
        daily_price = self.data.groupby('Date')['Unit_Price'].mean().reset_index()
        axes[1,0].plot(daily_price['Date'], daily_price['Unit_Price'], marker='o', color='orange')
        axes[1,0].set_xlabel('Date')
        axes[1,0].set_ylabel('Average Unit Price')
        axes[1,0].set_title('Price Over Time')
        axes[1,0].tick_params(axis='x', rotation=45)
        
        # 4. Residual plot
        y_pred = model_results['model'].predict(self.data[['Unit_Price']])
        residuals = self.data['Count'] - y_pred
        axes[1,1].scatter(y_pred, residuals, alpha=0.6)
        axes[1,1].axhline(y=0, color='r', linestyle='--')
        axes[1,1].set_xlabel('Predicted Demand')
        axes[1,1].set_ylabel('Residuals')
        axes[1,1].set_title('Residual Plot')
        
        plt.tight_layout()
        plt.savefig('/workspace/demand_analysis_plots.png', dpi=300, bbox_inches='tight')
        plt.show()
        
        # Create additional plot for discount analysis
        plt.figure(figsize=(12, 6))
        
        plt.subplot(1, 2, 1)
        discount_demand = self.data.groupby('Discount')['Count'].sum()
        plt.bar(discount_demand.index, discount_demand.values)
        plt.xlabel('Discount Percentage')
        plt.ylabel('Total Demand')
        plt.title('Demand by Discount Level')
        
        plt.subplot(1, 2, 2)
        plt.scatter(self.data['Price_After_Discount'], self.data['Count'], alpha=0.6)
        plt.xlabel('Price After Discount')
        plt.ylabel('Demand (Count)')
        plt.title('Price After Discount vs Demand')
        
        plt.tight_layout()
        plt.savefig('/workspace/discount_analysis_plots.png', dpi=300, bbox_inches='tight')
        plt.show()
    
    def generate_report(self, model_results):
        """Generate a comprehensive analysis report"""
        report = f"""
=== PARCEL DEMAND ANALYSIS REPORT ===

1. DATASET OVERVIEW:
   - Total observations: {len(self.data)}
   - Date range: {self.data['Date'].min()} to {self.data['Date'].max()}
   - Parcel types: {', '.join(self.data['Parcel_Type'].unique())}

2. PRICE ANALYSIS:
   - Average unit price: {self.data['Unit_Price'].mean():.2f}
   - Price range: {self.data['Unit_Price'].min():.2f} - {self.data['Unit_Price'].max():.2f}
   - Average discount: {self.data['Discount'].mean():.1f}%

3. DEMAND ANALYSIS:
   - Total demand: {self.data['Count'].sum():,}
   - Average daily demand: {self.data['Count'].mean():.1f}
   - Demand range: {self.data['Count'].min()} - {self.data['Count'].max()}

4. DEMAND MODEL ESTIMATION:
   Estimated Demand Function: D(p) = {model_results['intercept']:.2f} - {-model_results['slope']:.4f}*p
   
   - Intercept (a): {model_results['intercept']:.4f}
     (Maximum theoretical demand when price = 0)
   
   - Price Coefficient (b): {-model_results['slope']:.4f}
     (Demand decrease per unit price increase)
   
   - Model fit (R²): {model_results['r2']:.4f}
     ({'Good' if model_results['r2'] > 0.7 else 'Moderate' if model_results['r2'] > 0.5 else 'Weak'} explanatory power)

5. BUSINESS INSIGHTS:
   - Price elasticity of demand: {model_results['slope']:.4f}
   - For every 1 unit increase in price, demand decreases by {-model_results['slope']:.2f} units
   - The model explains {model_results['r2']*100:.1f}% of demand variation

6. RECOMMENDATIONS:
   Based on the analysis, {'consider' if model_results['r2'] > 0.5 else 'carefully evaluate'} pricing strategies that account for the estimated price sensitivity.
        """
        
        print(report)
        
        # Save report to file
        with open('/workspace/demand_analysis_report.txt', 'w', encoding='utf-8') as f:
            f.write(report)
        
        return report

def main():
    """Main function to run the complete analysis"""
    # Sample data based on the provided example
    sample_data = {
        'Date': ['1404/03/03'] * 5,
        'Parcel_Type': ['ميني پک'] * 5,
        'Discount': [0.0, 15.0, 17.0, 18.0, 19.0],
        'Count': [238, 4, 100, 4, 32],
        'Service_Price': [772320.168067, 709400.000000, 736402.800000, 724400.000000, 715025.000000]
    }
    
    # Create DataFrame
    df = pd.DataFrame(sample_data)
    
    print("Starting Parcel Demand Analysis...")
    print("=" * 50)
    
    # Initialize analysis
    analysis = ParcelDemandAnalysis(df)
    
    # Run complete analysis
    analysis.explore_data()
    daily_data = analysis.analyze_price_changes()
    correlations = analysis.analyze_demand_price_relationship()
    model_results = analysis.estimate_demand_model()
    analysis.create_visualizations(model_results)
    analysis.generate_report(model_results)
    
    print("\nAnalysis completed! Check the generated plots and report files.")
    
    return analysis, model_results

if __name__ == "__main__":
    analysis, results = main()