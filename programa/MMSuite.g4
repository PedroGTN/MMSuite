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

RETURN
	: 'return'
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
	:   decfuncao (comandos)* ('return' '(' parametros? ')')?
	;

programa
	:	(funcao)* EOF
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
    : (NUMINT | NUMREAL | CADEIA | VARIAVEL)
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

comandos
	:	declaracao
	|	comandoCondicao
	|	comandoRepeticao
	|   VARIAVEL
	|   RETURN
	|   python
	;
	
comandoCondicao
	:	'if' expressaoRelacional '{' comandos '}'
	|	'if' expressaoRelacional '{' comandos '}' 'else' '{' comandos '}'
	;
	
comandoRepeticao
	:	'while' expressaoRelacional '{' comandos '}'
	;

