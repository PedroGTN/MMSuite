import os
import sys

comando = ''
for i in sys.argv[1:]:
    comando += i + ' '
    
os.system(comando)