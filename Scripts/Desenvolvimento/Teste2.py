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

    subs.info = {
        "Title": "[Legendas-Otaku] Português (Brasil)",
        "PlayResX": 640,
        "PlayResY": 360,
        "ScriptType": "v4.00+",
        "WrapStyle": "0"
    }

    subs.aegisub_project = {}

    n = lambda v: str("{:.3f}".format(float(v) * escala)) if v.replace('.','').lstrip('-').isdigit() else v
    j = lambda x: " ".join([n(c) for c in re.split(r'[,\s]\s*', x[-1:][0])]) if x[0] == 'm' else ",".join([n(c) for c in re.split(r'[,\s]\s*', x[-1:][0])])
    for line in subs:
        busca_de_padroes = [tuple(i for i in m if i) for m in re.findall(r'(move|clip)(\()((?:\-?\,?\d+\.?\d+\W+?\d+\.?\d+)(?:\-?\,?\d+\.?\d+\W+?\d+\.?\d+)?)|[\\|\(|\}|\,](m)(\s.+?)[\)|\{]|(pos|move|org)(\()(.+?)\)|(fs)(\d+\.?\d+)',line.text)]
        # (move|clip|pos|org|fs)(\()?((?:\,?\-?\d+\.?\d+){1,4})
        for padrao in busca_de_padroes:
            try:
                line.text = line.text.replace("".join(padrao),"".join(padrao[:-1]) + j(padrao))
            except:
                continue
    # n = lambda v: str("{:.3f}".format(float(v) * escala)) if v.replace('.','').lstrip('-').isdigit() else v
    # for line in subs:
    #     try:
    #         b_padroes = [tuple(i for i in m if i) for m in re.findall(r'(pos|move|org|clip)(\()(.+?)\)|(fs)(\d+\.?\d+)',line.text)]
    #         for padrao in b_padroes:
    #             line.text = line.text.replace("".join(padrao),"".join(padrao[:-1]) + ",".join([n(c) for c in re.split(r'[,\s]\s*', padrao[-1:][0])]))

    #         b2_padroes = [tuple(i for i in m if i) for m in re.findall(r'(p[1-4])(.*)?(m.+[0-9]+.+(?={))',line.text)]
    #         for padrao in b2_padroes:
    #             line.text = line.text.replace("".join(padrao),"".join(padrao[:-1]) + " ".join([n(c) for c in re.split(r'[,\s]\s*', padrao[-1:][0])]))
    #     except:
    #         continue

    #     try:
    #         substituicao_tipo01 = substituicao_tipo02 = False
    #         busca_padrao = re.findall(r'(?<=p[1-4]).*?(?={)', line.text)
    #         if len(busca_padrao) > 0:
    #             substituicao_tipo01 = True
    #             antigos_valores = busca_padrao[0].split('m')[1].split(" ")[1:]
    #         if len(busca_padrao) == 0:
    #             substituicao_tipo02 = True
    #             antigos_valores = busca_padrao = line.text.split(re.findall(r'(?<=p[1-4]).*?(?=m)', line.text)[0])[1][2:].split(" ")

    #         novo_valor = ''
    #         for valor in antigos_valores:
    #             try:
    #                 novo_valor += str("{:.3f}".format(float(int(valor) * escala)) + ',')
    #             except:
    #                 novo_valor += valor + ','
    #                 continue

    #         novo_valor = novo_valor.replace(','," ")
    #         if substituicao_tipo01:
    #             line.text = line.text.replace(busca_padrao[0].split('m')[1]," " + novo_valor[:-1])
    #         if substituicao_tipo02:
    #             v = line.text.split(re.findall(r'(?<=p[1-4]).*?(?=m)', line.text)[0])[1][2:]
    #             line.text = line.text.replace(v," " + novo_valor[:-1])
    #     except:
    #         continue

    # for line in subs:
    #     try:
    #         busca_padrao = re.findall(r'fs([0-9]+)', line.text)
    #         if busca_padrao[0]:
    #             antigas_coordenadas = busca_padrao[0]
    #             novas_coordenadas = []
    #             novas_coordenadas.append("{:.3f}".format(float(int(busca_padrao[0]) * escala)))
    #             line.text = line.text.replace("fs" + antigas_coordenadas, "fs" + novas_coordenadas[0])
    #     except:
    #         continue

    # for line in subs:
    #     try:
    #         busca_padrao = re.findall(r'clip\((.+?)\)', line.text)

    #         if busca_padrao[0][0] == 'm':
    #             antigos_valores = busca_padrao[0].split('m')[1].split(" ")[1:]
    #             novo_valor = ''
    #             for valor in antigos_valores:
    #                 try:
    #                     novo_valor += str("{:.3f}".format(float(int(valor) * escala)) + ',')
    #                 except:
    #                     novo_valor += valor + ','
    #                     continue
    #                 novo_valor = novo_valor.replace(','," ")
    #             line.text = line.text.replace(busca_padrao[0].split('m')[1]," " + novo_valor[:-1])
    #         else:
    #             busca_padrao = busca_padrao[0].split(',')

    #             for coordenadas in [busca_padrao[i:i + 2] for i in range(0, len(busca_padrao), 2)]:
    #                 novas_coordenadas = []
    #                 novas_coordenadas.append("{:.3f}".format(float(coordenadas[0]) * escala))
    #                 novas_coordenadas.append("{:.3f}".format(float(coordenadas[1]) * escala))
    #                 lista_de_novas_cordenada = ','.join(novas_coordenadas)
    #                 antigas_coordenadas = coordenadas[0] + ',' + coordenadas[1]
    #                 line.text = line.text.replace(antigas_coordenadas, lista_de_novas_cordenada)
    #     except:
    #         continue

    # for line in subs:
    #     try:
    #         busca_padrao = re.findall(r'move\((.+?)\)', line.text)
    #         if len(busca_padrao) == 0:
    #             busca_padrao = re.findall(r'pos\((.+?)\)', line.text)
    #             # print(busca_padrao)
    #         if len(busca_padrao) == 0:
    #             busca_padrao = re.findall(r'org\((.+?)\)', line.text)

    #         busca_padrao = busca_padrao[0].split(',')

    #         for coordenadas in [busca_padrao[i: i+2] for i in range(0, len(busca_padrao), 2)]:
    #             novas_coordenadas = []
    #             novas_coordenadas.append("{:.3f}".format(float(coordenadas[0]) * escala))
    #             novas_coordenadas.append("{:.3f}".format(float(coordenadas[1]) * escala))
    #             lista_de_novas_cordenada = ','.join(novas_coordenadas)
    #             antigas_coordenadas = coordenadas[0] + ',' + coordenadas[1]
    #             line.text = line.text.replace(antigas_coordenadas, lista_de_novas_cordenada)
    #     except:
    #         continue



dir_trabalho = '/home/fagner/Vídeos/sampletest'

arq_dir_trabalho = os.listdir(dir_trabalho)
dir_bak_leg(dir_trabalho, arq_dir_trabalho)

dir_c_leg = os.listdir(dir_trabalho + CONFIG["dirLegendaAntiga"])

for arquivo_de_legenda in dir_c_leg:
    if arquivo_de_legenda.endswith(".ass"):
        subs = pysubs2.load(dir_trabalho + CONFIG["dirLegendaAntiga"] + '/' + arquivo_de_legenda, encoding="utf-8")
        resize_subs(subs)
        subs.save(dir_trabalho + '/' + arquivo_de_legenda)
