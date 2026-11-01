import pandas as pd
import os
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class OrderDataLoader:
    """Handles the ingestion of raw order data from various sources."""
    
    def __init__(self, raw_data_dir: str):
        self.raw_data_dir = raw_data_dir

    def load_from_csv(self, filename: str, date_columns: list = None) -> pd.DataFrame:
        """
        Loads raw data from a CSV file into a pandas DataFrame.
        
        Args:
            filename (str): The name of the file (e.g., 'orders_export.csv').
            date_columns (list): List of column names to parse as datetime objects.
            
        Returns:
            pd.DataFrame: The loaded raw data.
        """
        filepath = os.path.join(self.raw_data_dir, filename)
        
        if not os.path.exists(filepath):
            logging.error(f"File not found: {filepath}")
            raise FileNotFoundError(f"Cannot locate the raw data file at {filepath}")
            
        try:
        
            logging.info(f"Ingesting raw data from {filename}...")
            df = pd.read_csv(filepath, parse_dates=date_columns)
            
        
            logging.info(f"Successfully loaded {len(df)} rows and {len(df.columns)} columns.")
            return df
            
        except pd.errors.EmptyDataError:
            logging.error(f"The file {filename} is completely empty.")
            raise
        except Exception as e:
            logging.error(f"An unexpected error occurred during ingestion: {e}")
            raise

    def load_from_sql(self, query: str, connection_string: str) -> pd.DataFrame:
        """
        Placeholder method: Demonstrates how the loader can be expanded
        to pull live data directly from a PostgreSQL or MySQL database.
        """
    
        pass


if __name__ == "__main__":

    RAW_DATA_PATH = "./restaurant_orders.csv"
    

    loader = OrderDataLoader(raw_data_dir=RAW_DATA_PATH)
    
    os.makedirs(RAW_DATA_PATH, exist_ok=True)
    dummy_filepath = os.path.join(RAW_DATA_PATH, "restaurants_orders.csv")
    with open(dummy_filepath, "w") as f:
        f.write("OrderID,Order_Date,Category,Order_Value\n")
        f.write("101,2026-11-01,Apparel,45.50\n")
        f.write("102,2026-11-01,Electronics,1200.00\n")
    
    try:
        raw_orders_df = loader.load_from_csv(
            filename="daily_orders.csv", 
            date_columns=["Order_Date"]
        )
        
        print("\nRaw Data Preview:")
        print(raw_orders_df.head())
        print("\nData Types:")
        print(raw_orders_df.dtypes)
        
    except Exception as e:
        print("Ingestion failed. Halting analysis.")