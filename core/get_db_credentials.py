import json
from os.path import dirname, join

MAIN_DIRECTORY = dirname(dirname(__file__))


def get_full_path(*path):
    return join(MAIN_DIRECTORY, *path)


def get_db_credentials(config: str) -> str:
    with open(config) as file:
        config_file = json.load(file)

    username = config_file["username"]
    password = config_file["password"]
    dbname = config_file["dbname"]
    host = config_file["host"]

    res = "postgresql://%s:%s@%s/%s" % (username, password, host, dbname)
    return res


def get_credentials():
    return get_db_credentials(get_full_path("config.json"))
    # return "postgresql://racine@localhost/stepa"
