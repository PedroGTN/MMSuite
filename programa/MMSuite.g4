grammar MMSuite;

NUMINT
	:	('0'..'9')+
	;

NUMREAL
	:	('0'..'9')+ ('.' ('0'..'9')+)?
	;
	
VARIAVEL
	:	('a'..'z'|'A'..'Z') ('a'..'z'|'A'..'Z'|'0'..'9' | '_')*
	;

CADEIA
	:	'\'' ( ESC_SEQ | ~('\''|'\\') )* '\''
	;
	
OP_ARIT1
	:	'+' | '-'
	;

OP_ARIT2
	:	'*' | '/'
	;

OP_REL
	:	'>' | '>=' | '<' | '<=' | '<>' | '=='
	;

OP_BOOL	
	:	'and' | 'or'
	;

fragment
ESC_SEQ	: '\\\'';
COMENTARIO
    :   '#' ~('\n')* -> skip
    ;

WS  :   ( ' '
        | '\t'
        | '\r'
        | '\n'
        ) -> skip
    ;

funcao
	:   decfuncao (comandos)* return?
	;

importing
	:	'import' CADEIA
	;

func_importing
	:	'from' CADEIA 'import' CADEIA
	;

imports
	:	(importing|func_importing)*
	;

programa
	:	imports (funcao)* EOF
	;

parametros 
	: VARIAVEL (',' VARIAVEL)*
	;

decfuncao
	:	'func' VARIAVEL '(' parametros? ')'
    ;

python
	: 'python' '(' cadeiacomposta ')'
	;

valores
    : (NUMINT | NUMREAL | VARIAVEL'(' parametros ')' | cadeiacomposta)
    ;

declaracao
	:	VARIAVEL '=' valores
	;
	
	
expressaoAritmetica
	:	expressaoAritmetica OP_ARIT1 termoAritmetico
	|	termoAritmetico
	;
	
termoAritmetico
	:	termoAritmetico OP_ARIT2 fatorAritmetico
	|	fatorAritmetico
	;
	
fatorAritmetico
	:	NUMINT
	|	NUMREAL
	|	VARIAVEL
	|	'(' expressaoAritmetica ')'
	;
	
expressaoRelacional
	:	expressaoRelacional OP_BOOL termoRelacional
	|	termoRelacional
	;
	
termoRelacional
	:	expressaoAritmetica OP_REL expressaoAritmetica
	|	'(' expressaoRelacional ')'
	;
	
cadeiacomposta
	:    (CADEIA | VARIAVEL) ('+' (CADEIA|VARIAVEL))*
	;

return
	:	'return' VARIAVEL
	;

comandos
	:	declaracao
	|	comandoCondicao
	|	comandoRepeticao
	|   ( VARIAVEL '(' parametros ')' )
	|   python
	;
	
comandoCondicao
	:	'if' expressaoRelacional '{' comandos '}'
	|	'if' expressaoRelacional '{' comandos '}' 'else' '{' comandos '}'
	;
	
comandoRepeticao
	:	'while' expressaoRelacional '{' comandos '}'
	;

