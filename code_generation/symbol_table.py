from lark.visitors import Interpreter
from parser import get_parse_tree


class SymbolTable(Interpreter):
    def __init__(self):
        super().__init__()
        self.stack = []

    def push_scope(self, scope):
        self.stack.append(scope)

    def pop_scope(self):
        return self.stack.pop()

    def get_current_scope(self):
        return self.stack[-1]

    def push_symbol(self, symbol):
        cur_scope = self.stack[len(self.stack) - 1]
        cur_scope.symbols.append(symbol)

    def lookup_symbol(self, name):
        cur_scope = self.stack[len(self.stack) - 1]
        while cur_scope:
            for symbol in cur_scope.symbols:
                if symbol.name == name:
                    return symbol.value
            cur_scope = cur_scope.parent_scope
        raise Exception(
            'SymbolTable Error:symbol does not exist in symbolTable.')

    def start(self, tree):
        root = Scope('root')
        self.push_scope(root)
        self.visit_children(tree)

    def declaration(self, tree):
        for node in tree.children:
            if node.data in ['variable_declaration', 'function_declaration', 'class_declaration']:
                self.visit(node)

    def variable_declaration(self, tree):
        variable = tree.children[0]
        self.visit(variable)

    def variable(self, tree):
        print('variable')
        current_scope = self.get_current_scope()
        type = tree.children[0]
        name = tree.children[1].value
        variable = Symbol(name=name, type=type, value=None,
                          scope=current_scope)
        tree._meta = variable
        self.visit(type)

    def function_declaration(self, tree):
        print('function_declaration')

        self.visit_children(tree)

    def class_declaration(self, tree):
        print('class_declaration')
        self.visit_children(tree)


class Symbol:
    def __init__(self, name, type, value, scope):
        self.name = name
        self.type = type
        self.value = value
        self.scope = scope
        scope.add_symbol(self)


class Scope:
    def __init__(self, name, parent_scope=None):
        self.name = name
        self.parent_scope = parent_scope
        self.symbols = []

    def add_symbol(self, symbol):
        self.symbols.append(symbol)


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
"""


if __name__ == '__main__':
    tree = get_parse_tree(if_test_code)
    print(tree)
    print(tree.pretty())
    SymbolTable().visit(tree)


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
