from config import DEBUG


def read_file(path: str) -> list:
    with open(path, encoding='utf8') as file:
        return file.readlines()


def p(s: str):
    if (DEBUG):
        print(s)
