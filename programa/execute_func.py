import subprocess

def shell_exec(args, format='0'):
    """
    Funcao usada para poder termos retornos dentro da fase de interpretação

        Args:
        Param1 (Str Array): Argumentos do programa a ser executado
        Param2 (Str): Tipo de formatação necessario para o retorno

        Return:
        Param1 (Any): Tipo definido pelo Param2, stdout do programa que foi executado
    """
    process = subprocess.run(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    saida = process.stdout.decode('utf-8')[:-1]
    erro = process.stderr.decode('utf-8')

    if format == '1':
        saida = str(saida)
    if format == '0':
        saida = '0'
    else :
        saida = str(saida)

    return saida


def mms_exec(args:str, format='0'):
    """
    Funcao usada para poder termos retornos dentro da fase de interpretação

        Args:
        Param1 (Str Array): Argumentos do programa a ser executado
        Param2 (Str): Tipo de formatação necessario para o retorno

        Return:
        Param1 (Any): Tipo definido pelo Param2, stdout do programa que foi executado
    """
    process = subprocess.run(args.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    saida = process.stdout.decode('utf-8')[:-1]
    erro = process.stderr.decode('utf-8')

    # print(saida, erro)


    if format == '1':
        saida = str(saida)
    if format == '0':
        saida = '0'
    else :
        saida = str(saida)

    return saida