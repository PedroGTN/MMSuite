import os
import sys
from execute_func import mms_exec


vid = sys.argv[1]
args = 'ffmpeg -i "' + vid + '" -vf "fps=10,scale=320:-1:flags=lanczos,split[s0][s1];[s0]palettegen[p];[s1][p]paletteuse" -loop 0 ' + '"' + vid + '.gif"' 
mms_exec("python3 lib/exec.py " +  args , 0)
