# -*- coding:utf-8 -*-
# __author__ = 'Shanks'

import re
from compiler.typedef import*


class Token(object):
    def __init__(self, row, type_index, value):
        self.row = row
        self.value = value
        self.type = KW_TYPE[value] if type_index == KW_INDEX \
            else SEP_TYPE[value] if type_index == SEP_INDEX \
            else OPE_TYPE[value] if type_index == OPE_INDEX \
            else TOKEN_TYPE[type_index]




class Lexer:

    def __init__(self, file_path):
        self.tokens = []
        self.file = open(file_path, 'r')
        self.main()
        # add a file end symbol
        self.tokens.append(Token(self.tokens[-1].row, EOF_INDEX, 'EOF'))

    def main(self):
        row = 0
        string = ''
        str_reading = False

        for line in self.file:
            row += 1
            wordlist = self.word_list(line)
           # print(wordlist)
            i = 0
            while i < len(wordlist):
                word = wordlist[i]
                if not str_reading:
                    if self.is_blank(word):
                        pass
                    elif self.is_keyword(word):
                        self.tokens.append(Token(row, KW_INDEX, word))
                    elif self.is_identifier(word):
                        self.tokens.append(Token(row, IDE_INDEX, word))
                    elif self.is_separator(word):
                        self.tokens.append(Token(row, SEP_INDEX, word))
                    elif self.is_operator(word):
                        word2 = wordlist[i + 2]
                        if self.is_operator(word2) and wordlist[i+1] == '':
                            if word + word2 in operators[DYADIC]:
                                self.tokens.append(Token(row, OPE_INDEX, word + word2))
                                i = i + 3
                                continue
                            else:
                                print('ERROR: in {} row, {} is not defined'.format(row, word + word2))
                        else:
                            self.tokens.append(Token(row, OPE_INDEX, word))
                    elif self.is_digit_const(word):
                        self.tokens.append(Token(row, DIG_INDEX, word))
                    elif word == '"':
                        str_reading = True
                        self.tokens.append(Token(row, SEP_INDEX, word))
                    else:
                        print('ERROR: in {} row, {} is not defined'.format(row, word))
                    i = i + 1

                else:
                    if word != '"':
                        string += word
                        i += 1
                    else:
                        str_reading = False
                        self.tokens.append(Token(row, STR_INDEX, string))
                        self.tokens.append(Token(row, SEP_INDEX, word))
                        string = ''
                        i = i + 1

        if string:
            print('ERROR: in {} row, lack of the "'.format(row))

    @staticmethod
    def word_list(string):
        s = re.sub('/s+', ' ', string)
        return re.split('([^\w.])', s)

    @staticmethod
    def is_blank(word):
        if re.match('\s+', word) or word == '':
            return True
        return False

    @staticmethod
    def is_keyword(word):
        for words in keywords:
            if word in words:
                return True
        return False

    @staticmethod
    def is_operator(word):
        for words in operators:
            if word in words:
                return True
        return False

    @staticmethod
    def is_separator(word):
        return word in separators

    @staticmethod
    def is_identifier(word):
        if re.match('[a-zA-Z_]\w*', word):
            return True
        return False

    @staticmethod
    def is_digit_const(word):
        if re.match('\d+\.?\d*', word):
            return True
        return False

if __name__ == '__main__':
    laser = Lexer(r'D:\Project\python\Real\editor\compiler\text.c')

    for t in laser.tokens:
        print(t.row, t.type, t.value)



