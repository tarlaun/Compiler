import lark
from lark.visitors import Interpreter
from parser_code import get_parse_tree
from symbol_table import SymbolTable
from mips import *


# Typechecking... might move to a different file later.
class Type:
    double = "double"
    int = "int"
    bool = "bool"
    string = "string"
    array = "array"
    null = "null"


def is_primitive(type):
    return type in [Type.double, Type.string, Type.int, Type.bool]


def is_array(type):
    return not isinstance(type, str)


def convertible(type1, type2):  # type1 (Derived), type2 (Base)
    if is_primitive(type1) or is_primitive(type2):
        return type1 == type2

    if is_array(type1) or is_array(type2):
        return type1 == type2


class Cgen(Interpreter):
    label_counter = 0

    def count_label(self):
        self.label_counter += 1
        return self.label_counter

    def __init__(self):
        super().__init__()
        self.current_scope = None
        self.loop_labels = []
        self._types = []
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
            code += ' not main func '  # just for testing... its BS
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

    def IDENTIFIER(self, tree):
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
        print("#### EXPR")
        return ''.join(self.visit_children(tree))

    def expr0(self, tree):
        return ''.join(self.visit_children(tree))

    def expr1(self, tree):
        return ''.join(self.visit_children(tree))

    def expr2(self, tree):
        return ''.join(self.visit_children(tree))

    def expr3(self, tree):
        return ''.join(self.visit_children(tree))

    def expr4(self, tree):
        return ''.join(self.visit_children(tree))

    def expr5(self, tree):
        return ''.join(self.visit_children(tree))

    def expr6(self, tree):
        return ''.join(self.visit_children(tree))

    def expr7(self, tree):
        code = ''
        more_code = self.visit_children(tree)
        if len(more_code) == 0:
            return code
        return ''.join(more_code)

    def assignment(self, tree):
        print("#### ASS")
        code = ''.join(self.visit_children(tree))
        ''' typ = self._types[-1]
        if typ.name == 'double' and typ.dimension == 0:
            code += '.text\n'
            code += '\tlw $t0, 8($sp)\n'
            code += '\tl.d $f0, 0($sp)\n'
            code += '\ts.d $f0, 0($t0)\n'
            code += '\ts.d $f0, 8($sp)\n'
            code += '\taddi $sp, $sp, 8\n\n'
        else:
            code += '.text\n'
            code += '\tlw $t0, 8($sp)\n'
            code += '\tlw $t1, 0($sp)\n'
            code += '\tsw $t1, 0($t0)\n'
            code += '\tsw $t1, 8($sp)\n'
            code += '\taddi $sp, $sp, 8\n\n'
        self._types.pop()'''
        return code

    def var_addr(self, tree):
        var_scope = self.current_scope
        var_name = tree.children[0].value
        return 'var_addr'

    def var_access(self, tree):
        return 'var_access'

    def val(self, tree):
        print("#### val code gen")
        print(len(tree.children))
        code = ''.join(self.visit_children(tree))
        '''typ = self._types[-1]
        if typ.name == 'double' and typ.dimension == 0:
            code += '.text\n'
            code += '\tlw $t0, 0($sp)\n'
            code += '\tl.d $f0, 0($t0)\n'
            code += '\ts.d $f0, 0($sp)\n\n'
        else:
            code += '.text\n'
            code += '\tlw $t0, 0($sp)\n'
            code += '\tlw $t0, 0($t0)\n'
            code += '\tsw $t0, 0($sp)\n\n' '''
        return code

    def l_value(self, tree):
        print('#### start l-value')
        print(tree.children[0])
        return 'l_value'

    def const_int(self, tree):
        code = ''
        # code += '.text'
        const_val = tree.children[0].value.lower()
        code += mips_li('$t0', const_val)
        code += sub_stack(8)
        code += mips_store('$t0', '$sp')
        self._types.append(Type.int)
        return code

    def const_bool(self, tree):
        code = ''
        # code += '.text'
        const_val = tree.children[0].value.lower()
        numerical_val = 0
        if const_val == 'true':
            numerical_val = 1
        code += mips_li('$t0', numerical_val)
        code += sub_stack(8)
        code += mips_store('$t0', '$sp')
        self._types.append(Type.bool)
        return code

    def const_string(self, tree):
        return 'const_string'

    def null(self, tree):
        return 'NULL'

    def mul(self, tree):
        return 'MUL'

    def mod(self, tree):
        return 'MOD'

    def div(self, tree):
        return 'DIV'

    def add(self, tree):
        return 'ADD'

    def sub(self, tree):
        return 'SUB'

    def eq(self, tree):
        return 'eq'

    def gt(self, tree):
        return 'gt'

    def ge(self, tree):
        return 'ge'

    def lt(self, tree):
        return 'lt'

    def le(self, tree):
        return 'le'

    def neg(self, tree):
        return 'neg'

    def not_exprs(self, tree):
        return 'NOT_EXPRS'

    def actuals(self, tree):
        return 'actuals'

    def method(self, tree):
        return 'METH'

    def call(self, tree):
        return 'CALL'

    def subscript(self, tree):
        return 'subs_ '

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
bool main(){
bool fuck;
fuck = true;
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

'''  def expr(self, tree):
        print('#### start expr')
        self.visit_children(tree)
        print(tree.children)
        return 'expression' '''
