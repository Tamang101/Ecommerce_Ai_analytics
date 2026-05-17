from pathlib import Path
import json
import requests


BASE_URL = "https://dummyjson.com"
RAW_API_PATH = Path("data/raw/api")
RAW_API_PATH.mkdir(parents=True, exist_ok=True)


def fetch_data(resource: str, limit: int = 100) -> list:
    """
    Fetch all available records from a DummyJSON endpoint using pagination.
    Example resources: products, users, carts
    """
    all_items = []
    skip = 0

    while True:
        url = f"{BASE_URL}/{resource}?limit={limit}&skip={skip}"

        response = requests.get(url, timeout=30)
        response.raise_for_status()

        data = response.json()

        items = data.get(resource, [])
        total = data.get("total", 0)

        all_items.extend(items)

        print(f"Fetched {len(all_items)} / {total} records from {resource}")

        skip += limit

        if len(all_items) >= total:
            break

    return all_items


def save_json(data: list, filename: str) -> None:
    """
    Save extracted API data as raw JSON file.
    """
    output_path = RAW_API_PATH / filename

    with open(output_path, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)

    print(f"Saved file: {output_path}")


def extract_all() -> None:
    """
    Extract products, users, and carts from DummyJSON API.
    """
    resources = ["products", "users", "carts"]

    for resource in resources:
        data = fetch_data(resource)
        save_json(data, f"{resource}.json")


if __name__ == "__main__":
    extract_all()
