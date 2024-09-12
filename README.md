# Media Manipulation Suite

Esta é uma linguagem que busca dar ao usuário a possibilidade de criar uma caixa de ferramentas de manipulação de midias por meio de um interpretador no console.  

Toda função que o usuário cria é enviada para a biblioteca padrão da linguagem, para poder ser usada individualmente ou para que possa integrar outras funções de forma que se possa realizar manipulações muito complexas.  

Para fazer uso da linguagem basta que se escreva um arquivo com a extensão _.mms_ que contenha a declaração de uma função e seu comportamento, depois pode-se rodar a função criada com `python3 ../programa/MMSuite.py nova_func.mms` ou adicionar a função à bilbioteca padrão com `python3 ../programa/MMSuite.py add nova_func.mms`. Caso a função desejada já esteja na biblioteca padrão, pode-se inicar a linguagem no modo console com `python3 ../programa/MMSuite.py` e invocar diretamente as funções desejadas.  

Um exemplo de programa .mms pode ser observado a seguir:  
```
func yt2gif(link, t_init, t_dur)
nome_vid = dlyt(link)
nome_vid_armd = '"' + nome_vid + '"'
novo_nome = 'video.webm'
mv(nome_vid_armd, novo_nome)
cutvid(novo_nome, t_init, t_dur)
nome_final = 'video.webm_cut.webm'
vid2gif(nome_final)
```  

A função sendo criada se chama `yt2gif()` e ela faz uso das funções `dlyt()` para baixar os videos, `mv()` para renomar o arquivo baixado, `cutvid()` para cortar o video no momento desejado e `vid2gif()` para poder transformá-lo em um arquivo .gif.  

Toda funcao criada e adicionada a biblioteca padrao tem seu nome salvo em `funcloc.mmlib`.  

## Para Rodar a Linguagem

Baixe o ffmpeg com:  
```
sudo apt install ffmpeg
```

Baixe as dependências do python com:  
```
pip install requirements.txt
```

Faça a build do ANTLR com:  
```
bash build.sh
```

---

Para rodar o programa no modo console usa-se:  
```
python3 MMSuite.py 
```

Para rodar uma função da linguagem usa-se:  
```
python3 MMSuite.py [funcao] [args]
```

O comando `add` é usado para adicionar funções à biblioteca MMSuite:  
```
python3 MMSuite.py add [caminho/para/comando.mms]
```

O comando `del` é usado para remover funções da biblioteca MMSuite:  
```
python3 MMSuite.py del [nome da funcao]
```

## Testes
Existem duas pastas de testes que ajudam a demonstrar que a linguagem funciona, elas são `test_sucesso` e `teste_falha`. Dentro delas existe estão todas as funções usadas em testes da nossa linguagem, o arquivo `testes.md` descreve o que epsperar em cada teste e provê os comandos necessários para aferir por si mesmo.  