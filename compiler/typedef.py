# -*- coding:utf-8 -*-
# __author__ = 'Shanks'



# classify

TOKEN_TYPE = ['KEY_WORD', 'OPERATOR', 'SEPARATOR',
              'IDENTIFIER', 'DIGIT_CONSTANT', 'STRING_CONSTANT', 'EOF']

# index
KW_INDEX = 0
OPE_INDEX = 1
SEP_INDEX = 2
IDE_INDEX = 3
DIG_INDEX = 4
STR_INDEX = 5
EOF_INDEX = 6
# solidify
KW_TYPE = {'include': 'INCLUDE', 'int': 'INT', 'float': 'FLOAT', 'char': 'CHAR', 'double': 'DOUBLE', 'void': 'VOID',
           'NULL': 'NULL', 'for': 'FOR', 'if': 'IF', 'else': 'ELSE', 'while': 'WHILE', 'do': 'DO', 'return': 'RETURN'}
OPE_TYPE = {'=': 'ASSIGN', '&': 'ADDRESS', '<': 'LT', '>': 'GT', '++': 'SELF_PLUS', '--': 'SELF_MINUS', '+': 'PLUS',
            '-': 'MINUS', '*': 'MUL', '!': 'NOT', '/': 'DIV', '>=': 'GET', '<=': 'LET', r'!=': 'UQT', '==': 'EQUAL',
            '+=': 'PLUS_EQU', '-=': 'MINUS_EQU', '//': 'NOTE', '->': 'ATTR'}
SEP_TYPE = {'(': 'LL_BRACKET', ')': 'RL_BRACKET', '{': 'LB_BRACKET', '}': 'RB_BRACKET', '@': 'NONE',
            '[': 'LM_BRACKET', ']': 'RM_BRACKET', ',': 'COMMA', '"': 'DOUBLE_QUOTE', ';': 'SEMICOLON', '#': 'SHARP'}
# key word
keywords = [['int', 'float', 'double', 'char', 'void', 'NULL'],
            ['if', 'for', 'while', 'do', 'else'], ['include', 'return']]
DATA = 0
CONTROL = 1
OTHER = 2
# operator
operators = [['=', '&', '<', '>', '+', '-', '*', '/', '!'],
             ['++', '--', '>=', '<=', '!=', '+=', '-=', '==', '//', '->']]
UNARY = 0
DYADIC = 1

# delimiters
separators = ['(', ')', '{', '}', '[', ']', ',', ';', '#']

