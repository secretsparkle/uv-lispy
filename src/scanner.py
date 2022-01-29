import re

class Scanner:
    def __init__(self, source):
        self.source = source

    # split into tokens
    # * by two double quotes
    # * by whitespace
    # * by parentheses
    def split_into_lexemes(self):
        tokens = list(filter(None, re.split(r"(\".+\"|\s|[()])", self.source)))
        return [x for x in tokens if x!='' and x!=' ' and x!='\n']

