from lark.visitors import Interpreter
from parser import get_parse_tree


class Cgen(Interpreter):
    def start(self, tree):
        print('#### start the code generation')
        next = tree.children[0]
        self.visit(next)

    def if_stmt(self, tree):
        return None

    def for_stmt(self, tree):
        return None


code = """
int main() {
    if(a){
        Print(a);
    }
}

"""
if __name__ == '__main__':
    tree = get_parse_tree(code)
    print(tree)
    Cgen().visit(tree)
