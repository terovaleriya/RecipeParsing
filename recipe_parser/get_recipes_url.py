import os
import re

from recipe_parser.html_loader import get_html, get_soup

# страница с рецептами Waitrose
url = "https://www.waitrose.com/content/waitrose/en/home/recipes.html"
folder = "files"
if not os.path.exists(folder):
    os.makedirs(folder)

os.chdir(folder)

# файл, куда будем писать url
to_file = "recipes_urls.txt"

# достаем список категорий
page_html = get_html(url)
soup = get_soup(page_html)
soup = soup.find('div', {'class': "l-content"})
categories = soup.findAll("a", href=re.compile("/home/recipes/.+$"))
categories = [category['href'] for category in categories]
categories = [category if category.startswith("https://www.waitrose.com") else 'https://www.waitrose.com' + category for
              category in categories]
categories = set(categories)

# из каждой категории достаем все рецепты
# recipes_per_category_*.txt – распределение рецептов по категориям, url могут повторяться
all_recipes = []
for category in categories:
    try:
        with open('recipes_per_category.txt', 'w') as distribution:
            category_html = get_html(category)
            category_soup = get_soup(category_html)
            recipes = category_soup.findAll("a", href=re.compile("/home/recipes/recipe_directory.+$"))
            distribution.write("\nКатегория: " + category + "\n")
            distribution.write("Рецептов в категории: " + str(len(recipes)) + "\n")

            recipes = [recipe['href'] for recipe in recipes]
            recipes = [
                recipe if recipe.startswith(
                    "https://www.waitrose.com") else 'https://www.waitrose.com' + recipe + ".html"
                for recipe in recipes]
            recipes = [re.findall('.+?\.html', recipe)[0] for recipe in recipes]
            distribution.write("Url рецептов: " + "\n".join(recipes) + "\n")
            all_recipes.extend(recipes)
    except ConnectionError:
        print("Couldn't get " + category)

# превращаем полученный url в А4-url
all_recipes = [recipe[:-5] + ".A4" + recipe[-5:] for recipe in all_recipes]

# избавляемся от дубликатов
all_recipes = set(all_recipes)

# recipes_urls_*.txt – уникальный список всех url рецептов
with open(to_file, 'w') as f:
    for recipe_url in all_recipes:
        f.write(recipe_url)
        if recipe_url is not list(all_recipes)[-1]:
            f.write("\n")
