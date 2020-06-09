import sys
import os
import getopt
import requests
import urllib3
import xmltodict

import argparse
import xml.etree.ElementTree as ET
import ntpath
import pysubs2
import re

from matplotlib import font_manager

subs = [
    'Dialogue: 0,0:13:36.16,0:13:40.17,Signs,,0,0,0,,{\blur1\fax0.03\frz358.421\move(928,472,1352,472)\p1\c&H2F2628&}m 0 0 l 437 0 437 95 0 95{\p0}',
    'Dialogue: 0,0:13:36.16,0:13:40.17,Signs,,0,0,0,,{\blur0.5\fax0.03\fs60\c&H6792AE&\frz358.421\move(929,468,1353,468)\fnImpress BT}Biblioteca Sana'
]

novas_linhas = []

escala = 0.5

l  = '\p1\c&H2F2628&}m 0 0 l 437 0 437 95 0 95{\p0}'

for line in subs:
    busca_padrao = re.findall('(?<=p1).*?(?={)', line.text)
    j = busca_padrao[0].split('m')[1]
    antigos_valores = busca_padrao[0].split('m')[1].split(" ")[1:]

    novo_valor = ''
    for valor in antigos_valores:
        try:
            novo_valor += str("{:.0f}".format(float(int(valor) * escala)) + ',')
        except:
            novo_valor += valor + ','
            continue

    novo_valor = novo_valor.replace(','," ")
    line = line.replace(j," " + novo_valor[:-1])
    print(line)

for line in subs:
    try:
        busca_padrao = re.findall('move\((.+?)\)', line)
        if len(busca_padrao) == 0:
            busca_padrao = re.findall('pos\((.+?)\)', line)
        if len(busca_padrao) == 0:
            busca_padrao = re.findall('org\((.+?)\)', line)

        busca_padrao = busca_padrao[0].split(',')

        for coordenadas in [busca_padrao[i: i+2] for i in range(0, len(busca_padrao), 2)]:
            novas_coordenadas = []
            novas_coordenadas.append("{:.0f}".format(float(int(coordenadas[0]) * escala)))
            novas_coordenadas.append("{:.0f}".format(float(int(coordenadas[1]) * escala)))
            lista_de_novas_cordenada = ','.join(novas_coordenadas)
            antigas_coordenadas = coordenadas[0] + ',' + coordenadas[1]
            line = line.replace(antigas_coordenadas, lista_de_novas_cordenada)

        novas_linhas.append(line)
    except:
        continue

print(subs[0] + '\n' + novas_linhas[0] + '\n' + subs[1] + '\n' + novas_linhas[1])

# subs = pysubs2.load('/home/fagner/ProjetosVSCode/ScriptsLegendas/Scripts/[FAL]To_LOVE-Ru_Darkness_2nd-_-07(1280x720 Hi10P BD AAC)[583F1CD6].ass', encoding="utf-8")
# resize_subs(subs)

# lista = ["Arial","Fira Sans"]

# def cheque_fontes_instaladas(subs):
#     lista_de_fontes = open('listaDeFontes.txt','w+')
#     for style in subs.styles.values():
#         if ntpath.basename(font_manager.findfont(style.fontname.replace('-', " "))) == 'DejaVuSans.ttf':
#             lista_de_fontes.write("Fonte: --> " + style.fontname + '\n')

#     lista_de_fontes.close()


# lista_de_fontes = open('listaDeFontes.txt','w+')
# for font in lista:
#     r = ntpath.basename(font_manager.findfont(font.replace('-', " ")))
#     if r  == 'DejaVuSans.ttf':
#         lista_de_fontes.write("Fonte: --> " + font + '\n')
# lista_de_fontes.close()




# x = map(lambda x: x.split(":")[1], commands.getstatusoutput('fc-list')[1].split("\n"))

# def baixa_tvmaze_legendas(codigo=None):
#     return requests.get('http://api.anidb.net:9001/httpapi?request=anime&client=fagnerpc&clientver=2&protover=1&aid=5625', verify=True).json()

# tree = requests.get(
#     "http://api.anidb.net:9001/httpapi?request=anime&client=fagnerpc&clientver=2&protover=1&aid=5625", verify=True
# ).content()
# tree = ET.fro('Scripts/httpapi.xml')
# root = tree.getroot()
# # legendas = requests.get(
# #     'http://api.anidb.net:9001/httpapi?request=anime&client=fagnerpc&clientver=2&protover=1&aid=5625',
# #     verify=True).json()

# # t = root.findall(
# #     "./episodes/episode/[title='en']"
# # )
# # for child in root.findall("./episodes/episode/title/[lang='en']"):
# #     print(child.attrib)

# names = {}
# for i in tree.iter("episode"):
#     student_id = i.find("epno").text
#     for t in i.findall('title'):
#         if t.attrib['{http://www.w3.org/XML/1998/namespace}lang'] == 'en':
#             # n = int(i.find("epno").text)
#             try:
#                 print('#' + str(int(i.find("epno").text)) + ' - ' + t.text)
#             except:
#                 continue
#     k = [x.text for x in i.findall('title')]
#     names[student_id] = k

# print(names)

# for ep in root['anime']['episodes']['episode']:
#     for t in ep['title']:
#         if ep[1] == 'en':
#             print(ep['title']['@xml:lang'])


# parser = argparse.ArgumentParser(description='Um programa de exemplo.')

# parser.add_argument('--frase',
#                     action='store',
#                     dest='frase',
#                     default='Hello, world!',
#                     required=False,
#                     help='A frase que deseja imprimir n vezes.')

# parser.add_argument('-n',
#                     action='store',
#                     dest='n',
#                     required=True,
#                     help='O número de vezes que a frase será impressa.')

# arguments = parser.parse_args()

# for i in range(0, int(arguments.n)):
#     print (arguments.frase)

# import json
# import os
# import re
# import shutil
# import sys

# import natsort as natsort
# import pysubs2 as pysubs2
# import requests

# lista = ["N1.ass", "N2.mkv","N3.ass","N4.mkv"]

# l1 = [x for x in lista if x.endswith(".ass")]

# teste  = lambda arquivo, extensao: arquivo if arquivo.endswith(".ass") else None

# m = [teste(x, "ass") for x in lista]

# # m = teste("N1.mkv","ass")

# # map()

# # m = map(teste,lista)

# print(m)


# def trocar_caractere(texto):
#     replacements = {"?": "_", ":": "~"}

#     return "".join([replacements.get(c, c) for c in texto])

# text = trocar_caractere("Olá?, como vai:")

# print(text)
