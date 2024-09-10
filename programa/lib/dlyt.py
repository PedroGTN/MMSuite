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

print(saida)
