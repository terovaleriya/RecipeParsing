import asyncio
import json
import os

from core.domain import *
from core.get_db_credentials import get_credentials
from core.loaders import recipe_to_db
from core.model import db
from recipe_parser.recipe import Recipe


async def recipe_test(delete: bool = True):
    title_1 = "That's my recipe"
    id_1 = await create_recipe_by_title(title_1)
    id_2 = await create_recipe_by_title(title_1)
    assert (id_1 == id_2)
    id = await get_recipe_id_by_title(title_1)
    assert (id == id_1)
    recipe_1 = await retrieve_recipe_by_id(id)
    assert (recipe_1.title == title_1)
    title_2 = "That's someone else's recipe"

    await update_recipe_by_id(id, title_2)
    recipe_2 = await retrieve_recipe_by_id(id)
    assert (recipe_2.title == title_2)
    if not delete:
        return id
    result = await delete_recipe_by_id(id)
    assert (result is None)
    assert (await retrieve_recipe_by_id(id) is None)


async def ingredient_test(delete: bool = True):
    raw_string = "I'm a raw string"
    name = "Coconut"
    quantity = "Many"
    comment_1 = "Yummy"
    id_1 = await create_ingredient_by_raw_string(raw_string, name, quantity, comment_1)
    id_2 = await create_ingredient_by_raw_string(raw_string, name, quantity, comment_1)
    assert (id_1 == id_2)
    id = await get_ingredient_id_by_raw_string(raw_string)
    assert (id == id_1)
    ingredient_1 = await retrieve_ingredient_by_id(id)
    assert (ingredient_1.raw_string == raw_string)
    comment_2 = "Phi"
    await update_ingredient_by_id(id, comment=comment_2)
    ingredient_2 = await retrieve_ingredient_by_id(id)
    assert (ingredient_2.raw_string == raw_string)
    assert (ingredient_2.name == name)
    assert (ingredient_2.quantity == quantity)
    assert (ingredient_2.comment == comment_2)
    if not delete:
        return id
    result = await delete_ingredient_by_id(id)
    assert (result is None)
    assert (await retrieve_ingredient_by_id(id) is None)


async def tag_test(delete: bool = True):
    tag = "I'm the coolest tag"
    id_1 = await create_tag_by_tag(tag)
    id_2 = await create_tag_by_tag(tag)
    assert (id_1 == id_2)
    id = await get_tag_id_by_tag(tag)
    assert (id == id_1)
    tag_ = await retrieve_tag_by_id(id)
    assert (tag_.tag == tag)
    if not delete:
        return id
    result = await delete_tag_by_id(id)
    assert (result is None)
    assert (await retrieve_tag_by_id(id) is None)


async def instruction_test(delete: bool = True):
    instruction = "Do this"
    id_1 = await create_instruction_by_instruction(instruction)
    id_2 = await create_instruction_by_instruction(instruction)
    assert (id_1 == id_2)
    id = await get_instruction_by_instruction(instruction)
    assert (id == id_1)
    instruction_ = await retrieve_instruction_by_id(id)
    assert (instruction_.instruction == instruction)
    if not delete:
        return id
    result = await delete_instruction_by_id(id)
    assert (result is None)
    assert (await retrieve_instruction_by_id(id) is None)


async def image_test(delete: bool = True):
    image = "I'm image"
    id_1 = await create_image_by_image_url(image)
    id_2 = await create_image_by_image_url(image)
    assert (id_1 == id_2)
    id = await get_image_id_by_image_url(image)
    assert (id == id_1)
    image_ = await retrieve_image_by_id(id)
    assert (image_.image == image)
    if not delete:
        return id
    result = await delete_image_by_id(id)
    assert (result is None)
    assert (await retrieve_image_by_id(id) is None)


async def planning_test(delete: bool = True):
    prep_time_1 = "it's fast"
    cook_time_1 = "it's long"
    total_time_1 = "forever"
    serves_1 = "1"
    id_1 = await create_planning_by_planning(prep_time_1, cook_time_1, total_time_1, serves_1)
    id_2 = await create_planning_by_planning(prep_time_1, cook_time_1, total_time_1, serves_1)
    assert (id_1 == id_2)
    id = await get_planning_id_by_parameters(prep_time_1, cook_time_1, total_time_1, serves_1)
    assert (id == id_1)
    planning_1 = await retrieve_planning_by_id(id)
    assert (planning_1.prep_time == prep_time_1)
    assert (planning_1.cook_time == cook_time_1)
    assert (planning_1.total_time == total_time_1)
    assert (planning_1.serves == serves_1)
    prep_time_2 = "it's not fast"
    cook_time_2 = "it's not long"
    total_time_2 = "not forever"
    serves_2 = "2"

    await update_planning_by_id(id, prep_time_2, cook_time_2, total_time_2, serves_2)
    planning_2 = await retrieve_planning_by_id(id)
    assert (planning_2.prep_time == prep_time_2)
    assert (planning_2.cook_time == cook_time_2)
    assert (planning_2.total_time == total_time_2)
    assert (planning_2.serves == serves_2)
    if not delete:
        return id
    result = await delete_planning_by_id(id)
    assert (result is None)
    assert (await retrieve_planning_by_id(id) is None)


