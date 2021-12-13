import asyncio
import json

import os

from core.get_db_credentials import get_credentials
from core.loaders import product_to_db
from core.model import db

from download_products.product import Product


async def main():
    credentials = get_credentials()
    await db.set_bind(credentials)
    file_name = "../download_products/all_products.txt"
    with open(file_name, "r") as file:
        data = json.load(file)
        for item in data:
            product_json = {
                'str_id': item.get('id'),
                'name': item.get('name'),
                'size': item.get('size', None),
                'price': item.get('weights', {}).get('pricePerUomQualifier', None),
                'image_url': item.get('thumbnail', None)
            }
            product = Product(**product_json)
            await product_to_db(product)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
