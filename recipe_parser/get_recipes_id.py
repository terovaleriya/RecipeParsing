import re

# файл с url
url_file = "files/recipes_urls.txt"
# куда пишем id
id_file = "files/ids.txt"

# хотим достать уникальные идентефикаторы для рецептов из url (так называются файлы с html рецептов)
with open(url_file, 'r') as urls:
    matches = urls.read().split("\n")
    matches = set([re.findall('[^/]+(?=/$|$)', url)[0] for url in matches])

# запишем их в ids_*.txt
matches_file = open(id_file, 'w')
for match in matches:
    matches_file.write(match)
    if match is not list(matches)[-1]:
        matches_file.write("\n")
matches_file.close()