async def nutrition_test(delete: bool = True):
    energy_1 = "energy"
    fat_1 = "fat"
    saturated_fat_1 = "saturated_fat"
    carbohydrate_1 = "carbohydrate"
    sugars_1 = "sugars"
    protein_1 = "protein"
    salt_1 = "salt"
    fibre_1 = "fibre"
    id_1 = await create_nutrition_by_nutrition(energy_1, fat_1, saturated_fat_1, carbohydrate_1,
                                               sugars_1, protein_1, salt_1, fibre_1)
    id_2 = await create_nutrition_by_nutrition(energy_1, fat_1, saturated_fat_1, carbohydrate_1,
                                               sugars_1, protein_1, salt_1, fibre_1)
    assert (id_1 == id_2)
    id = await get_nutrition_id_by_parameters(energy_1, fat_1, saturated_fat_1, carbohydrate_1,
                                              sugars_1, protein_1, salt_1, fibre_1)
    assert (id == id_1)
    nutrition_1 = await retrieve_nutrition_by_id(id)
    assert (nutrition_1.energy == energy_1)
    assert (nutrition_1.fat == fat_1)
    assert (nutrition_1.saturated_fat == saturated_fat_1)
    assert (nutrition_1.carbohydrate == carbohydrate_1)
    assert (nutrition_1.sugars == sugars_1)
    assert (nutrition_1.protein == protein_1)
    assert (nutrition_1.salt == salt_1)
    assert (nutrition_1.fibre == fibre_1)
    energy_2 = "not energy"
    fat_2 = "not fat"
    saturated_fat_2 = "not saturated_fat"
    carbohydrate_2 = "not carbohydrate"
    sugars_2 = "not sugars"
    protein_2 = "not protein"
    salt_2 = "not salt"
    fibre_2 = "not fibre"

    await update_nutrition_by_id(id, energy_2, fat_2, saturated_fat_2, carbohydrate_2,
                                 sugars_2, protein_2, salt_2, fibre_2)
    nutrition_2 = await retrieve_nutrition_by_id(id)
    assert (nutrition_2.energy == energy_2)
    assert (nutrition_2.fat == fat_2)
    assert (nutrition_2.saturated_fat == saturated_fat_2)
    assert (nutrition_2.carbohydrate == carbohydrate_2)
    assert (nutrition_2.sugars == sugars_2)
    assert (nutrition_2.protein == protein_2)
    assert (nutrition_2.salt == salt_2)
    assert (nutrition_2.fibre == fibre_2)
    if not delete:
        return id
    result = await delete_nutrition_by_id(id)
    assert (result is None)
    assert (await retrieve_nutrition_by_id(id) is None)


async def pruduct_test(delete: bool = True):
    name_1 = "that's me"
    size_1 = "huge"
    price_1 = "cheap"
    url_1 = "Ima URL"
    id_1 = await create_product(name_1, size_1, price_1, url_1)
    id_2 = await create_product(name_1, size_1, price_1, url_1)
    assert (id_1 == id_2)
    id = await get_product_id_by_parameters(name_1, size_1, price_1, url_1)
    assert (id == id_1)
    product_1 = await retrieve_product_by_id(id)
    assert (product_1.name == name_1)
    assert (product_1.size == size_1)
    assert (product_1.price == price_1)
    assert (product_1.image_url == url_1)
    name_2 = "it's not me :("
    size_2 = "small"
    price_2 = "expensive"
    url_2 = "I'm not URL!"

    await update_product_by_id(id, name_2, size_2, price_2, url_2)
    product_2 = await retrieve_product_by_id(id)
    assert (product_2.name == name_2)
    assert (product_2.size == size_2)
    assert (product_2.price == price_2)
    assert (product_2.image_url == url_2)
    if not delete:
        return id
    result = await delete_product_by_id(id)
    assert (result is None)
    assert (await retrieve_product_by_id(id) is None)


async def main():
    credentials = get_credentials()
    await db.set_bind(credentials)

    await recipe_test()
    await ingredient_test()
    await tag_test()
    await instruction_test()
    await image_test()
    await planning_test()
    await nutrition_test()
    await pruduct_test()
    await db.set_bind(credentials)

    print(await get_unchecked_products_by_ingredient_id(7))

    print(await get_matched_products_by_ingredient_id(7))
    # json_folder = "../recipe_parser/recipes_json/"
    # i = 0
    # for f in os.listdir(json_folder):
    #     if i == 2:
    #         break
    #     f = json_folder + f
    #     with open(f, "r") as file:
    #         json_str = file.readline()
    #         obj = json.loads(json_str)
    #         recipe = Recipe(**obj)
    #         await recipe_to_db(recipe)
    #     i += 1
    #
    # await delete_recipe_by_id(4)
    # await delete_recipe_by_id(6)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
