import logging
from typing import Optional, Any, List

import asyncpg

from core import schema, model

# Links


logging.basicConfig(filename="db_load.log", level=logging.WARNING)


def get_field(table: model) -> (str, str):
    field_a = "recipe"
    field_b = ""
    if table == model.RecipesIngredients:
        field_b = "ingredient"
    elif table == model.RecipesInstructions:
        field_b = "instruction"
    elif table == model.RecipesNutrition:
        field_b = "nutrition"
    elif table == model.RecipesPlanning:
        field_b = "planning"
    elif table == model.RecipesImages:
        field_b = "image"
    elif table == model.RecipesTags:
        field_b = "tag"
    elif table == model.ProductStringIdsMatching:
        field_a = "id"
        field_b = "string_id"
    elif table == model.MatchedIngredientsProducts or table == model.UncheckedIngredientsProducts:
        field_a = "ingredient"
        field_b = "product"

    return field_a, field_b


async def create_link(table: Any, id_a, id_b) -> int:
    field_a, field_b = get_field(table)
    try:
        obj_data = {
            field_a: id_a,
            field_b: id_b
        }
        link = await table.create(**obj_data)
        return link.id
    except asyncpg.exceptions.UniqueViolationError:
        logging.info("Link in %s between %s and %s already exists", str(table), str(id_a), str(id_b))


async def create_link_recipe_ingredient(id_a: int, id_b: int):
    await create_link(model.RecipesIngredients, id_a, id_b)


async def create_link_recipe_instruction(id_a: int, id_b: int):
    await create_link(model.RecipesInstructions, id_a, id_b)


async def create_link_recipe_tag(id_a: int, id_b: int):
    await create_link(model.RecipesTags, id_a, id_b)


async def create_link_recipe_image(id_a: int, id_b: int):
    await create_link(model.RecipesImages, id_a, id_b)


async def create_link_recipe_planning(id_a: int, id_b: int):
    await create_link(model.RecipesPlanning, id_a, id_b)


async def create_link_recipe_nutrition(id_a: int, id_b: int):
    await create_link(model.RecipesNutrition, id_a, id_b)


async def create_link_matched_ingredients_products(id_a: int, id_b: int):
    await create_link(model.MatchedIngredientsProducts, id_a, id_b)


async def create_link_unchecked_ingredients_products(id_a: int, id_b: int):
    await create_link(model.UncheckedIngredientsProducts, id_a, id_b)


async def create_link_product_string_ids_matching(id_a: int, id_b: str):
    await create_link(model.ProductStringIdsMatching, id_a, id_b)


# GETTERS

async def get_unchecked_products_by_ingredient_id(ingredient_id: int) -> List[int]:
    link_list = await model.UncheckedIngredientsProducts.query.where(
        model.UncheckedIngredientsProducts.ingredient == ingredient_id).gino.all()
    return [i.product for i in link_list]


async def get_matched_products_by_ingredient_id(ingredient_id: int) -> List[int]:
    link_list = await model.MatchedIngredientsProducts.query.where(
        model.MatchedIngredientsProducts.ingredient == ingredient_id).gino.all()
    return [i.product for i in link_list]


# PRODUCT

# OK
async def retrieve_product_by_id(product_id: int) -> Optional[schema.Product]:
    obj = await model.Products.get(product_id)
    return obj.as_schema() if obj else None


# OK
async def delete_product_by_id(product_id: int) -> None:
    await model.Products.delete.where(model.Products.id == product_id).gino.status()


# OK
async def create_product(name: str, size: str = None, price: str = None, image_url: str = None) -> int:
    products = model.Products
    try:
        obj_data = {
            "name": name,
            "size": size,
            "price": price,
            "image_url": image_url
        }
        product = await products.create(**obj_data)
        return product.id

    except asyncpg.exceptions.UniqueViolationError:
        logging.info(
            "Product with [name '%s', size '%s', price %s, image_url '%s'] already exists", name, str(size), str(price),
            str(image_url))
        return await get_product_id_by_parameters(name, size, price, image_url)


