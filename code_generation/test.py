from lark.visitors import Interpreter
from parser import get_parse_tree


class IncreaseSomeOfTheNumbers(Interpreter):
    def start(self, tree):
        print('start')

    def number(self, tree):
        print('number function')
        tree.children[0] += 1

    def skip(self, tree):
        print('skip function')
        # skip this subtree. don't change any number node inside it.
        pass


code = """
int[][][] c;
int d;
class Ostad extends Emp{
    void daneshjoo(){
    }
}
class Person{
    double name;
    int a;
    string l;
    int mmd(){
        int c;
    }
}

class Emp extends Person {
    int lks;
    int fight(){}
    int mmd(){}
} 
void cal(int number, double mmd) {
    int c;
    {
        int d;
    }
    c = number;
}
double stone(){
    double f;
}
int main() {
    int a;
    int b;

    a = ReadInteger();
    b = ReadInteger();

    if(a){
        Print(a);
    }

    Print(a);
    Print(b);
}

"""
if __name__ == '__main__':
    tree = get_parse_tree(code)
    print(tree)
    IncreaseSomeOfTheNumbers().visit(tree)
