import re

class Query:
    def __init__(self, query_words):
        self.query_words = re.findall(r'\w+', query_words.lower())


#just in case
class Utilities:
    pass