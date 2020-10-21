%option noyywrap
%option header-file="lex.yy.h"
%{
#include <iostream>

#define YY_DECL int yylex()
%}
%%
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



{delim} {}

"/*" {
	char c;
	while(1){	
		while(c=input() != '*');
		if(c=input() == '/')
			break;		
	}
}

"//" {
	char c;
	while((c = input()) != '\n');
}

{reservedWord} {
	fprintf(yyout, "%s\n", yytext);
}


{integer} {
	fprintf(yyout, "T_INTLITERAL %s\n", yytext);
}

{doubleSign} {
	fprintf(yyout, "%s\n", yytext);
}

{sign} {
	fprintf(yyout,"%s\n", yytext);
}

{double} {
	fprintf(yyout, "T_DOUBLELITERAL %s\n", yytext);
}

{string} {
	fprintf(yyout, "T_STRINGLITERAL %s\n", yytext);
}

{boolVal} {
	fprintf(yyout, "T_BOOLEANLITERAL %s\n", yytext );
}
{id} {
	fprintf(yyout, "T_ID %s\n", yytext);
}

%%
