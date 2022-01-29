import parser
import scanner
import sys


class Error:
    def __init__(self, description):
        self.description = description

    def get_description(self):
        return self.description

class Table:
    def __init__(self):
        self.table = {}

    def access(self, key):
        return self.table[key]

    def insert(self, key, value):
        self.table[key] = value

class Token:
    def __init__(self, tokentype, lexeme, literal, line):
       self.tokentype = tokentype
       self.lexeme = lexeme
       self.literal = literal
       self.line = line


source = ""
# open source file if supplied
if len(sys.argv) > 1 and len(sys.argv) < 3:
    f = open(sys.argv[1])
    source = f.read()
    s = scanner.Scanner(source)
    tokens = s.split_into_lexemes()
    print(tokens)
    p = parser.Parser(source, tokens)
    print(p.is_valid_lisp_syntax())