# OK
async def update_product_by_id(product_id: int, name: str = None, size: str = None, price: str = None,
                               image_url: str = None) -> Optional[
    int]:
    products = model.Products

    try:
        obj = await products.get(product_id)
        name = name if (name is not None) else obj.name
        size = size if (size is not None) else obj.size
        price = price if (price is not None) else obj.price
        image_url = image_url if (image_url is not None) else obj.image_url
        obj_data = {
            "name": name,
            "size": size,
            "price": price,
            "image_url": image_url
        }
        await obj.update(**obj_data).apply()
    except AttributeError:
        logging.warning("Product with id %s doesn't exist", str(product_id))
    except asyncpg.exceptions.UniqueViolationError:
        logging.error(
            "Product with [name '%s', size '%s', price '%s', image_url '%s'] already exists. "
            "Update by id %s is not completed",
            name,
            str(size), str(price), str(image_url), product_id)
        return await get_product_id_by_parameters(name, size, image_url)


# OK
async def get_product_id_by_parameters(name: str, size: str = None, price: str = None, image_url: str = None) -> int:
    products = model.Products
    return await products.query.where(products.name == name).where(products.size == size). \
        where(products.price == price).where(products.image_url == image_url).gino.scalar()


# RECIPE

# OK
async def retrieve_recipe_by_id(recipe_id: int) -> Optional[schema.Recipe]:
    obj = await model.Recipes.get(recipe_id)
    return obj.as_schema() if obj else None


# OK
async def delete_recipe_by_id(recipe_id: int) -> None:
    await model.Recipes.delete.where(model.Recipes.id == recipe_id).gino.status()


# OK
# (пытается создать, если удалось -- вернет новый id,
# а если такой уже есть, вернет id уже существующего)
async def create_recipe_by_title(title: str) -> int:
    recipes = model.Recipes
    try:
        obj_data = {
            "title": title
        }
        recipe_ = await recipes.create(**obj_data)
        logging.info("RECIPE CREATED")
        return recipe_.id
    except asyncpg.exceptions.UniqueViolationError:
        logging.info("Recipe with title '%s' already exists", title)
        id = await get_recipe_id_by_title(title)
        return id


# ?
async def update_recipe_by_id(recipe_id: int, title: str = None) -> Optional[int]:
    recipes = model.Recipes
    try:
        obj = await recipes.get(recipe_id)
        title = title if (title is not None) else obj.title
        obj_data = {
            "title": title
        }
        await obj.update(**obj_data).apply()
    except AttributeError:
        logging.warning("Recipe with id %s doesn't exist", str(recipe_id))
    except asyncpg.exceptions.UniqueViolationError:
        logging.error("Recipe with title '%s' already exists. Update by id %s is not completed", title, recipe_id)
        id = await get_recipe_id_by_title(title)
        return id


# OK
async def get_recipe_id_by_title(title: str) -> int:
    recipes = model.Recipes
    id = await recipes.query.where(recipes.title == title).gino.scalar()
    return id


# INGREDIENT

# OK
async def retrieve_ingredient_by_id(ingredient_id: int) -> Optional[schema.Ingredient]:
    obj = await model.Ingredients.get(ingredient_id)
    return obj.as_schema() if obj else None


# OK
async def delete_ingredient_by_id(ingredient_id: int) -> None:
    await model.Ingredients.delete.where(model.Ingredients.id == ingredient_id).gino.status()


# OK
async def create_ingredient_by_raw_string(raw_string: str, name: str = None, quantity: str = None,
                                          comment: str = None) -> int:
    ingredients = model.Ingredients
    try:
        obj_data = {
            "name": name,
            "quantity": quantity,
            "comment": comment,
            "raw_string": raw_string
        }
        ingredient_ = await ingredients.create(**obj_data)
        logging.info("INGREDIENT CREATED")
        return ingredient_.id
    except asyncpg.exceptions.UniqueViolationError:
        id = await get_ingredient_id_by_raw_string(raw_string)
        logging.info("Ingredient with raw string '%s' already exists", raw_string)
        return id


