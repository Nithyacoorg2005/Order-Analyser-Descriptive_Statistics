import pandas as pd
import numpy as np

class DescriptiveCalculator:
    """
    Calculates core descriptive statistics for e-commerce datasets.
    Methods are static so they can be called directly without instantiating the class.
    """

    @staticmethod
    def get_executive_summary(df: pd.DataFrame, value_col: str = 'Order_Value') -> dict:
        """
        Calculates central tendency and overall health metrics.
        """
        if df.empty:
            return {}

        return {
            'Total_Orders': len(df),
            'Total_Revenue': round(df[value_col].sum(), 2),
            'Mean_Order_Value': round(df[value_col].mean(), 2),
            'Median_Order_Value': round(df[value_col].median(), 2),
            'Std_Deviation': round(df[value_col].std(), 2),
            'Min_Order': round(df[value_col].min(), 2),
            'Max_Order': round(df[value_col].max(), 2)
        }

    @staticmethod
    def get_category_breakdown(df: pd.DataFrame, cat_col: str = 'Category', value_col: str = 'Order_Value') -> pd.DataFrame:
        """
        Groups data to summarize frequency and performance across different segments.
        """
        breakdown = df.groupby(cat_col).agg(
            Total_Orders=(value_col, 'count'),
            Revenue=(value_col, 'sum'),
            Mean_Order_Value=(value_col, 'mean')
        ).reset_index()
        
        # Sort by revenue descending to highlight top-performing categories
        return breakdown.sort_values(by='Revenue', ascending=False).round(2)

    @staticmethod
    def get_percentile_thresholds(df: pd.DataFrame, value_col: str = 'Order_Value', percentiles: list = [50, 75, 90, 99]) -> dict:
        """
        Calculates positional metrics to identify high-value customer tiers (e.g., VIPs).
        """
        # Drop NaNs to prevent calculation errors on missing data
        clean_series = df[value_col].dropna()
        calc_values = np.percentile(clean_series, percentiles)
        
        return {f"P{p}": round(val, 2) for p, val in zip(percentiles, calc_values)}

    @staticmethod
    def get_outliers_iqr(df: pd.DataFrame, value_col: str = 'Order_Value') -> pd.DataFrame:
        """
        Isolates extreme outliers using the Interquartile Range (IQR) method.
        This is the mathematical equivalent of finding dots outside a Box Plot's whiskers.
        """
        Q1 = df[value_col].quantile(0.25)
        Q3 = df[value_col].quantile(0.75)
        IQR = Q3 - Q1
        
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        
        outliers = df[(df[value_col] < lower_bound) | (df[value_col] > upper_bound)]
        return outliers

# ==========================================
# Execution Example
# ==========================================
if __name__ == "__main__":
    # 1. Create dummy data (representing output from data_loader.py)
    data = {
        'OrderID': [101, 102, 103, 104, 105, 106, 107, 108],
        'Category': ['Apparel', 'Electronics', 'Apparel', 'Home', 'Electronics', 'Apparel', 'Home', 'Electronics'],
        'Order_Value': [25, 1200, 30, 45, 850, 22, 60, 4500] # 4500 is a deliberate outlier
    }
    df = pd.DataFrame(data)

    # 2. Run the calculations
    print("--- EXECUTIVE SUMMARY ---")
    summary = DescriptiveCalculator.get_executive_summary(df)
    for key, val in summary.items():
        print(f"{key}: {val}")

    print("\n--- CATEGORY BREAKDOWN ---")
    print(DescriptiveCalculator.get_category_breakdown(df).to_string(index=False))

    print("\n--- PERCENTILES (VIP Tiers) ---")
    print(DescriptiveCalculator.get_percentile_thresholds(df))

    print("\n--- DETECTED OUTLIERS ---")
    print(DescriptiveCalculator.get_outliers_iqr(df).to_string(index=False))