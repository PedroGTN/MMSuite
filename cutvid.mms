func cutvid(vid, t_init, t_dur)
args = 'ffmpeg -i "' + vid + '" -ss '
 + t_init + ' -t ' + t_dur + ' "' + 
 vid + '_cut.webm"'
exec(args)