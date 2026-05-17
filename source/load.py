from pathlib import Path
import os

import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.engine import URL


PROCESSED_PATH = Path("data/processed")


def get_database_engine():
    """
    Create a PostgreSQL database connection using environment variables.
    This version safely handles special characters in the password.
    """
    load_dotenv()

    connection_url = URL.create(
        drivername="postgresql+psycopg2",
        username=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        database=os.getenv("DB_NAME"),
    )

    engine = create_engine(connection_url)

    return engine


def load_csv_to_postgres(filename: str, table_name: str, engine) -> None:
    """
    Load one processed CSV file into a PostgreSQL table.
    """
    file_path = PROCESSED_PATH / filename

    if not file_path.exists():
        raise FileNotFoundError(f"Missing processed file: {file_path}")

    df = pd.read_csv(file_path)

    df.to_sql(
        name=table_name,
        con=engine,
        if_exists="replace",
        index=False
    )

    print(f"Loaded {filename} into table '{table_name}' | rows: {len(df)}")


def load_all() -> None:
    """
    Load all processed CSV files into PostgreSQL.
    """
    engine = get_database_engine()

    tables = {
        "dim_customers.csv": "dim_customers",
        "dim_products.csv": "dim_products",
        "fact_orders.csv": "fact_orders",
        "fact_order_items.csv": "fact_order_items",
    }

    for filename, table_name in tables.items():
        load_csv_to_postgres(filename, table_name, engine)

    print("All tables loaded into PostgreSQL successfully.")


if __name__ == "__main__":
    load_all()
