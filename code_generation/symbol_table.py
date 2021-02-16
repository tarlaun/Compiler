from lark.visitors import Interpreter
from parser_code import get_parse_tree
from Error import *

class SymbolTable():
    def __init__(self):
        super().__init__()
        self.stack = []
        self.functions = []
        self.classes = []

    def push_scope(self, scope):
        self.stack.append(scope)

    def pop_scope(self):
        return self.stack.pop()

    def get_current_scope(self):
        return self.stack[-1]

    def push_symbol(self, symbol):
        cur_scope = self.stack[len(self.stack) - 1]
        symbol.set_scope(cur_scope)
        cur_scope.symbols.append(symbol)

    def lookup_symbol(self, name):
        cur_scope = self.get_current_scope()
        search_stack = [cur_scope]
        while(len(search_stack) != 0):
            scope = search_stack.pop()
            for symbol in scope.symbols:
                if symbol.name == name:
                    return symbol
            for parent in scope.parent_scopes:
                search_stack.append(parent)
        raise SymbolTableError(
            'SymbolTable Error: symbol does not exist in symbolTable.')

    def push_function(self, function):
        self.functions.append(function)

    def lookup_function(self, name):
        for f in self.functions:
            if f.name == name:
                return f
        raise Exception(
            'SymbolTable Error: function does not exist in symbolTable.')

    def push_class(self, class_obj):
        self.classes.append(class_obj)

    def lookup_class(self, name):
        for c in self.classes:
            if c.name == name:
                return c
        raise ClassError(
            'SymbolTable Error: class does not exist in symbolTable.')


class Symbol:
    def __init__(self, name, type, value=None, scope=None, label=None):
        self.name = name
        self.type = type
        self.value = value
        self.scope = scope
        self.label = label
        if(scope):
            scope.add_symbol(self)

    def set_value(self, value):
        self.value = value

    def set_scope(self, scope):
        self.scope = scope
        scope.add_symbol(self)

    def set_label(self, label):
        self.label = label


class Scope:
    def __init__(self, name, parent_scope=None):
        self.name = name
        self.parent_scopes = []
        self.parent_scopes.append(parent_scope)
        self.symbols = []

    def add_symbol(self, symbol):
        self.symbols.append(symbol)

    def add_parent_scope(self, parent):
        self.parent_scopes.append(parent)

    def get_id(self):
        id = self.name
        parent = self.parent_scopes[0]
        while parent:
            id += ('__' + parent.name)
            parent = parent.parent_scopes[0]
        return id

    def __str__(self):
        return self.get_id()


class Function:
    def __init__(self, scope, name, return_type=None, label=None , func_formals = None):
        self.scope = scope
        self.name = name
        self.return_type = return_type
        self.label = label
        self.func_formals = func_formals


class Class:
    def __init__(self, scope, name, label=None , variables = [] , functions = []):
        self.scope = scope
        self.name = name
        self.label = label
        self.variables = variables
        self.functions = functions

    def get_func_index(self , name):
        i = 0
        for x in self.functions:
            if x.name == name:
                return i
            i = i + 1
        return -1
    
    def get_function(self , name) :
        index = self.get_func_index(name)
        if index == -1:
            raise SymbolTableError('invalid function for class')
        return self.functions[index]

    def get_var_index(self, name):
        i = 0
        for x in self.variables:
            if x.name == name:
                return i
            i = i + 1
        return -1
    
    def get_variable(self , name):
        index = self.get_var_index(name)
        if index == -1:
            raise SymbolTableError('invalid variable for class')
        return self.variables[index]

    def set_label(self, label):
        self.label = label

