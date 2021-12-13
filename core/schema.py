class Recipe:
    def __init__(self, recipe_id: int, title: str):
        self.recipe_id = recipe_id
        self.title = title

    def __str__(self) -> str:
        return str(self.recipe_id) + ", " + self.title


class Ingredient:
    def __init__(self, ingredient_id: int, raw_string: str, name: str = None, quantity: str = None,
                 comment: str = None):
        self.ingredient_id = ingredient_id
        self.raw_string = raw_string
        self.name = name
        self.quantity = quantity
        self.comment = comment

    def __str__(self) -> str:
        return str(self.ingredient_id) + ", " + str(self.name) + ", " + \
               str(self.quantity) + ", " + str(self.comment) + ", " + self.raw_string


class Instruction:
    def __init__(self, instruction_id: int, instruction: str):
        self.instruction_id = instruction_id
        self.instruction = instruction

    def __str__(self) -> str:
        return str(self.instruction_id) + ", " + self.instruction


class Tag:
    def __init__(self, tag_id: int, tag: str):
        self.tag_id = tag_id
        self.tag = tag

    def __str__(self) -> str:
        return str(self.tag_id) + ", " + self.tag


class Image:
    def __init__(self, image_id: int, image: str):
        self.image_id = image_id
        self.image = image

    def __str__(self) -> str:
        return str(self.image_id) + ", " + self.image


class Plan:
    def __init__(self, planning_id: int, prep_time: str, cook_time: str, total_time: str, serves: str):
        self.planning_id = planning_id
        self.prep_time = prep_time
        self.cook_time = cook_time
        self.total_time = total_time
        self.serves = serves

    def __str__(self) -> str:
        return str(self.planning_id) + ", " + str(self.prep_time) + ", " + \
               str(self.cook_time) + ", " + str(self.total_time) + ", " + str(self.serves)


class Nutrition:
    def __init__(self, nutrition_id: int, energy: str, fat: str, saturated_fat: str, carbohydrate: str, sugars: str,
                 protein: str,
                 salt: str, fibre: str):
        self.nutrition_id = nutrition_id
        self.energy = energy
        self.fat = fat
        self.saturated_fat = saturated_fat
        self.carbohydrate = carbohydrate
        self.sugars = sugars
        self.protein = protein
        self.salt = salt
        self.fibre = fibre

    def __str__(self) -> str:
        return str(self.nutrition_id) + ", " + str(self.energy) + ", " + \
               str(self.fat) + ", " + str(self.saturated_fat) + ", " + str(self.carbohydrate) + ", " + str(
            self.sugars) + ", " + \
               str(self.protein) + ", " + str(self.salt) + ", " + str(self.fibre)


class Product:
    def __init__(self, product_id: int, name: str, size: str, price: str, image_url: str):
        self.product_id = product_id
        self.name = name
        self.size = size
        self.price = price
        self.image_url = image_url

    def __str__(self) -> str:
        return str(self.product_id) + ", " + self.name + ", " + self.size + ", " + self.price + ", " + self.image_url
