import requests
from wb_parser.models import Product

def parse_and_save_products(query: str, limit: int = 10) -> dict:
    """parser for wb, using v13 search-queries"""
    # Указание местоположения (dest) обязательное, поставил свое
    url = f"https://search.wb.ru/exactmatch/ru/common/v13/search?query={query}&resultset=catalog&limit={limit}&dest=-1257786"
    response = requests.get(url)
    data = response.json()

    products = data.get("data", {}).get("products", [])

    created = 0
    updated = 0
    for item in products:
        product_id = item.get("id")
        if not product_id:
            continue

        sizes = item.get("sizes", [])
        if not sizes or not sizes[0].get("price"):
            continue

        price_info = sizes[0]["price"]
        price = price_info.get("basic", 0) / 100
        discounted_price = price_info.get("product", 0) / 100

        _, was_created = Product.objects.update_or_create(
            product_id=product_id,
            defaults={
                "name": item.get("name"),
                "price": price,
                "discounted_price": discounted_price,
                "rating": item.get("reviewRating"),
                "review_count": item.get("feedbacks"),
            }
        )
        if was_created:
            created += 1
        else:
            updated += 1

    return {"created": created, "updated": updated}
