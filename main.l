%{
#undef yywrap
#define yywrap() 1
#include <stdio.h>

%}

delim [ \t\n\s\r]
whiteSpace {delim}+

boolVal true|false
reservedWord void|int|double|bool|string|class|interface|null|this|extends|implements|for|while|if|else|return|break|continue|new|NewArray|Print|ReadInteger|ReadLine|dtoi|itod|btoi|itob|private|protected|public
letter [A-Za-z]
digit [0-9]
id {letter}({letter}|_|{digit})*
string \".*\"
decimalInteger {digit}+
hexInteger 0(x|X)[0-9a-fA-F]+
integer {hexInteger}|{decimalInteger}
doubleSign ==|!=|<=|>=|!=|(\&\&)|(\|\|)
sign [+\-\*/\%<>={\|\|}\!;,\.\[\]\(\)]
simpleDouble {digit}+\.{digit}*
scientificDouble {simpleDouble}(e|E)(\+|-)?{decimalInteger}
double {simpleDouble}|{scientificDouble}


%%

{delim} {

}

"/*" {
	char c;
	while(1){	
		while(c=input()!='*');
		if(c=input()=='/')
			break;		
	}
}

"//" {
	char c;
	while((c = input()) != '\n');
}

{reservedWord} {
	printf("%s\n",yytext);
}


{integer} {
	printf("T_INTLITERAL %s\n",yytext);
}

{doubleSign} {
	printf( "%s\n", yytext);
}

{sign} {
	printf("%s\n",yytext);
}

{double} {
	printf("T_DOUBLELITERAL %s\n", yytext);
}

{string} {
	printf("T_STRINGLITERAL %s\n",yytext);
}

{boolVal} {
	printf("T_BOOLEANLITERAL %s\n" , yytext);
}
{id} {
	printf("T_ID %s\n",yytext);
}





%%

int main()
{
		yylex();
	return 0;
}