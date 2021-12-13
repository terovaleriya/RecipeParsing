import os
import re

from recipe_parser.html_loader import get_html

folder = "recipes_html/"
urls_file = "files/recipes_urls.txt"

if not os.path.exists(folder):
    os.makedirs(folder)

error = open("files/connection_error_urls.txt", "w")

urls = open(urls_file, "r")
urls_list = urls.read().split("\n")
for url in urls_list:
    id = re.findall('[^/]+(?=/$|$)', url)[0]
    if not os.path.exists(folder + id):
        try:
            cur_soup = get_html(url)
            with open(folder + id, 'w') as f:
                f.write(cur_soup)
        except ConnectionError:
            print("Can't get html from " + url)
            error.write(url)
            if url is not urls_list[-1]:
                error.write("\n")
error.close()
