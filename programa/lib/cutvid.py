import os
import sys
from execute_func import mms_exec


vid = sys.argv[1]
t_init = sys.argv[2]
t_dur = sys.argv[3]
args = 'ffmpeg -i "' + vid + '" -ss ' + t_init + ' -t ' + t_dur + ' "' + vid + '_cut.webm"' 
mms_exec("python3 lib/exec.py " +  args , 0)
