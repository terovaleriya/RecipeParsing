from typing import List


class Tag:
    def __init__(self, tag: str):
        self.tag = tag

    def __repr__(self):
        return self.tag


class Ingredient:
    def __init__(self, item: str,
                 # amount: float, units: str
                 ):
        self.item = item
        # self.amount = amount
        # self.measure = units

    def __repr__(self):
        return self.item \
            # + ": "+ str(self.amount) + self.measure


class Step:
    def __init__(self, step: str):
        self.step = step

    def __repr__(self):
        return self.step


# class Nutrition:
#     def __init__(self, ...):
#         self.energy = energy
#         self.fat = fat
#         self.saturated_fat = saturated_fat
#         self.carbohydrate = carbohydrate
#         self.sugars = sugars
#         self.protein = protein
#         self.salt = salt
#         self.fibre = fibre


class Planning:
    def __init__(self, prep_time: str, cook_time: str, total_time: str, serves: str):
        self.prep_time = prep_time
        self.cook_time = cook_time
        self.total_time = total_time
        self.serves = serves

    def __str__(self):
        return "Preparation time: " + self.prep_time + "\n" + "Cooking time: " + self.cook_time + "\n" + "Total time: " + self.total_time + "\n" + "Serves: " + self.serves


class Recipe:
    def __init__(self, title: str, tags: List[Tag], planning: Planning, ingredients: List[Ingredient],
                 instructions: List[Step], nutrition: dict, image_url: str):
        self.title = title
        self.tags = tags
        self.planning = planning
        self.ingredients = ingredients
        self.instructions = instructions
        self.nutrition = nutrition
        self.image_url = image_url
