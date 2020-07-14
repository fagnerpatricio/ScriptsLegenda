import os
import natsort
import re
import shutil

dir_trabalho = '/home/fagner/Vídeos/Shows/'

arq_dir_trabalho = os.listdir(dir_trabalho)
arq_dir_trabalho = natsort.natsorted(arq_dir_trabalho, reverse=False)

contador = 1
for a in arq_dir_trabalho:
    shutil.move(dir_trabalho + a, dir_trabalho + "Episode S01E" + str(contador).zfill(2) + ".ptBR.ass")
    contador = contador + 1
