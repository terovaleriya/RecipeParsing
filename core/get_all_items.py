from core import model


async def get_all_ingredients():
    return list(await model.Ingredients.query.gino.all())


async def get_all_products():
    return list(await model.Products.query.gino.all())
