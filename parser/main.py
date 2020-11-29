import sys, getopt
def main(argv):
    inputfile = ''
    outputfile = ''
    try:
        opts, args = getopt.getopt(argv,"hi:o:",["ifile=","ofile="])
    except getopt.GetoptError:
        print ('main.py -i <inputfile> -o <outputfile>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print ('test.py -i <inputfile> -o <outputfile>')
            sys.exit()
        elif opt in ("-i", "--ifile"):
            inputfile = arg
        elif opt in ("-o", "--ofile"):
            outputfile = arg
    with open("tests/" + inputfile, "r") as input_file:
        passed = True
        test = input_file.read()
        try:
            from src.parser import decaf_parser
            decaf_parser.parse(test)
        except:
            passed = False
        pass

    with open("out/" + outputfile, "w") as output_file:
        output_file.write("OK" if passed else "Syntax Error")

if __name__ == "__main__":
    main(sys.argv[1:])
