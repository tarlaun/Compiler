#include <iostream>
#include <fstream>
#include <vector>
#include <string>
#include lex.yy.h

using namespace std ;
extern FILE *yyin,*yyout;

int main(int argc, char* argv[]){
    if (argc < 5 ){
        cerr<< "Usage: " << argv[0] << " -i <input> -o <output>" << endl ;
        return 1;
    }

    string input_file_path = argv[2];
    string output_file_path = argv[4];

    ofstream output_file(output_file_path) ;
    ifstream input_file
    fprintf(yyout);
    yyin = fopen(input_file_path, "r");
    yyout = fopen(output_file_path, "w");
    

}
