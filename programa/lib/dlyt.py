import os
import sys
from execute_func import mms_exec


link = sys.argv[1]
args = 'yt-dlp ' + link 
retorno = mms_exec("python3 lib/exec.py " + args , 0)

lines = retorno.split('\n')
saida = ''

for l in lines:
    if l[:8] == '[Merger]':
        saida = l

saida = saida.split('\"')[-2]
saida2 = saida.replace(' ', '_')

for i in range(len(saida2)):
    if saida2[i] > '~':
        saida2.replace(saida2[i], '_')
        i-=1

os.rename(saida, saida2)

print(saida2)