# OK
async def update_ingredient_by_id(ingredient_id: int, name: str = None, quantity: str = None,
                                  comment: str = None) -> None:
    ingredients = model.Ingredients

    try:
        obj = await ingredients.get(ingredient_id)
        name = name if (name is not None) else obj.name
        quantity = quantity if (quantity is not None) else obj.quantity
        comment = comment if (comment is not None) else obj.comment
        obj_data = {
            "name": name,
            "quantity": quantity,
            "comment": comment,
        }
        await obj.update(**obj_data).apply()
    except AttributeError:
        logging.warning("Ingredient with id %s doesn't exist", str(ingredient_id))


# OK
async def get_ingredient_id_by_raw_string(raw_string: str) -> int:
    ingredients = model.Ingredients
    id = await ingredients.query.where(ingredients.raw_string == raw_string).gino.scalar()
    return id


# TAG

# OK
async def retrieve_tag_by_id(tag_id: int) -> Optional[schema.Tag]:
    obj = await model.Tags.get(tag_id)
    return obj.as_schema() if obj else None


# OK
async def delete_tag_by_id(tag_id: int) -> None:
    await model.Tags.delete.where(model.Tags.id == tag_id).gino.status()


# OK
async def create_tag_by_tag(tag: str) -> int:
    tags = model.Tags
    id = await get_tag_id_by_tag(tag)
    try:
        obj_data = {
            "tag": tag
        }
        tag_ = await tags.create(**obj_data)
        return tag_.id

    except asyncpg.exceptions.UniqueViolationError:
        id = await get_tag_id_by_tag(tag)
        logging.info("Tag with name '%s' already exists", tag)
        return id


# ?
async def update_tag_by_id(tag_id: int, tag: str = None) -> Optional[int]:
    tags = model.Tags
    try:
        obj = await tags.get(tag_id)
        tag = tag if (tag is not None) else obj.tag
        obj_data = {
            "tag": tag
        }
        await obj.update(**obj_data).apply()
    except AttributeError:
        logging.warning("Tag with id %s doesn't exist", str(tag_id))
    except asyncpg.exceptions.UniqueViolationError:
        id = await get_tag_id_by_tag(tag)
        logging.error("Tag with name '%s' already exists. Update by id %s is not completed", tag, tag_id)
        return id


# OK
async def get_tag_id_by_tag(tag: str) -> int:
    tags = model.Tags
    id = await tags.query.where(tags.tag == tag).gino.scalar()
    return id


# IMAGE URL

# OK
async def retrieve_image_by_id(image_id: int) -> Optional[schema.Image]:
    obj = await model.Images.get(image_id)
    return obj.as_schema() if obj else None


# OK
async def delete_image_by_id(image_id: int) -> None:
    await model.Images.delete.where(model.Images.id == image_id).gino.status()


# OK
async def create_image_by_image_url(image_url: str) -> int:
    images = model.Images
    try:
        obj_data = {
            "image": image_url
        }
        image_ = await images.create(**obj_data)
        return image_.id
    except asyncpg.exceptions.UniqueViolationError:
        id = await get_image_id_by_image_url(image_url)
        logging.info("Image with image URL '%s' already exists", image_url)
        return id


# ?
async def update_image_by_id(image_id: int, image_url: str = None) -> Optional[int]:
    images = model.Images
    try:
        obj = await images.get(image_id)
        image_url = image_url if (image_url is not None) else obj.image
        obj_data = {
            "image": image_url
        }
        await obj.update(**obj_data).apply()
    except AttributeError:
        logging.warning("Image with id %s doesn't exist", str(image_id))
    except asyncpg.exceptions.UniqueViolationError:
        id = await get_image_id_by_image_url(image_url)
        logging.error("Image with image URL '%s' already exists. Update by id %s is not completed", image_url,
                      image_id)
        return id


# OK
async def get_image_id_by_image_url(image_url: str) -> int:
    images = model.Images
    id = await images.query.where(images.image == image_url).gino.scalar()
    return id


