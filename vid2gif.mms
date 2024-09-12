func vid2gif(vid)
args = 'ffmpeg -i "' + vid + '
" -vf "fps=10,scale=320:-1:flags=lanczos,split[s0][s1];[s0]palettegen[p];[s1][p]paletteuse"
 -loop 0 ' + '"' + vid + '.gif"'
exec(args)