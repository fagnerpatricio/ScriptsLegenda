import sys
import os
import getopt
import requests
import urllib3
import xmltodict

import argparse
import xml.etree.ElementTree as ET
import ntpath

from matplotlib import font_manager

lista = ["Arial","Fira Sans"]

def cheque_fontes_instaladas(subs):
    lista_de_fontes = open('listaDeFontes.txt','w+')
    for style in subs.styles.values():
        if ntpath.basename(font_manager.findfont(style.fontname.replace('-', " "))) == 'DejaVuSans.ttf':
            lista_de_fontes.write("Fonte: --> " + style.fontname + '\n')

    lista_de_fontes.close()


lista_de_fontes = open('listaDeFontes.txt','w+')
for font in lista:
    r = ntpath.basename(font_manager.findfont(font.replace('-', " ")))
    if r  == 'DejaVuSans.ttf':
        lista_de_fontes.write("Fonte: --> " + font + '\n')
lista_de_fontes.close()




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
