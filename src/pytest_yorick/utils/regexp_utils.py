import re


def regexp_compile(pattern):
    return re.compile(pattern)


def regexp_match(pattern, string):
    return re.match(pattern, string)


def regexp_search(pattern, path):
    return re.search(pattern, path)
