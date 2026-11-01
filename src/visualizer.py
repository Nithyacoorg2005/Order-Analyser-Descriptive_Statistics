import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

sns.set_theme(style="whitegrid", palette="muted")

class DescriptiveVisualizer:
    """Generates and saves visual representations of descriptive statistics."""

    @staticmethod
    def _ensure_dir(save_path: str):
        """Creates the output directory if it doesn't exist."""
        if save_path:
            os.makedirs(os.path.dirname(save_path), exist_ok=True)

    @staticmethod
    def plot_distribution(df: pd.DataFrame, value_col: str = 'Order_Value', save_path: str = None):
        """
        Plots a histogram with a Kernel Density Estimate (KDE) curve 
        to show the shape and central tendency of the data.
        """
        plt.figure(figsize=(10, 6))
        sns.histplot(df[value_col], kde=True, bins=20, color="blue")
        
        plt.title(f"Distribution of {value_col.replace('_', ' ')}", fontsize=14, pad=15)
        plt.xlabel("Value ($)", fontsize=12)
        plt.ylabel("Frequency (Number of Orders)", fontsize=12)
        
        if save_path:
            DescriptiveVisualizer._ensure_dir(save_path)
            plt.savefig(save_path, bbox_inches="tight")
            print(f"Saved distribution plot to {save_path}")
        else:
            plt.show()
        plt.close()

    @staticmethod
    def plot_outliers_box(df: pd.DataFrame, value_col: str = 'Order_Value', save_path: str = None):
        """
        Plots a box plot to visually isolate extreme outliers and show the IQR.
        """
        plt.figure(figsize=(10, 4))
        sns.boxplot(x=df[value_col], color="coral")
        
        plt.title(f"Box Plot: Isolating Outliers in {value_col.replace('_', ' ')}", fontsize=14, pad=15)
        plt.xlabel("Value ($)", fontsize=12)
        
        if save_path:
            DescriptiveVisualizer._ensure_dir(save_path)
            plt.savefig(save_path, bbox_inches="tight")
            print(f"Saved box plot to {save_path}")
        else:
            plt.show()
        plt.close()

    @staticmethod
    def plot_category_revenue(df: pd.DataFrame, cat_col: str = 'Category', value_col: str = 'Order_Value', save_path: str = None):
        """
        Plots a bar chart comparing total revenue across different categories.
        """
        # Calculate revenue first
        category_revenue = df.groupby(cat_col)[value_col].sum().reset_index()
        category_revenue = category_revenue.sort_values(by=value_col, ascending=False)

        plt.figure(figsize=(10, 6))
        sns.barplot(data=category_revenue, x=cat_col, y=value_col, hue=cat_col, palette="viridis", legend=False)
        
        plt.title("Total Revenue by Category", fontsize=14, pad=15)
        plt.xlabel("Product Category", fontsize=12)
        plt.ylabel("Total Revenue ($)", fontsize=12)
        
        if save_path:
            DescriptiveVisualizer._ensure_dir(save_path)
            plt.savefig(save_path, bbox_inches="tight")
            print(f"Saved category bar chart to {save_path}")
        else:
            plt.show()
        plt.close()

if __name__ == "__main__":
   
    data = {
        'OrderID': [101, 102, 103, 104, 105, 106, 107, 108, 109, 110],
        'Category': ['Apparel', 'Electronics', 'Apparel', 'Home', 'Electronics', 
                     'Apparel', 'Home', 'Electronics', 'Electronics', 'Home'],
       
        'Order_Value': [25, 1200, 30, 45, 850, 22, 60, 4500, 3200, 55] 
    }
    df = pd.DataFrame(data)

    
    OUTPUT_DIR = "./outputs/charts"

   
    print("Generating visual reports...")
    DescriptiveVisualizer.plot_distribution(df, save_path=f"{OUTPUT_DIR}/distribution.png")
    DescriptiveVisualizer.plot_outliers_box(df, save_path=f"{OUTPUT_DIR}/outliers_box.png")
    DescriptiveVisualizer.plot_category_revenue(df, save_path=f"{OUTPUT_DIR}/category_revenue.png")