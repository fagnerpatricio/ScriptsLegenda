import argparse
import json
import ntpath
import os
import re
import shutil
import sys
import xml.etree.ElementTree as ET

import natsort as natsort
import pysubs2 as pysubs2
import requests
from matplotlib import font_manager
from tabulate import tabulate

CONFIG = json.load(open('/home/fagner/Documentos/ProjetosVSCode/ScriptsLegendas/Scripts/config.json', 'r'))


def dir_bak_leg(dir_trabalho_temp=None, dir_legenda=None):
    # Criando o Diretório onde ficaram as legendas originais da Crunchroll
    try:
        original_umask = os.umask(0)
        os.mkdir(dir_trabalho_temp + CONFIG["dirLegendaAntiga"])
    except OSError:
        print("Falha na cricao do diretorio porque ele ja existe" + dir_trabalho_temp + CONFIG["dirLegendaAntiga"])
    else:
        print("Successfully created the directory %s " + dir_trabalho_temp + CONFIG["dirLegendaAntiga"])
    finally:
        os.umask(original_umask)

    # Move os arquivos de legendas para o diretorio de Backup
    for arquivo_de_legenda in dir_legenda:
        if arquivo_de_legenda.endswith(".ass"):
            try:
                shutil.move(dir_trabalho_temp +'/'+ arquivo_de_legenda, dir_trabalho_temp + CONFIG["dirLegendaAntiga"])
            except OSError:
                print("Arquivo já existe no destino" + arquivo_de_legenda)

def desloca_subs(subs, h=0,m=0,s=0,delta_deslocamento=0):
    s = 32
    tempo_inicial = (h * 3600000) + (m * 60000) + (s * 1000)
    delta_deslocamento = 89999
    for line in subs:
        if line.start > tempo_inicial:
            line.start += delta_deslocamento
            line.end += delta_deslocamento


dir_trabalho = '/home/fagner/Vídeos/Banco De Testes Para Legendas/'

arq_dir_trabalho = os.listdir(dir_trabalho)
dir_bak_leg(dir_trabalho, arq_dir_trabalho)

dir_c_leg = os.listdir(dir_trabalho + CONFIG["dirLegendaAntiga"])

for arquivo_de_legenda in dir_c_leg:
    if arquivo_de_legenda.endswith(".ass"):
        subs = pysubs2.load(dir_trabalho + CONFIG["dirLegendaAntiga"] + '/' + arquivo_de_legenda, encoding="utf-8")
        desloca_subs(subs)
        subs.save(dir_trabalho + '/' + arquivo_de_legenda)
