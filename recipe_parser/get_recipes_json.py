import os

from recipe_parser.parser import get_json

html_folder = "recipes_html/"
json_folder = "recipes_json/"

if not os.path.exists(json_folder):
    os.makedirs(json_folder)

for file in os.listdir(html_folder):
    with open(json_folder + file[:-5] + ".json", "w") as f:
        file = open(html_folder + file, "r")
        f.write(get_json(file))
        file.close()
