# Parcel Demand Analysis Tools

This repository contains tools to analyze the relationship between parcel service pricing and customer demand, helping you estimate the demand function **D(p) = a - b*p**.

## 🎯 What You Get

- **Demand Function Estimation**: Calculate the coefficients `a` and `b` in D(p) = a - b*p
- **Price-Demand Correlation Analysis**: Measure how strongly price affects demand
- **Price Elasticity Calculation**: Understand customer price sensitivity
- **Time-based Price Impact Analysis**: See how demand changed when you increased prices
- **Statistical Validation**: R-squared, correlation coefficients, and model fit assessment

## 📋 Analysis Results Summary

Based on your sample data:

### **Estimated Demand Function**: `D(p) = 135 - 0.0008*p`

- **Strong negative correlation (-0.709)** ✅ Price increases reduce demand  
- **Moderate model fit (50.3% R²)** - Price explains half of demand variation
- **Inelastic demand (-0.786 elasticity)** - Customers are moderately price-sensitive
- **Revenue optimization opportunity** - Small price increases may boost revenue

## 🚀 Quick Start

### Option 1: Use Your CSV Data (Recommended)
```bash
# Put your data in CSV format (see data_template.csv for example)
python3 analyze_your_data.py your_data.csv
```

### Option 2: Use Sample Data
```bash
# Run analysis on provided sample data
python3 simple_analysis.py
```

## 📊 File Description

| File | Description | Use Case |
|------|-------------|----------|
| `analyze_your_data.py` | **Main analysis tool** | Use this with your complete dataset |
| `simple_analysis.py` | Basic analysis with sample data | Quick demo or small datasets |
| `data_template.csv` | CSV format template | Template for your data format |
| `Parcel_Demand_Analysis_Report.md` | Detailed analysis report | Full results interpretation |
| `parcel_demand_analysis.py` | Advanced analysis (needs packages) | Full-featured analysis with plots |

## 📁 Data Format

Your CSV file should have these columns:

```csv
Date,Parcel_Type,Discount,Count,Service_Price
1404/03/03,ميني پک,0.0,238,772320.168067
1404/03/03,ميني پک,15.0,4,709400.000000
1404/03/04,استاندارد,10.0,150,500000.000000
```

### Column Definitions:
- **Date**: Persian date (YYYY/MM/DD format)
- **Parcel_Type**: Type of parcel service (ميني پک, استاندارد, etc.)
- **Discount**: Discount percentage offered (0-100)
- **Count**: Number of parcels (demand)
- **Service_Price**: Total revenue for this service

## 🔍 Understanding Your Results

### Correlation Analysis
- **-0.7 to -1.0**: Strong negative relationship (ideal for pricing analysis)
- **-0.4 to -0.7**: Moderate relationship (good for insights)
- **-0.1 to -0.4**: Weak relationship (collect more data)

### R-squared (Model Fit)
- **>70%**: Excellent - price strongly predicts demand
- **40-70%**: Good - price is important factor
- **<40%**: Moderate - other factors may be more important

### Price Elasticity
- **>1**: Elastic demand (very price-sensitive)
- **<1**: Inelastic demand (less price-sensitive)

## 💡 Business Insights from Your Data

### ✅ **Confirmed:**
1. **Price increases DO reduce demand** (correlation: -0.709)
2. **Linear model reasonably fits your data** (R²: 50.3%)
3. **Customers are moderately price-sensitive** (elasticity: -0.786)

### 📈 **Strategic Recommendations:**
1. **Revenue Optimization**: With inelastic demand, 5-10% price increases may boost revenue
2. **Market Position**: Lower price sensitivity suggests customers value your service
3. **Data Enhancement**: Expand dataset for more robust analysis

## 🔧 Technical Requirements

- **Python 3.x** (built-in libraries only for basic analysis)
- **Optional**: pandas, matplotlib, seaborn (for advanced analysis)

## 📈 Next Steps

1. **Expand Your Dataset**: Include more dates and observations
2. **Test Price Changes**: Use the model to predict demand at different price points
3. **Monitor Results**: Track actual vs predicted demand when you change prices
4. **Segment Analysis**: Analyze different parcel types or customer segments separately

## 🤔 Troubleshooting

### Common Issues:

**"Weak correlation detected"**
- Collect more data points
- Check for data quality issues
- Consider seasonal factors or other variables

**"Low R-squared"**
- Price may not be the primary demand driver
- Include other factors (competition, marketing, seasonality)
- Check for non-linear relationships

**"File not found error"**
- Ensure CSV file is in the same directory
- Check file name spelling
- Verify CSV format matches template

## 📞 Support

For questions about the analysis or extending the tools:

1. Check the detailed report: `Parcel_Demand_Analysis_Report.md`
2. Review the sample data format: `data_template.csv`
3. Run the simple analysis first: `python3 simple_analysis.py`

---

**Happy analyzing! 📊🚚**
