import sys
import getopt
from parser_code import get_parse_tree
from cgen import Cgen


def main(argv):
    inputfile = ''
    outputfile = ''
    try:
        opts, args = getopt.getopt(argv, "hi:o:", ["ifile=", "ofile="])
    except getopt.GetoptError:
        print('main.py -i <inputfile> -o <outputfile>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('test.py -i <inputfile> -o <outputfile>')
            sys.exit()
        elif opt in ("-i", "--ifile"):
            inputfile = arg
        elif opt in ("-o", "--ofile"):
            outputfile = arg

    with open("tests/" + inputfile, "r") as input_file:
        code = input_file.read()
        parse_tree = get_parse_tree(code)

    with open("out/" + outputfile, "w") as output_file:
        sys.stdout = output_file
        output_code = Cgen().visit(parse_tree)
        output_file.write(output_code)
        sys.stdout.close()


if __name__ == "__main__":
    main(sys.argv[1:])
