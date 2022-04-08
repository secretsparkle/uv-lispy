
from enum import Enum
from enum import auto
import re

class TokenType(Enum):
    # symbols
    LEFT_PAREN = auto()
    RIGHT_PAREN = auto()

    # one or more characters
    AS_OPERATOR = auto()
    BINARY_OPERATOR = auto()
    DEFINE_OPERATOR = auto()
    IMPORT_OPERATOR = auto()
    FROM_OPERATOR = auto()
    IDENTIFIER = auto()
    LAMBDA_OPERATOR = auto()
    NUMBER = auto()
    QUOTE_OPERATOR = auto()
    STRING = auto()

    KEYWORD_IDENTIFIER = auto()
    EOF = auto()
    FALSE = auto()
    NIL = auto()
    TRUE = auto()

class Token:
    def __init__(self, token_type, literal, line):
       self.token_type = token_type
       self.literal = literal
       self.line = line

class Scanner:
    def __init__(self, source):
        self.lexemes = []
        self.source = source
        self.tokens = []

    def define_tokens(self):
        for lexeme in self.lexemes:
            if lexeme[0] == "=":
                self.tokens.append(Token(TokenType.BINARY_OPERATOR, "==", lexeme[1]))
            elif lexeme[0] == "if":
                self.tokens.append(Token(TokenType.KEYWORD_IDENTIFIER, "if", lexeme[1]))
            elif lexeme[0] == ">":
                self.tokens.append(Token(TokenType.BINARY_OPERATOR, ">", lexeme[1]))
            elif lexeme[0] == "(":
                self.tokens.append(Token(TokenType.LEFT_PAREN, "(", lexeme[1]))
            elif lexeme[0] == "<":
                self.tokens.append(Token(TokenType.BINARY_OPERATOR, "<", lexeme[1]))
            elif lexeme[0]== "-":
                self.tokens.append(Token(TokenType.BINARY_OPERATOR, "-", lexeme[1]))
            elif lexeme[0] == "+":
                self.tokens.append(Token(TokenType.BINARY_OPERATOR, "+", lexeme[1]))
            elif lexeme[0] == ")":
                self.tokens.append(Token(TokenType.RIGHT_PAREN, ")", lexeme[1]))
            elif lexeme[0] == "/":
                self.tokens.append(Token(TokenType.BINARY_OPERATOR, "/", lexeme[1]))
            elif lexeme[0] == "*":
                self.tokens.append(Token(TokenType.BINARY_OPERATOR, "*", lexeme[1]))
            elif lexeme[0] == "and":
                self.tokens.append(Token(TokenType.BINARY_OPERATOR, "and", lexeme[1]))
            elif lexeme[0] == "as":
                self.tokens.append(Token(TokenType.AS_OPERATOR, "as", lexeme[1]))
            elif lexeme[0] == "define":
                self.tokens.append(Token(TokenType.DEFINE_OPERATOR, "define", lexeme[1]))
            elif lexeme[0] == "import":
                self.tokens.append(Token(TokenType.IMPORT_OPERATOR, "import", lexeme[1]))
            elif lexeme[0] == "from":
                self.tokens.append(Token(TokenType.FROM_OPERATOR, "from", lexeme[1]))
            elif lexeme[0] == "false":
                self.tokens.append(Token(TokenType.FALSE, "false", lexeme[1]))
            elif lexeme[0] == "lambda":
                self.tokens.append(Token(TokenType.LAMBDA_OPERATOR, "lambda", lexeme[1]))
            elif lexeme[0] == "nil":
                self.tokens.append(Token(TokenType.NIL, "nil", lexeme[1]))
            elif lexeme[0] == "not":
                self.tokens.append(Token(TokenType.KEYWORD_IDENTIFIER, "not", lexeme[1]))
            elif lexeme[0] == "or":
                self.tokens.append(Token(TokenType.BINARY_OPERATOR, "or", lexeme[1]))
            elif lexeme[0] == "true":
                self.tokens.append(Token(TokenType.TRUE, "true", lexeme[1]))
            elif re.match("^[a-zA-Z]+\-[a-zA-Z]+|^[a-zA-Z]+", lexeme[0]):
                self.tokens.append(Token(TokenType.IDENTIFIER, lexeme[0], lexeme[1]))
            elif re.match("^(__)[a-zA-Z]*__", lexeme[0]):
                self.tokens.append(Token(TokenType.IDENTIFIER, lexeme[0], lexeme[1]))
            elif re.match("[0-9]+", lexeme[0]):
                self.tokens.append(Token(TokenType.NUMBER, lexeme[0], lexeme[1]))
            elif lexeme[0] == "\'":
                self.tokens.append(Token(TokenType.QUOTE_OPERATOR, "'", lexeme[1]))
            elif re.match("\".*\"", lexeme[0]):
                self.tokens.append(Token(TokenType.STRING, lexeme[0], lexeme[1]))
            else:
                print("No match for " + lexeme[0])
                return False
        self.tokens.append(Token(TokenType.EOF, "", self.lexemes[-1][1]))
        return True


    # split into lexemes
    # * by two double quotes
    # * by whitespace
    # * by parentheses
    def split_into_lexemes(self):
        raw_lexemes = list(filter(None, re.split(r"(\"[^\"]+\"|\s|[()])", self.source)))
        line = 0
        for lexeme in raw_lexemes:
            if lexeme == '\n':
                line += 1
                continue
            self.lexemes.append((lexeme, line))
        self.lexemes = [lexeme for lexeme in self.lexemes if lexeme[0]!='' and lexeme[0]!=' ' and lexeme[0]!='\n']

