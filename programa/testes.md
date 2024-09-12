## Testes léxicos/sintáticos:
**Teste 01**:  
- Codigo test_cut_vid.mms nao tem virgulas entre os argumentos
  - `python3 ../programa/MMSuite.py add test_cut_vid.mms`
- Falha no ANTLR!
```
line 2:11 mismatched input '0' expecting ')'
Erros de sintaxe
```


**Teste 02**:
- Codigo test_exec.mms nao fechou parenteses
  - `python3 ../programa/MMSuite.py add test_exec.mms`
- Falha no ANTLR!
```
line 3:47 missing ')' at '<EOF>'
Erros de sintaxe
```

**Teste 03**:
- Codigo return_no_return.mms nao tem valor de retorno apos o termo retorno 
  - `python3 ../programa/MMSuite.py add return_no_return.mms`

- Falha no ANTLR!
```
line 2:32 missing VARIAVEL at '<EOF>'
Erros de sintaxe
```

## Testes semânticos:  

**Teste 04**:  
- Chamou funcao que nao existe  
  - `python3 ../programa/MMSuite.py add func_que_nao_existe.mms`  
```
"Função desconhecida sendo executada "del" na linha 2"
"Compilação abortada"
```


**Teste 05**:  
- Usou variavel que nao existe  
  - `python3 ../programa/MMSuite.py add var_que_nao_existe.mms`  
```  
"Função ou variável não declarada anteriormente tentando ser usada"
"var2 encontrado na linha 2"
"Compilação abortada"
```  

**Teste 06**:  
- Numero errado de argumentos  
  - `python3 ../programa/MMSuite.py add num_errado_args.mms
`  
```
"Número errado de argumentos usados na chamada da função "cutvid" na linha 2"
"Compilação abortada"
```