# INSTRUCTIONS

# OK
async def retrieve_instruction_by_id(instruction_id: int) -> Optional[schema.Instruction]:
    obj = await model.Instructions.get(instruction_id)
    return obj.as_schema() if obj else None


# OK
async def delete_instruction_by_id(instruction_id: int) -> None:
    await model.Instructions.delete.where(model.Instructions.id == instruction_id).gino.status()


# OK
async def create_instruction_by_instruction(instruction: str) -> int:
    instructions = model.Instructions

    try:
        obj_data = {
            "instruction": instruction
        }
        instruction_ = await instructions.create(**obj_data)
        return instruction_.id
    except asyncpg.exceptions.UniqueViolationError:
        id = await get_instruction_by_instruction(instruction)
        logging.info("Instruction with content '%s' already exists", instruction)
        return id


# ?
async def update_instruction_by_id(instruction_id: int, instruction: str = None) -> Optional[int]:
    instructions = model.Instructions
    try:
        obj = await instructions.get(instruction_id)
        instruction = instruction if (instruction is not None) else obj.instruction
        obj_data = {
            "instruction": instruction
        }
        await obj.update(**obj_data).apply()
    except AttributeError:
        logging.warning("Instruction with id %s doesn't exist", str(instruction_id))
    except asyncpg.exceptions.UniqueViolationError:
        id = await get_instruction_by_instruction(instruction)
        logging.error("Instruction with content '%s' already exists. Update by id %s is not completed", instruction,
                      instruction_id)
        return id


# OK
async def get_instruction_by_instruction(instruction: str) -> int:
    instructions = model.Instructions
    id = await instructions.query.where(instructions.instruction == instruction).gino.scalar()
    return id


# PLANNING
# OK
async def retrieve_planning_by_id(planning_id: int) -> Optional[schema.Plan]:
    obj = await model.Plan.get(planning_id)
    return obj.as_schema() if obj else None


# OK
async def delete_planning_by_id(planning_id: int) -> None:
    await model.Plan.delete.where(model.Plan.id == planning_id).gino.status()


# OK
async def create_planning_by_planning(prep_time: str = None, cook_time: str = None, total_time: str = None,
                                      serves: str = None) -> int:
    planning = model.Plan
    try:
        obj_data = {
            "prep_time": prep_time,
            "cook_time": cook_time,
            "total_time": total_time,
            "serves": serves
        }
        planning_ = await planning.create(**obj_data)
        return planning_.id
    except asyncpg.exceptions.UniqueViolationError:
        id = await get_planning_id_by_parameters(prep_time, cook_time, total_time, serves)
        logging.info(
            "Planning with [prep_time = %s, cook_time = %s, total_time = %s, %s serves] already exists", str(prep_time),
            str(cook_time), str(total_time), str(serves))
        return id


# ?
async def update_planning_by_id(planning_id: int, prep_time: str = None, cook_time: str = None, total_time: str = None,
                                serves: str = None) -> Optional[int]:
    planning = model.Plan
    try:
        obj = await planning.get(planning_id)
        prep_time = prep_time if (prep_time is not None) else obj.prep_time
        cook_time = cook_time if (cook_time is not None) else obj.cook_time
        total_time = total_time if (total_time is not None) else obj.total_time
        serves = serves if (serves is not None) else obj.serves

        obj_data = {
            "prep_time": prep_time,
            "cook_time": cook_time,
            "total_time": total_time,
            "serves": serves
        }

        await obj.update(**obj_data).apply()
    except AttributeError:
        logging.warning("Planning with id %s doesn't exist", str(planning_id))
    except asyncpg.exceptions.UniqueViolationError:
        id = await get_planning_id_by_parameters(prep_time, cook_time, total_time, serves)
        logging.error(
            "Planning with [prep_time = %s, cook_time = %s, total_time = %s, %s serves] already exists. Update by id %s is not completed",
            str(prep_time),
            str(cook_time), str(total_time), str(serves), planning_id)
        return id


