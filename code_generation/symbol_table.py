class SymbolTable:
    def __init__(self):
        self.stack = []

    def push_scope(self, scope):
        self.stack.append(scope)

    def pop_scope(self):
        return self.stack.pop()

    def push_symbol(self, symbol):
        cur_scope = self.stack[len(self.stack) - 1]
        cur_scope.variables.append(symbol)

    def lookup_symbol(self, name):
        cur_scope = self.stack[len(self.stack) - 1]
        while cur_scope:
            for symbol in cur_scope.symbols:
                if symbol.name == name:
                    return symbol.value
            cur_scope = cur_scope.parent_scope
        raise Exception(
            'SymbolTable Error:symbol does not exist in symbolTable.')


class Symbol:
    def __init__(self, name, value):
        self.name = name
        self.val = value
        self.scope = None


class Scope:
    def __init__(self, name, parent_scope):
        self.name = name
        self.parent_scope = parent_scope
        self.symbols = []
