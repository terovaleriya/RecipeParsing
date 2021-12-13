import asyncio
import json

import os

from core.get_db_credentials import get_credentials
from core.loaders import recipe_to_db
from core.model import db

from recipe_parser.recipe import Recipe


async def main():
    credentials = get_credentials()
    await db.set_bind(credentials)
    json_folder = "../recipe_parser/recipes_json/"
    for f in os.listdir(json_folder):
        f = json_folder + f
        with open(f, "r") as file:
            json_str = file.readline()
            obj = json.loads(json_str)
            recipe = Recipe(**obj)
            await recipe_to_db(recipe)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
