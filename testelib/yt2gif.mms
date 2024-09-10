func yt2gif(link, t_init, t_dur)
nome_vid = dlyt(link)
nome_vid_armd = '"' + nome_vid + '"'
novo_nome = 'videofoda.webm'
mv(nome_vid_armd, novo_nome)
cutvid(novo_nome, t_init, t_dur)
nome_final = 'videofoda.webm_cut.webm'
vid2gif(nome_final)