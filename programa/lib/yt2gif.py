import os
import sys
from execute_func import mms_exec


link = sys.argv[1]
t_init = sys.argv[2]
t_dur = sys.argv[3]
nome_vid = mms_exec("python3 lib/dlyt.py " + link + " " , 0)
nome_vid_armd = nome_vid 
novo_nome = 'videogif.webm'
mms_exec("python3 lib/mv.py " +  nome_vid_armd + " " + novo_nome + " " , 0)
mms_exec("python3 lib/cutvid.py " +  novo_nome + " " + t_init + " " + t_dur + " " , 0)
nome_final = 'videogif.webm_cut.webm'
mms_exec("python3 lib/vid2gif.py " +  nome_final + " " , 0)
