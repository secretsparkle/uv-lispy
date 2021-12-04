import re

class Token:
    def init(self, tokentype, lexeme, literal, line):
       self.tokentype = tokentype
       self.lexeme = lexeme
       self.literal = literal
       self.line = line

    # to_string function? not sure in python

class Scanner:
    def init(self, source):
        self.current = -1
        self.source = source
        self.tokens = []

    def split_into_lexemes(self):
        self.tokens = list(filter(None, re.split(r"(\s|[()])", query)))

    def scan_tokens(self):
        # we are at the beginning of the next lexeme
        while not is_at_end():
            start = current
            scan_token()

        tokens.append(Token("EOF", "", "", line)) # this definitely needs work

TokenType = {
    # Single Character Tokens
    "LEFT_PAREN", "RIGHT_PAREN", "LEFT_BRACE", "RIGHT_BRACE", "COMMA", "DOT",
    "MINUS", "PLUS", "SEMICOLON", "SLASH", "STAR",

    # One or Two Character Tokens
    "BANG", "BANG_EQUAL", "EQUAL", "GREATER", "GREATER_EQUAL", "LESS", "LESS_EQUAL",

    #Literals
    "IDENTIFIER", "STRING", "NUMBER",

    # Keywords
    "EOF"
}

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