# OK
async def get_planning_id_by_parameters(prep_time: str = None, cook_time: str = None, total_time: str = None,
                                        serves: str = None) -> int:
    planning = model.Plan
    id = await planning.query.where(planning.prep_time == prep_time).where(planning.cook_time == cook_time).where(
        planning.total_time == total_time).where(planning.serves == serves).gino.scalar()
    return id


# NUTRITION

# OK
async def retrieve_nutrition_by_id(nutrition_id: int) -> Optional[schema.Nutrition]:
    obj = await model.Nutrition.get(nutrition_id)
    return obj.as_schema() if obj else None


# OK
async def delete_nutrition_by_id(nutrition_id: int) -> None:
    await model.Nutrition.delete.where(model.Nutrition.id == nutrition_id).gino.status()


# OK
async def create_nutrition_by_nutrition(energy: str = None, fat: str = None, saturated_fat: str = None,
                                        carbohydrate: str = None, sugars: str = None,
                                        protein: str = None, salt: str = None, fibre: str = None) -> int:
    nutrition = model.Nutrition
    try:
        obj_data = {
            "energy": energy,
            "fat": fat,
            "saturated_fat": saturated_fat,
            "carbohydrate": carbohydrate,
            "sugars": sugars,
            "protein": protein,
            "salt": salt,
            "fibre": fibre
        }
        nutrition_ = await nutrition.create(**obj_data)
        return nutrition_.id
    except asyncpg.exceptions.UniqueViolationError:
        id = await get_nutrition_id_by_parameters(energy, fat, saturated_fat, carbohydrate,
                                                  sugars, protein, salt, fibre)
        logging.info("This nutrition with this exact nutrient information already exists")
        return id


# OK
async def update_nutrition_by_id(nutrition_id: int, energy: str = None, fat: str = None, saturated_fat: str = None,
                                 carbohydrate: str = None, sugars: str = None,
                                 protein: str = None, salt: str = None, fibre: str = None) -> Optional[int]:
    nutrition = model.Nutrition
    try:
        obj = await nutrition.get(nutrition_id)

        energy = energy if (energy is not None) else obj.energy
        fat = fat if (fat is not None) else obj.fat
        saturated_fat = saturated_fat if (saturated_fat is not None) else obj.saturated_fat
        carbohydrate = carbohydrate if (carbohydrate is not None) else obj.carbohydrate
        sugars = sugars if (sugars is not None) else obj.sugars
        protein = protein if (protein is not None) else obj.protein
        salt = salt if (salt is not None) else obj.salt
        fibre = fibre if (fibre is not None) else obj.fibre

        obj_data = {
            "energy": energy,
            "fat": fat,
            "saturated_fat": saturated_fat,
            "carbohydrate": carbohydrate,
            "sugars": sugars,
            "protein": protein,
            "salt": salt,
            "fibre": fibre
        }

        await obj.update(**obj_data).apply()
    except AttributeError:
        logging.warning("Planning with id %s doesn't exist", str(nutrition_id))
    except asyncpg.exceptions.UniqueViolationError:
        id = await get_nutrition_id_by_parameters(energy, fat, saturated_fat, carbohydrate,
                                                  sugars, protein, salt, fibre)
        logging.error(
            "This nutrition with this exact nutrient information already exists. Update by id %s is not completed",
            nutrition_id)
        return id


# OK
async def get_nutrition_id_by_parameters(energy: str = None, fat: str = None, saturated_fat: str = None,
                                         carbohydrate: str = None, sugars: str = None,
                                         protein: str = None, salt: str = None, fibre: str = None) -> int:
    nutrition = model.Nutrition
    nutrition_id = await nutrition.query.where(nutrition.energy == energy).where(nutrition.fat == fat).where(
        nutrition.saturated_fat == saturated_fat).where(nutrition.carbohydrate == carbohydrate).where(
        nutrition.sugars == sugars).where(nutrition.protein == protein).where(
        nutrition.salt == salt).where(nutrition.fibre == fibre).gino.scalar()
    return nutrition_id
