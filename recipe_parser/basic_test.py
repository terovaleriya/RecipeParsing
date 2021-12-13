import json
import os
import re
import unittest

from recipe_parser.html_loader import get_html
from recipe_parser.parser import get_recipe, get_json
from recipe_parser.recipe import *

unittest.sortTestMethodsUsing = None

file = "pulled-beef-saladwithmintavocado0.A4.html"


class TestParserBeef(unittest.TestCase):

    def setUp(self):
        beef_url = "https://www.waitrose.com/content/waitrose/en/home/recipes/recipe_directory/p/pulled-beef-saladwithmintavocado0.A4.html"

        id = re.findall('[^/]+(?=/$|$)', beef_url)[0]
        try:
            cur_soup = get_html(beef_url)
            with open(id, 'w') as f:
                f.write(cur_soup)
        except ConnectionError:
            print("Can't get html from " + beef_url)

    def test_step2_parse(self):
        beef_file = open(file, "r")
        recipe = get_recipe(beef_file)
        my_recipe = Recipe("Pulled beef salad with mint & avocado", [Tag("Gluten Free")],
                           Planning("PT10M", "PT30M", "PT40M", "2"),
                           [Ingredient('380g pack slow cooked beef brisket'),
                            Ingredient('2 echalion shallots, thinly sliced into rings'),
                            Ingredient('2 essential Lemons, juice reserved'),
                            Ingredient('3 tbsp Cooks’ Ingredients Thai Sweet Chilli Sauce'),
                            Ingredient('1 x 350g tub Thai Sticky Rice'),
                            Ingredient('1 Waitrose 1 Perfectly Ripe Extra Large Avocado, stoned and sliced'),
                            Ingredient('½ x 25g pack mint, leaves picked'),
                            Ingredient('1 Cooks’ Ingredients Red Thai Chilli, thinly sliced')],
                           [Step(
                               "Preheat the oven to 200°C, gas mark 6. Cook the beef for 30 minutes, following pack instructions. Discard any large pieces of fat from the liquor before you cook."),
                               Step(
                                   "Toss the shallots with 5 tbsp lemon juice and the sweet chilli sauce to create a dressing, then set aside."),
                               Step(
                                   "When the meat is cooked, lift it from the juices and pull to shreds using two forks. Add 2 tbsp of the cooking juices to the shallots and sweet chilli sauce."),
                               Step("Meanwhile, heat the sticky rice according to the pack instructions."),
                               Step(
                                   "Toss the meat with the dressing, avocado, mint leaves and fresh Thai chilli, then serve straight away with the sticky rice.")],
                           {'Energy': '3,226kJ 768kcals', 'Fat': '29g', 'Saturated Fat': '7.9g', 'Carbohydrate': '78g',
                            'Sugars': '17g',
                            'Protein': '44g', 'Salt': '1.3g', 'Fibre': '8g'},
                           "//d1v30bmd12dhid.cloudfront.net/static/version6/content/dam/waitrose/recipes/images/p/WW-Pulled-Beef-Mint-Avocado-Salad-Shroud.gif/_jcr_content/renditions/cq5dam.thumbnail.400.400.png"
                           )
        self.assertEqual(my_recipe.title, recipe.title)
        self.assertEqual(str(my_recipe.tags), str(recipe.tags))
        self.assertEqual(str(my_recipe.planning), str(recipe.planning))
        self.assertEqual(str(my_recipe.ingredients), str(recipe.ingredients))
        self.assertEqual(str(my_recipe.instructions), str(recipe.instructions))
        self.assertEqual(my_recipe.nutrition, recipe.nutrition)
        self.assertEqual(my_recipe.image_url, recipe.image_url)
        beef_file.close()

    def test_step3_json(self):
        beef_file = open(file, "r")
        json_str = get_json(beef_file)
        my_json_str = json.JSONEncoder(ensure_ascii=False).encode(
            {
                "title": "Pulled beef salad with mint & avocado",
                "tags": [
                    {
                        "tag": "Gluten Free"
                    }
                ],
                "planning": {
                    "prep_time": "PT10M",
                    "cook_time": "PT30M",
                    "total_time": "PT40M",
                    "serves": "2"
                },
                "ingredients": [
                    {
                        "item": "380g pack slow cooked beef brisket"
                    },
                    {
                        "item": "2 echalion shallots, thinly sliced into rings"
                    },
                    {
                        "item": "2 essential Lemons, juice reserved"
                    },
                    {
                        "item": "3 tbsp Cooks’ Ingredients Thai Sweet Chilli Sauce"
                    },
                    {
                        "item": "1 x 350g tub Thai Sticky Rice"
                    },
                    {
                        "item": "1 Waitrose 1 Perfectly Ripe Extra Large Avocado, stoned and sliced"
                    },
                    {
                        "item": "½ x 25g pack mint, leaves picked"
                    },
                    {
                        "item": "1 Cooks’ Ingredients Red Thai Chilli, thinly sliced"
                    }
                ],
                "instructions": [
                    {
                        "step": "Preheat the oven to 200°C, gas mark 6. Cook the beef for 30 minutes, following pack instructions. Discard any large pieces of fat from the liquor before you cook."
                    },
                    {
                        "step": "Toss the shallots with 5 tbsp lemon juice and the sweet chilli sauce to create a dressing, then set aside."
                    },
                    {
                        "step": "When the meat is cooked, lift it from the juices and pull to shreds using two forks. Add 2 tbsp of the cooking juices to the shallots and sweet chilli sauce."
                    },
                    {
                        "step": "Meanwhile, heat the sticky rice according to the pack instructions."
                    },
                    {
                        "step": "Toss the meat with the dressing, avocado, mint leaves and fresh Thai chilli, then serve straight away with the sticky rice."
                    }
                ],
                "nutrition": {
                    "Energy": "3,226kJ 768kcals",
                    "Fat": "29g",
                    "Saturated Fat": "7.9g",
                    "Carbohydrate": "78g",
                    "Sugars": "17g",
                    "Protein": "44g",
                    "Salt": "1.3g",
                    "Fibre": "8g"
                }
                ,
                "image_url": "//d1v30bmd12dhid.cloudfront.net/static/version6/content/dam/waitrose/recipes/images/p/WW-Pulled-Beef-Mint-Avocado-Salad-Shroud.gif/_jcr_content/renditions/cq5dam.thumbnail.400.400.png"
            })
        self.assertEqual(my_json_str, json_str)
        beef_file.close()

        self.addCleanup(os.remove, file)


if __name__ == '__main__':
    unittest.main()
