
from enum import Enum
from enum import auto
import re

class TokenType(Enum):
    # symbols
    LEFT_PAREN = auto()
    RIGHT_PAREN = auto()

    # one or more characters
    IDENTIFIER = auto()
    NUMBER = auto()
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
            print(lexeme[0])
            print(lexeme[1])
            if lexeme[0] == "=":
                self.tokens.append(Token(TokenType.KEYWORD_IDENTIFIER, "=", lexeme[1]))
            elif lexeme[0] == ">":
                self.tokens.append(Token(TokenType.KEYWORD_IDENTIFIER, ">", lexeme[1]))
            elif lexeme[0] == "(":
                self.tokens.append(Token(TokenType.LEFT_PAREN, "(", lexeme[1]))
            elif lexeme[0] == "<":
                self.tokens.append(Token(TokenType.KEYWORD_IDENTIFIER, "<", lexeme[1]))
            elif lexeme[0]== "-":
                self.tokens.append(Token(TokenType.KEYWORD_IDENTIFIER, "-", lexeme[1]))
            elif lexeme[0] == "+":
                self.tokens.append(Token(TokenType.KEYWORD_IDENTIFIER, "+", lexeme[1]))
            elif lexeme[0] == ")":
                self.tokens.append(Token(TokenType.RIGHT_PAREN, ")", lexeme[1]))
            elif lexeme[0] == "/":
                self.tokens.append(Token(TokenType.KEYWORD_IDENTIFIER, "/", lexeme[1]))
            elif lexeme[0] == "*":
                self.tokens.append(Token(TokenType.KEYWORD_IDENTIFIER, "*", lexeme[1]))
            elif lexeme[0] == "and":
                self.tokens.append(Token(TokenType.KEYWORD_IDENTIFIER, "and", lexeme[1]))
            elif lexeme[0] == "define":
                self.tokens.append(Token(TokenType.KEYWORD_IDENTIFIER, "define", lexeme[1]))
            elif lexeme[0] == "false":
                self.tokens.append(Token(TokenType.FALSE, "false", lexeme[1]))
            elif lexeme[0] == "nil":
                self.tokens.append(Token(TokenType.NIL, "nil", lexeme[1]))
            elif lexeme[0] == "not":
                self.tokens.append(Token(TokenType.KEYWORD_IDENTIFIER, "not", lexeme[1]))
            elif lexeme[0] == "or":
                self.tokens.append(Token(TokenType.KEYWORD_IDENTIFIER, "or", lexeme[1]))
            elif lexeme[0] == "true":
                self.tokens.append(Token(TokenType.TRUE, "true", lexeme[1]))
            elif re.match("^[a-zA-Z]+\-[a-zA-Z]+|^[a-zA-Z]+", lexeme[0]):
                self.tokens.append(Token(TokenType.IDENTIFIER, lexeme[0], lexeme[1]))
            elif re.match("[0-9]+", lexeme[0]):
                self.tokens.append(Token(TokenType.NUMBER, lexeme[0], lexeme[1]))
            elif re.match("\"*\"", lexeme[0]):
                self.tokens.append(Token(TokenType.STRING, lexeme[0], lexeme[1]))
            else:
                print("No match")
        self.tokens.append(Token(TokenType.EOF, "", self.lexemes[-1][1]))


    # split into lexemes
    # * by two double quotes
    # * by whitespace
    # * by parentheses
    def split_into_lexemes(self):
        raw_lexemes = list(filter(None, re.split(r"(\".+\"|\s|[()])", self.source)))
        line = 0
        for lexeme in raw_lexemes:
            if lexeme == '\n':
                line += 1
                continue
            self.lexemes.append((lexeme, line))
        self.lexemes = [lexeme for lexeme in self.lexemes if lexeme[0]!='' and lexeme[0]!=' ' and lexeme[0]!='\n']

