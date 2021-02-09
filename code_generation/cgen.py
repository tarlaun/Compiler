import lark
from lark.visitors import Interpreter
from parser_code import get_parse_tree
from symbol_table import SymbolTable
import mips


class Cgen(Interpreter):
    label_counter = 0

    def count_label(self):
        self.label_counter += 1
        return self.label_counter

    def __init__(self):
        super().__init__()
        self.loop_labels = []
        self.symbol_table = SymbolTable()

    def start(self, tree):
        code = ''
        print('#### start the code generation')

        self.symbol_table.visit(tree)

        code += ''.join(self.visit_children(tree))
        return code

    def declaration(self, tree):
        code = ''
        for decl in tree.children:
            code += self.visit(decl)
        return code

    def function_declaration(self, tree):
        code = ''
        function = tree._meta
        self.symbol_table.push_scope(function.scope)
        if len(tree.children) == 4:
            ident = tree.children[1]
            formals = tree.children[2]
            stmt_block = tree.children[3]
        else:
            ident = tree.children[0]
            formals = tree.children[1]
            stmt_block = tree.children[2]
        code += self.visit(tree.children[0])
        code += self.visit(formals)
        code += self.visit(stmt_block)
        if ident == 'main':
            code += 'main func'
        else:
            code += mips.mips_semantic_error()  # just for testing... its BS
        self.symbol_table.pop_scope()
        return code

    def variable_declaration(self, tree):
        code = ''
        code += ''.join(self.visit_children(tree))
        return 'fucking variable decl'

    def variable(self, tree):
        code = ''
        return 'fucking variable'

    def formals(self, tree):
        # push to stack
        return 'formals'

    def type(self, tree):
        return 'type'

    def IDENT(self, tree):
        return 'ident'

    def stmt_block(self, tree):
        code = ''
        print('#### start stmt')
        child = tree.children[0]
        stmt_label = self.count_label()
        child._meta = stmt_label
        code += self.visit(tree.children[0])
        code += self.visit(tree.children[1])
        return code

    def expr(self, tree):
        print('#### start expr')
        self.visit_children(tree)
        print(tree.children)
        return 'expression'

    def l_value(self, tree):
        print('#### start l-value')
        print(tree.children[0])
        return None

    def stmt(self, tree):
        code = ''
        print('#### start stmt')
        child = tree.children[0]
        stmt_label = self.count_label()
        child._meta = stmt_label
        code += self.visit(child)
        return code

    def if_stmt(self, tree):
        print('### start if_stmt')
        expr = tree.children[0]
        self.visit(expr)
        stmt = tree.children[1]
        self.visit(stmt)
        hasElse = len(tree.children) != 2
        if not hasElse:
            # generate if(expr){stmt;} code
            None
        else:
            else_stmt = tree.children[2]
            self.visit(else_stmt)
            # generate if(expr){stmt;}else{stmt;} code
            None
        return None

    def for_stmt(self, tree):
        print('### start for_stmt')
        for_label = tree._meta
        self.loop_labels.append(for_label)
        expr1 = tree.children[0]
        self.visit(expr1)
        expr2 = tree.children[1]
        self.visit(expr2)
        expr3 = tree.children[2]
        self.visit(expr3)
        # generate for(expr;expr;expr){stmt;} code
        self.loop_labels.pop()
        return None

    def while_stmt(self, tree):
        print('### start while_stmt')
        while_label = tree._meta
        print(while_label)
        self.loop_labels.append(while_label)
        expr = tree.children[0]
        self.visit(expr)
        stmt = tree.children[1]
        self.visit(stmt)
        # generate for(expr;expr;expr){stmt;} code
        self.loop_labels.pop()
        return None


if_test_code = """
int main() {
    int a;
    a = 1;
    if(true){
        int a;
        a = 1;
    }
}
"""
for_test_code = """
int main() {
    int i;
    for(i = 0; i < 10; i = i+1){
        Print(i);
   }
}
"""

while_test_code = """
int main() {
    int i;
    i = 0;
    while (i < 5) {
        Print(i);
        i = i + 1;
    }
}
"""

shit_test_code = '''
int fucker(){
int fuck;
fuck = 12;
}
'''

if __name__ == '__main__':
    tree = get_parse_tree(shit_test_code)
    # print(tree)
    print(tree.pretty())
    code = ''
    code += str(Cgen().visit(tree))
    print("CODE:")
    print(code)
