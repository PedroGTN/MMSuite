import os
import sys
from pathlib import Path

dir = Path().resolve()
comando1 = str(dir) + '/' + sys.argv[1]
print(comando1)
comando2 = str(dir) + '/' + sys.argv[2]
print(comando2)

Path(comando1).rename(comando2)