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

CONFIG = json.load(open('/home/fagner/ProjetosVSCode/ScriptsLegendas/Scripts/config.json', 'r'))


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



def resize_subs(subs, res_x_dest=640):
    res_x_src = int(subs.info["PlayResX"])
    # res_y_src = int(subs.info["PlayResY"])
    escala = res_x_dest / float(res_x_src)
    #res_y_dest = int(escala * res_y_src)

    for style in subs.styles.values():
        style.fontsize = int(style.fontsize * escala)
        style.marginl = int(style.marginl * escala)
        style.marginr = int(style.marginr * escala)
        style.marginv = int(style.marginv * escala)
        style.outline = int(style.outline * escala)
        style.shadow = int(style.shadow * escala)
        style.spacing = int(style.spacing * escala)

    for line in subs:
        try:
            busca_padrao = re.findall(r'(?<=p[1-4]).*?(?={)', line.text)
            antigos_valores = busca_padrao[0].split('m')[1].split(" ")[1:]

            novo_valor = ''
            for valor in antigos_valores:
                try:
                    novo_valor += str("{:.0f}".format(float(int(valor) * escala)) + ',')
                except:
                    novo_valor += valor + ','
                    continue

            novo_valor = novo_valor.replace(','," ")
            line.text = line.text.replace(busca_padrao[0].split('m')[1]," " + novo_valor[:-1])
        except:
            continue

    for line in subs:
        try:
            busca_padrao = re.findall(r'fs([0-9]+)', line.text)
            if busca_padrao[0]:
                antigas_coordenadas = busca_padrao[0]
                novas_coordenadas = []
                novas_coordenadas.append("{:.3f}".format(float(int(busca_padrao[0]) * escala)))
                line.text = line.text.replace("fs" + antigas_coordenadas, "fs" + novas_coordenadas[0])
        except:
            continue

    for line in subs:
        try:
            busca_padrao = re.findall(r'move\((.+?)\)', line.text)
            if len(busca_padrao) == 0:
                busca_padrao = re.findall(r'pos\((.+?)\)', line.text)
            if len(busca_padrao) == 0:
                busca_padrao = re.findall(r'org\((.+?)\)', line.text)

            busca_padrao = busca_padrao[0].split(',')

            for coordenadas in [busca_padrao[i: i+2] for i in range(0, len(busca_padrao), 2)]:
                novas_coordenadas = []
                novas_coordenadas.append("{:.0f}".format(float(int(coordenadas[0]) * escala)))
                novas_coordenadas.append("{:.0f}".format(float(int(coordenadas[1]) * escala)))
                lista_de_novas_cordenada = ','.join(novas_coordenadas)
                antigas_coordenadas = coordenadas[0] + ',' + coordenadas[1]
                line.text = line.text.replace(antigas_coordenadas, lista_de_novas_cordenada)
        except:
            continue


dir_trabalho = '/run/media/fagner/Jogos & Backup/Animes/Não Organizados/[FAL] To Love-Ru BD/DesenScript'

arq_dir_trabalho = os.listdir(dir_trabalho)
dir_bak_leg(dir_trabalho, arq_dir_trabalho)

dir_c_leg = os.listdir(dir_trabalho + CONFIG["dirLegendaAntiga"])

for arquivo_de_legenda in dir_c_leg:
    if arquivo_de_legenda.endswith(".ass"):
        subs = pysubs2.load(dir_trabalho + CONFIG["dirLegendaAntiga"] + '/' + arquivo_de_legenda, encoding="utf-8")
        resize_subs(subs)
        subs.save(dir_trabalho + '/' + arquivo_de_legenda)