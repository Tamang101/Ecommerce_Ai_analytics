from pathlib import Path
import json
import pandas as pd


RAW_API_PATH = Path("data/raw/api")
PROCESSED_PATH = Path("data/processed")
PROCESSED_PATH.mkdir(parents=True, exist_ok=True)

def load_json(filename: str) -> list:
    """
    Load raw JSON data from the raw API folder.
    """
    file_path = RAW_API_PATH / filename

    with open(file_path, "r", encoding="utf-8") as file:
        data = json.load(file)

    return data


def transform_customers(users: list) -> pd.DataFrame:
    """
    Transform users API data into a clean customer dimension table.
    """
    customer_rows = []

    for user in users:
        customer_rows.append({
            "customer_id": user.get("id"),
            "first_name": user.get("firstName"),
            "last_name": user.get("lastName"),
            "email": user.get("email"),
            "phone": user.get("phone"),
            "age": user.get("age"),
            "gender": user.get("gender"),
            "city": user.get("address", {}).get("city"),
            "state": user.get("address", {}).get("state"),
            "country": user.get("address", {}).get("country"),
            "company": user.get("company", {}).get("name"),
            "job_title": user.get("company", {}).get("title"),
        })

    customers_df = pd.DataFrame(customer_rows)
    customers_df = customers_df.drop_duplicates(subset=["customer_id"])

    return customers_df


def transform_products(products: list) -> pd.DataFrame:
    """
    Transform products API data into a clean product dimension table.
    """
    product_rows = []

    for product in products:
        product_rows.append({
            "product_id": product.get("id"),
            "product_name": product.get("title"),
            "category": product.get("category"),
            "brand": product.get("brand"),
            "price": product.get("price"),
            "discount_percentage": product.get("discountPercentage"),
            "rating": product.get("rating"),
            "stock": product.get("stock"),
            "availability_status": product.get("availabilityStatus"),
            "warranty_information": product.get("warrantyInformation"),
            "shipping_information": product.get("shippingInformation"),
        })

    products_df = pd.DataFrame(product_rows)
    products_df = products_df.drop_duplicates(subset=["product_id"])

    return products_df


def transform_orders(carts: list) -> pd.DataFrame:
    """
    Transform carts API data into an order fact table.
    Each cart is treated as one order.
    """
    order_rows = []

    for cart in carts:
        order_rows.append({
            "order_id": cart.get("id"),
            "customer_id": cart.get("userId"),
            "total_products": cart.get("totalProducts"),
            "total_quantity": cart.get("totalQuantity"),
            "total_amount": cart.get("total"),
            "discounted_total": cart.get("discountedTotal"),
        })

    orders_df = pd.DataFrame(order_rows)
    orders_df = orders_df.drop_duplicates(subset=["order_id"])

    return orders_df


def transform_order_items(carts: list) -> pd.DataFrame:
    """
    Transform nested cart products into an order items fact table.
    """
    item_rows = []

    for cart in carts:
        order_id = cart.get("id")
        customer_id = cart.get("userId")

        for product in cart.get("products", []):
            item_rows.append({
                "order_id": order_id,
                "customer_id": customer_id,
                "product_id": product.get("id"),
                "product_name": product.get("title"),
                "quantity": product.get("quantity"),
                "unit_price": product.get("price"),
                "total_amount": product.get("total"),
                "discount_percentage": product.get("discountPercentage"),
                "discounted_total": product.get("discountedTotal"),
            })

    order_items_df = pd.DataFrame(item_rows)

    return order_items_df


def save_processed_data(df: pd.DataFrame, filename: str) -> None:
    """
    Save transformed DataFrame as CSV.
    """
    output_path = PROCESSED_PATH / filename
    df.to_csv(output_path, index=False)
    print(f"Saved processed file: {output_path} | rows: {len(df)}")


def transform_all() -> None:
    """
    Full transformation pipeline.
    """
    products = load_json("products.json")
    users = load_json("users.json")
    carts = load_json("carts.json")

    customers_df = transform_customers(users)
    products_df = transform_products(products)
    orders_df = transform_orders(carts)
    order_items_df = transform_order_items(carts)

    save_processed_data(customers_df, "dim_customers.csv")
    save_processed_data(products_df, "dim_products.csv")
    save_processed_data(orders_df, "fact_orders.csv")
    save_processed_data(order_items_df, "fact_order_items.csv")

    print("Transformation completed successfully.")


if __name__ == "__main__":
    transform_all()
