import json
import re

from bs4 import BeautifulSoup

from recipe_parser.html_loader import get_soup
from recipe_parser.recipe import *


def get_title(recipe: BeautifulSoup) -> str:
    title = recipe.find('h2').text.strip()
    assert title
    return title


def get_tags(recipe: BeautifulSoup) -> List[Tag]:
    tags = recipe.find('ul', {'class': "tags"})
    if tags:
        all_tags: List[Tag] = []
        for tag in tags.findAll('li'):
            all_tags.append(Tag(tag.text.strip()))
        return all_tags


def get_planning(recipe: BeautifulSoup) -> Planning:
    prep_time = recipe.find('span', {'itemprop': "prepTime"})
    prep_time = prep_time["content"].strip() if prep_time else None
    cook_time = recipe.find('span', {'itemprop': "cookTime"})
    cook_time = cook_time["content"].strip() if cook_time else None
    total_time = recipe.find('span', {'itemprop': "totalTime"})
    total_time = total_time["content"].strip() if total_time else None
    serves = recipe.find('span', {'itemprop': "recipeYield"})
    serves = serves.text.strip() if serves else None

    return Planning(prep_time, cook_time, total_time, serves)


# getting method and ingredients strategy is the same
def get_i(recipe: BeautifulSoup, pattern):
    templist = recipe.find("div", {'class': pattern})
    if not templist.text.strip():
        templist = recipe.find("div", class_="parbase additionalinfo text")
    if templist.find("div", class_="text"):
        templist = templist.find('div', class_="text")
    ilist = []
    if templist.find("ol"):
        for item in templist.findAll("ol"):
            ilist.append(item.text)
    else:
        ilist = templist.text.split('\n')
    return ilist


def get_ingredients(recipe: BeautifulSoup) -> List[Ingredient]:
    ingredients_list = get_i(recipe, re.compile('parbase ingredients text.*'))
    ingredients: List[Ingredient] = []
    for ingredient in ingredients_list:
        ingredient = ingredient.replace("• ", "").replace("*", "").replace("", " ")
        ingredient = re.sub(' +', ' ', ingredient)
        comment = ingredient.startswith("(") and ingredient.endswith(")")
        ingredient = ingredient.strip()
        if ingredient and not ingredient.isupper() and not ingredient.endswith(":") and not comment:
            ingredients.append(Ingredient(ingredient))
    assert ingredients
    return ingredients


def get_instructions(recipe: BeautifulSoup) -> List[Step]:
    instructions_list = get_i(recipe, re.compile("method parbase text.*"))
    # избавляемся от Cook's tip
    strings_with_substring = [string for string in instructions_list if
                              string.startswith(("Cook’s tip", "Cook's tip", "Cook's Tip"))]
    if strings_with_substring:
        instructions_list = instructions_list[:instructions_list.index(strings_with_substring[0])]
    instructions: List[Step] = []
    for instruction in instructions_list:
        instruction = instruction.replace("• ", "")
        instruction = re.sub(' +', ' ', instruction).strip()
        instruction = re.sub(re.compile('^\d+(\s*\.|\s)'), "", instruction)
        instruction = instruction.replace("\n", " ")
        if instruction and not instruction.isupper() and not instruction.endswith(":"):
            instructions.append(Step(instruction.strip()))
    return instructions


def get_image(recipe: BeautifulSoup) -> str:
    image = recipe.find('img')["src"]

    # getting a larger picture (some of 200.200 don't exist)
    image = image.replace("200.200", "400.400")
    return image.strip()


def get_nutrition(recipe: BeautifulSoup) -> dict:
    table = recipe.find('div', {'itemprop': "nutrition"})
    if table:
        th = table.findAll("th")
        td = table.findAll("td")
        return {i.text.strip(): cell.text.strip() for i, cell in zip(th, td)}


def get_recipe(file):
    data = file.read()
    recipe = recipe_content(data)
    return Recipe(get_title(recipe), get_tags(recipe), get_planning(recipe), get_ingredients(recipe),
                  get_instructions(recipe),
                  get_nutrition(recipe), get_image(recipe))


# getting json out of parsed Recipe
def get_json(file):
    recipe = get_recipe(file)
    return json.dumps(recipe.__dict__, default=lambda o: o.__dict__, ensure_ascii=False)


def recipe_content(html_data) -> BeautifulSoup:
    recipe = get_soup(html_data).find('div', {'itemtype': "http://schema.org/Recipe"})
    assert recipe
    return recipe
