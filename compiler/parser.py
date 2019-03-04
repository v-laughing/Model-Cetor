# -*- coding:utf-8 -*-
# __author__ = 'Shanks'

from compiler.syntaxtree import *

from compiler.lexer import *


class Parser(object):
    # sentence pattern
    CONTROL_SENTENCE = 'CONTROL_SENTENCE'
    INCLUDE = 'INCLUDE'
    ANNOTATION = 'ANNOTATION'
    FUNCTION_STATEMENT = 'FUNCTION_STATEMENT'
    STATEMENT = 'STATEMENT'
    FUNCTION_CALL = 'FUNCTION_CALL'
    ASSIGNMENT = 'ASSIGNMENT'
    RETURN = 'RETURN'

    def __init__(self):
        lexer = Lexer(r'D:\Project\python\Real\editor\compiler\text.c')
        # lexical elements
        self.tokens = lexer.tokens
        self.tokens_len = len(self.tokens)
        # element index
        self.index = 0

        self.tree = SyntaxTree()
        self.main()

    def error(self, token):
        print('ERROR: in {} row, {} syntax error!'.format(token.row, token.value))
        exit()

    # look ahead some elements
    def look(self, i=0):
        return self.tokens[self.index + i]

    def match(self, value):
        token = self.tokens[self.index]
        if token.value == value:
            self.index = self.index + 1
        else:
            self.error(token)

    def main(self):
        self.tree.current = self.tree.root = SyntaxTreeNode('Sentence')

        while self.index < self.tokens_len:
            sentence_pattern = self._judge_sentence_pattern()
            if sentence_pattern is None:
                self.index += 1
            elif sentence_pattern == self.INCLUDE:
                self._include()
            elif sentence_pattern == self.ASSIGNMENT:
                self._assignment()
            elif sentence_pattern == self.STATEMENT:
                self._statement()
            else:
                exit()

    def _judge_sentence_pattern(self):
        token = self.look()
        if token.value == 'EOF':
            return
        token1 = self.look(1)
        if token.value == '#' and token1.value == 'include':
            return self.INCLUDE
        elif token.value == '//':
            return self.ANNOTATION
        elif token.value in keywords[CONTROL]:
            return self.CONTROL_SENTENCE
        elif token.value in keywords[DATA] and token1.type == 'IDENTIFIER':
            token2 = self.look(2)
            if token2.value == '(':
                return self.FUNCTION_STATEMENT
            elif token2.value in [',', ';', '[', '=']:
                return self.STATEMENT
            else:
                self.error(token2)
        elif token.type == 'IDENTIFIER':
            if token1.value == '(':
                return self.FUNCTION_CALL
            elif token1.value in ['=', '[']:
                return self.ASSIGNMENT
            else:
                self.error(token1)
        elif token.value == 'return':
            return self.RETURN
        else:
            self.error(token)

    def _include(self, father=None):
        self.index += 2
        include_tree = self._abstract_tree('include', father)
        if self.look().value == '"':
            self.index += 1
            include_tree.add_child_node(SyntaxTreeNode(self.look().value))
            self.index += 1
            self.match('"')
        elif self.look().value == '<':
            self.index += 1
            include_tree.add_child_node(SyntaxTreeNode(self.look().value))
            self.index += 1
            self.match('>')
        else:
            self.error(self.look())

    def _annotation(self):
        self.match('//')
        row = self.look().row
        while self.tokens[self.index].row == row:
            self.index += 1

    def _function_statement(self, father=None):
        if not father:
            father = self.tree.root
        func_tree = SyntaxTree()
        func_tree.current = func_tree.root = SyntaxTreeNode('FunctionStatement')
        self.tree.add_child_node(func_tree.root, father)
        # return type
        type_token = self.look()
        func_tree.add_child_node(SyntaxTreeNode('Type'))
        func_tree.add_child_node(SyntaxTreeNode(type_token.value, 'DATA_TYPE',
                                           {'type': type_token.value}))
        self.index += 1
        # function name
        name_type = self.look()
        func_tree.add_child_node(SyntaxTreeNode('FunctionName'), func_tree.root)
        func_tree.add_child_node(SyntaxTreeNode(name_type.value, 'IDENTIFIER',
                                                          {'type': 'FUNCTION_NAME'}))
        self.index += 1
        # parameter list
        self.match('(')
        params_list = SyntaxTreeNode('StateParameterList')
        func_tree.add_child_node(params_list, func_tree.root)

        while self.look().value != ')':
            if self.look().value in keywords[DATA]:
                param = SyntaxTreeNode('Parameter')
                func_tree.add_child_node(param, params_list)
                func_tree.add_child_node(SyntaxTreeNode(self.look().value, 'DATA_TYPE',
                                                                  {'type': self.look().value}), param)
                self.index += 1
                if self.look().type == 'IDENTIFIER':
                    func_tree.add_child_node(SyntaxTreeNode(self.look().value, 'IDENTIFIER',
                                                                      {'type': 'VARIABLE',
                                                                       'variable_type': self.look().value}), param)
                    self.index += 1
                    if self.look().value == ',':
                        self.index += 1
                else:
                    self.error(self.look())
            else:
                self.error(self.look())
        self.match(')')
        if self.look().value == ';':
            self.index += 1
        elif self.look() == '{':
            self._block()
        else:
            self.error(self.look())

    def _statement(self, father=None):
        # not allow this condition: int c,b=1; the symbol behind of the expression must be ';'.
        variable_type = self.look().type
        self.index += 1
        while self.look().value != ';':
            variant = self.look()
            if variant.type == 'IDENTIFIER':
                statement_tree = self._abstract_tree('Statement', father)
                if self.look(1).value in [',', ';']:
                    statement_tree.add_child_node(SyntaxTreeNode(variant.value, variable_type, 'variant'))
                    self.index += 1
                elif self.look(1).value == '[':
                    self._expression(statement_tree.root)
                elif self.look(1).value == '=':
                    self._assignment(statement_tree.root)
                    break
                else:
                    self.error(self.look(1))
            else:
                self.match(',')
        else:
            self.match(';')

    def _assignment(self, father=None):
        # end this sentence
        assign_tree = self._abstract_tree('assignment', father)
        
        while self.look().value != ';':
            token = self.look()
            if token.type == 'IDENTIFIER':
                look1 = self.look(1)
                if look1.value == '=':
                    assign_tree.add_child_node(SyntaxTreeNode(self.look().value, 'IDENTIFIER', 'variant'))
                    self.index += 1
                elif look1.value == '[':
                    self._expression(assign_tree.root)
                else:
                    self.error(look1)
            elif token.value == '=':
                self.index += 1
                self._expression(assign_tree.root)
        self.match(';')
        
    def _expression(self, father=None):
        token_list = self._suffix_expr()
        #for t in token_list:
         #   print(t.row, t.type, t.value)
        node_list = []
        for token in token_list:
            if token.type in ['DIGIT_CONSTANT', 'IDENTIFIER']:
                node = SyntaxTreeNode(token.value, token.type)
                node_list.append(node)
            else:
                tree = SyntaxTree()
                if token.value == '[':
                    tree.current = tree.root = SyntaxTreeNode('[]')
                    if node_list[-2]:
                        node_list[-2].set_extra_info('array_name')
                else:
                    tree.current = tree.root = SyntaxTreeNode(token.value)
                    if node_list[-2] and node_list[-2].type == 'IDENTIFIER':
                        node_list[-2].set_extra_info('variant_name')
                tree.add_child_node(node_list[-2])
                tree.add_child_node(node_list[-1])
                node_list.pop()
                node_list.pop()
                node_list.append(tree.root)

        if len(node_list) == 1:
            expr_tree = self._abstract_tree('expression', father)
            expr_tree.add_child_node(node_list[0])
        else:
            self.error(self.look())

    def _suffix_expr(self):
        # viewed the array as a expression, '[' as a operator
        # not end this sentence because it is a expr
        priority = {'@': -1, '(': -1, ')': -1, ']': '-1', '>': 0, '<': 0, '>=': 0, '<=': 0,
                    '+': 1, '-': 1, '*': 2, '/': 2, '++': 3, '--': 3, '!': 3, '[': 4}

        low_token = Token(0, SEP_INDEX, '@')
        # "(" replease "["
        re_token = Token(0, SEP_INDEX, '(')
        operator_stack = [low_token]
        want = []
        while self.look().value not in [';', '=']:
            token = self.look()
            if token.type in ['DIGIT_CONSTANT', 'IDENTIFIER']:
                want.append(token)
            elif token.value in priority and token.value != '@':
                if token.value == '(':
                    operator_stack.append(token)
                elif token.value in [')', ']']:
                    while operator_stack[-1].value != '(':
                        want.append(operator_stack.pop())
                    operator_stack.pop()
                else:
                    while priority[token.value] <= priority[operator_stack[-1].value]:
                        want.append(operator_stack.pop())
                    operator_stack.append(token)
                    if token.value == '[':
                        operator_stack.append(re_token)
            else:
                self.error(token)
            self.index += 1

        while operator_stack[-1].value != '@':
            want.append(operator_stack.pop())
        return want

    def _abstract_tree(self, root_name, father=None):
        if not father:
            father = self.tree.root
        tree = SyntaxTree()
        tree.current = tree.root = SyntaxTreeNode(root_name)
        self.tree.add_child_node(tree.root, father)
        return tree

# DFS遍历语法树
    def display(self, node, i=0):
        if not node:
            return
        print('{}{}{}'.format(node.value, '('+node.type if node.type is not None else '',
                              '[])' if node.extra_info == 'array' is not None else ''))
        child = node.first_son
        if child:
            print('-'*(4+i), end=' ')
            self.display(child, i+4)
        right = node.right
        if right:
            print('-'*i, end=' ')
            self.display(right, i)


if __name__ == '__main__':
    parser = Parser()
    parser.display(parser.tree.root)



