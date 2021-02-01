from parser import get_parse_tree


def if_cgen():
    return None


def for_cgen():
    return None


def while_cgen():
    return None


def function_cgen():
    return None


def statement_cgen():
    return None


def class_cgen():
    return None


def cgen(code):
    parse_tree = get_parse_tree(code)
    print('Parse Tree#############')
    print(parse_tree)
    print('#######################')


test_code = 'int a;'

if __name__ == '__main__':
    cgen(test_code)
