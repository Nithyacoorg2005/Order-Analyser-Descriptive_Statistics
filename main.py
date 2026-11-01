import yaml
import os
import logging
from datetime import datetime

from src.data_loader import OrderDataLoader
from src.calculator import DescriptiveCalculator
from src.visualizer import DescriptiveVisualizer

def load_config(config_path="config.yaml"):
    """Loads the YAML configuration file."""
    with open(config_path, "r") as file:
        return yaml.safe_load(file)

def setup_logging(config):
    """Configures the logger based on the YAML settings."""
    log_dir = config['directories']['logs']
    os.makedirs(log_dir, exist_ok=True)
    
    logging.basicConfig(
        level=getattr(logging, config['logging']['level'].upper()),
        format=config['logging']['format'],
        force=True,  # <--- ADD THIS LINE to override Matplotlib's logger
        handlers=[
            logging.FileHandler(os.path.join(log_dir, config['logging']['filename'])),
            logging.StreamHandler() 
        ]
    )
def generate_markdown_report(summary_stats, cat_breakdown, vip_tiers, report_path):
    """Compiles the descriptive statistics into a readable markdown report."""
    today = datetime.now().strftime("%Y-%m-%d")
    
    # Opening the multi-line f-string with exactly 3 quotes
    report_content =f"""# Daily E-Commerce Health Report ({today})



## 1. Executive Summary
* **Total Revenue:** ${summary_stats['Total_Revenue']:,.2f}
* **Total Orders:** {summary_stats['Total_Orders']}
* **Average Order Value (Mean):** ${summary_stats['Mean_Order_Value']:,.2f}
* **Typical Order Value (Median):** ${summary_stats['Median_Order_Value']:,.2f}

## 2. Customer VIP Tiers (Percentiles)
* **Top 50% spend over:** ${vip_tiers.get('P50', 0):,.2f}
* **Top 25% spend over:** ${vip_tiers.get('P75', 0):,.2f}
* **Top 10% (VIP) spend over:** ${vip_tiers.get('P90', 0):,.2f}
* **Top 1% (Whales) spend over:** ${vip_tiers.get('P99', 0):,.2f}

## 3. Category Performance

{cat_breakdown.to_string(index=False)}
"""
def run_pipeline():
    # 1. Initialization
    config = load_config()
    setup_logging(config)
    logging.info("Starting the Descriptive Orders Analyzer pipeline...")

    # Extract configuration variables
    raw_dir = config['directories']['raw_data']
    charts_dir = config['directories']['charts']
    reports_dir = config['directories']['reports']
    schema = config['data_schema']
    vip_percentiles = config['analysis']['vip_percentiles']

    # 2. Ingestion
    loader = OrderDataLoader(raw_data_dir=raw_dir)
    try:
        df = loader.load_from_csv(filename="daily_orders.csv", date_columns=schema['date_columns'])
    except Exception as e:
        logging.error("Pipeline aborted due to data loading failure.")
        return

    # 3. Calculation (Descriptive Statistics)
    logging.info("Calculating descriptive statistics...")
    summary = DescriptiveCalculator.get_executive_summary(df, value_col=schema['value_column'])
    category_data = DescriptiveCalculator.get_category_breakdown(
        df, cat_col=schema['category_column'], value_col=schema['value_column']
    )
    vip_tiers = DescriptiveCalculator.get_percentile_thresholds(
        df, value_col=schema['value_column'], percentiles=vip_percentiles
    )

    # 4. Visualization
    logging.info("Generating visual assets...")
    DescriptiveVisualizer.plot_distribution(
        df, value_col=schema['value_column'], save_path=f"{charts_dir}/distribution.png"
    )
    DescriptiveVisualizer.plot_outliers_box(
        df, value_col=schema['value_column'], save_path=f"{charts_dir}/outliers_box.png"
    )
    DescriptiveVisualizer.plot_category_revenue(
        df, cat_col=schema['category_column'], value_col=schema['value_column'], save_path=f"{charts_dir}/category_revenue.png"
    )

    # 5. Reporting
    report_filename = f"{reports_dir}/health_report_{datetime.now().strftime('%Y%m%d')}.md"
    generate_markdown_report(summary, category_data, vip_tiers, report_filename)
    
    logging.info("Pipeline completed successfully.")

if __name__ == "__main__":
    print("Initializing pipeline...") 
    
    # Create dummy data for testing if the raw folder is empty
    os.makedirs("./data/raw", exist_ok=True)
    dummy_csv = "./data/raw/daily_orders.csv"
    if not os.path.exists(dummy_csv):
        with open(dummy_csv, "w") as f:
            f.write("OrderID,Order_Date,Category,Order_Value\n")
            f.write("101,2026-11-01,Apparel,45.50\n")
            f.write("102,2026-11-01,Electronics,1200.00\n")
            f.write("103,2026-11-01,Apparel,22.00\n")
            f.write("104,2026-11-01,Home,150.00\n")
            f.write("105,2026-11-01,Electronics,850.00\n")
    
    # This is the line that actually forces the script to run
    run_pipeline()
    print("Pipeline execution finished! Check the outputs/ folder.")