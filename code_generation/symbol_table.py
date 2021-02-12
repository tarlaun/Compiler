from lark.visitors import Interpreter
from parser_code import get_parse_tree


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
        cur_scope = self.stack[len(self.stack) - 1]
        while cur_scope:
            for symbol in cur_scope.symbols:
                if symbol.name == name:
                    return symbol.value
            cur_scope = cur_scope.parent_scope
        raise Exception(
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
        raise Exception(
            'SymbolTable Error: class does not exist in symbolTable.')


class Symbol:
    def __init__(self, name, type, value=None, scope=None):
        self.name = name
        self.type = type
        self.value = value
        self.scope = scope
        if(scope):
            scope.add_symbol(self)

    def set_value(self, value):
        self.value = value

    def set_scope(self, scope):
        self.scope = scope
        scope.add_symbol(self)


class Scope:
    def __init__(self, name, parent_scope=None):
        self.name = name
        self.parent_scope = parent_scope
        self.symbols = []

    def add_symbol(self, symbol):
        self.symbols.append(symbol)

    def get_id(self):
        id = self.name
        parent = self.parent_scope
        while parent:
            id += ('/' + parent.name)
            parent = parent.parent_scope
        return id

    def __str__(self):
        return self.get_id()
    


class Function:
    def __init__(self, scope, name, return_type=None):
        self.scope = scope
        self.name = name
        self.return_type = return_type
        self.label = None

    def set_label(self, label):
        self.label = label


class Class:
    def __init__(self, scope, name):
        self.scope = scope
        self.name = name


if_test_code = """
int main() {
    int a;
    a = 1;
    if(true){
        int a;
        a = 1;
    }
}

void func2(){

}

void func3(int a){

}
"""


if __name__ == '__main__':
    # tree = get_parse_tree(if_test_code)
    # SymbolTable().visit(tree)
    None

    # if __name__ == '__main__':
    #     # THIS IS JUST FOR TEST
    #     symbol_table = SymbolTable()

    #     # root scope
    #     root = Scope('root')
    #     symbol_table.push_scope(root)

    #     root_symbol = Symbol('root_var', 11)
    #     root_symbol2 = Symbol('shared_var', 22)

    #     symbol_table.push_symbol(root_symbol)
    #     symbol_table.push_symbol(root_symbol2)

    #     print('lookup root_var', symbol_table.lookup_symbol('root_var'))

    #     # another scope
    #     scope1 = Scope('scope1', root)
    #     symbol_table.push_scope(scope1)

    #     scope1_symbol = Symbol('shared_var', 33)
    #     symbol_table.push_symbol(scope1_symbol)
    #     print('lookup shared_var', symbol_table.lookup_symbol('shared_var'))

    #     # another scope
    #     scope2 = Scope('scope2', scope1)

    #     symbol_table.push_scope(scope2)

    #     scope2_symbol = Symbol('scope2_var', 44)
    #     symbol_table.push_symbol(scope2_symbol)
    #     print('lookup scope2_var', symbol_table.lookup_symbol('scope2_var'))
    #     print('lookup shared_var', symbol_table.lookup_symbol('shared_var'))
