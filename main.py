import re

class Token:
    def init(self, tokentype, lexeme, literal, line):
       self.tokentype = tokentype
       self.lexeme = lexeme
       self.literal = literal
       self.line = line

class Scanner:
    def init(self, source):
        self.current = -1
        self.source = source
        self.tokens = []

    def split_into_lexemes(self):
        self.tokens = list(filter(None, re.split(r"(\s|[()])", query)))

def balanced_parentheses(string) -> bool:
   parentheses = []
   for char in string:
       if char == '(':
           parentheses.insert(-1, char)
       elif char == ')' and len(parentheses) > 0:
           parentheses.pop()
       elif char == ')':
           return False

   if len(parentheses) > 0:
        return False

   return True

# the REPL begins
while True:
    query = input("> ")
    if balanced_parentheses(query):
        print(query)

