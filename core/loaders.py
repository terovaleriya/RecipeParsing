import asyncio
import json
from typing import List

from core.domain import *
from core.get_db_credentials import get_credentials
from core.model import db

from recipe_parser.recipe import Recipe
from download_products.product import Product


async def recipe_to_db(recipe: Recipe):
    recipe_id = await create_recipe_by_title(recipe.title)

    ingredients = recipe.ingredients
    if ingredients:
        for ingredient in ingredients:
            ingredient_id = await create_ingredient_by_raw_string(ingredient.get("item"))
            await create_link_recipe_ingredient(recipe_id, ingredient_id)

    tags = recipe.tags
    if tags:
        for tag in tags:
            tag_id = await create_tag_by_tag(tag.get("tag"))
            await create_link_recipe_tag(recipe_id, tag_id)

    instructions = recipe.instructions
    if instructions:
        for instruction in instructions:
            instruction_id = await create_instruction_by_instruction(instruction.get("step"))
            await create_link_recipe_instruction(recipe_id, instruction_id)

    image_id = await create_image_by_image_url(recipe.image_url)
    await create_link_recipe_image(recipe_id, image_id)

    planning = recipe.planning
    if planning:
        planning_id = await create_planning_by_planning(planning.get("prep_time"), planning.get("cook_time"),
                                                        planning.get("total_time"), planning.get("serves"))
        await create_link_recipe_planning(recipe_id, planning_id)

    nutrition = recipe.nutrition
    if nutrition:
        nutrition_id = await create_nutrition_by_nutrition(nutrition.get("Energy"), nutrition.get("Fat"),
                                                           nutrition.get("Saturated Fat"),
                                                           nutrition.get("Carbohydrate"),
                                                           nutrition.get("Sugars"), nutrition.get("Protein"),
                                                           nutrition.get("Salt"), nutrition.get("Fibre"))

        await create_link_recipe_nutrition(recipe_id, nutrition_id)


async def load_unchecked_products(ingredient_id: int, id_list: List[int]):
    for id in id_list:
        await create_link_unchecked_ingredients_products(ingredient_id, id)


async def load_matched_product(ingredient_id: int, product_id: int):
    await create_link_matched_ingredients_products(ingredient_id, product_id)


async def product_to_db(product: Product):
    product_id = await create_product(product.name, product.size, product.price, product.image_url)

    await create_link_product_string_ids_matching(product_id, product.str_id)


async def main():
    credentials = get_credentials()
    await db.set_bind(credentials)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
