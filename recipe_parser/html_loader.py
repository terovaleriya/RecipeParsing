import logging

import requests
from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter
from urllib3 import Retry


# загружаем HTML страницу по url
def get_html(url) -> str:
    # logging.basicConfig(level=logging.DEBUG)
    s = requests.Session()

    # Если получаем какой-то код кроме 200, пробуем еще раз, но не более чем 10 раз на страницу
    retry_strategy = Retry(
        total=10,
        backoff_factor=2,
        status_forcelist=[x for x in requests.status_codes.codes if x != 200]
    )
    s.mount('http://', HTTPAdapter(max_retries=retry_strategy))

    get = s.get(url)

    # если мы все-таки не смогли получить страницу (потому что ее там больше нет или еще 1050 причин почему),
    # сохраним эту инфу
    if get.status_code != 200:
        raise ConnectionError(get.status_code)

    get.encoding = "utf-8"
    page_data = get.text

    return page_data


# теперь у нас есть HTML строка (файл), чтобы парсить ее, преобразуем в soup
def get_soup(html_page) -> BeautifulSoup:
    return BeautifulSoup(html_page, "html.parser")
