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
# CONFIG_ESTILOS_LEGENDAS = json.load(open('/home/fagner/ProjetosVSCode/ScriptsLegendas/Scripts/estilos.json', 'r'))

Padrao = {
        "fontname": "Fira Sans",
        "fontsize": 22,
        "backcolor": [
            0,
            0,
            0,
            0
        ],
        "outlinecolor": [
            25,
            25,
            25,
            0
        ],
        "secondarycolor": [
            0,
            0,
            255,
            0
        ],
        "primarycolor": [
            255,
            255,
            255,
            0
        ],
        "bold": -1,
        "italic": 0,
        "underline": 0,
        "strikeout": 0,
        "scalex": 100,
        "scaley": 100,
        "spacing": 0,
        "angle": 0,
        "borderstyle": 1,
        "outline": 2,
        "shadow": 1,
        "alignment": 2,
        "marginl": 40,
        "marginr": 40,
        "marginv": 15,
        "encoding": 0
    }

Italico = {
        "fontname": "Fira Sans",
        "fontsize": 22,
        "backcolor": [
            0,
            0,
            0,
            0
        ],
        "outlinecolor": [
            25,
            25,
            25,
            0
        ],
        "secondarycolor": [
            0,
            0,
            255,
            0
        ],
        "primarycolor": [
            255,
            255,
            255,
            0
        ],
        "bold": -1,
        "italic": -1,
        "underline": 0,
        "strikeout": 0,
        "scalex": 100,
        "scaley": 100,
        "spacing": 0,
        "angle": 0,
        "borderstyle": 1,
        "outline": 2,
        "shadow": 1,
        "alignment": 2,
        "marginl": 40,
        "marginr": 40,
        "marginv": 15,
        "encoding": 0
    }

SoFonte = {
    "fontname": "Fira Sans"
}
estilos = {
    'Default': Padrao,
    'Main Dialogue': Padrao,
    'Italics Dialogue': Italico,
    'Default - italics': Italico,
}

fontes_legendas_otaku = {
    'Arial':'Roboto',
    'Times New Roman':'Roboto Slab',
    'Trebuchet MS': 'Fira Sans'
}

CONFIG_ESTILOS_LEGENDAS = json.loads(json.dumps(estilos))

print(CONFIG_ESTILOS_LEGENDAS['Default - italics']['fontname'])

def baixa_tvmaze_legendas(codigo=None):
    return requests.get('http://api.tvmaze.com/shows/' + codigo + '/episodes', verify=True).json()


def baixa_anidb_legendas(client=None,clientver=None, codigo=None):
    return ET.fromstring(requests.get(
        "http://api.anidb.net:9001/httpapi?request=anime&client="+client+"&clientver="+clientver+"&protover=1&aid="+codigo,
        verify=True
    ).content)


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


def exibir_previa(nome_temp=None, temp_nome_legenda=None, temp_nome_episodio=None):
    print('<--------\t' + nome_temp + '\t-------->\n')
    print('Legenda:\t' + temp_nome_legenda)
    print('Episódio:\t' + temp_nome_episodio)


def corrigi_estilos_subs(subs, temp_dir_salvar, temp_nome_salvar):
    subs.info = {
        "Title": "[Legendas-Otaku] Português (Brasil)",
        "PlayResX": 640,
        "PlayResY": 360,
        "ScriptType": "v4.00+",
        "WrapStyle": "0"
    }

    subs.aegisub_project = {}

    lista_com_contadores_de_estilos = {}

    altera_elementos = lambda x, y: x if x else y
    altera_cor = lambda x, y: pysubs2.Color(*x) if True else y

    for nome_estilo, estilo in zip(subs.styles.keys(), subs.styles.values()):
        for atributo in frozenset(estilo.FIELDS):
            try:
                if any(x == atributo for x in ["backcolor", "outlinecolor", "secondarycolor","primarycolor"]):
                    vars(estilo)[atributo] = altera_cor(CONFIG_ESTILOS_LEGENDAS[nome_estilo][atributo],
                                                        vars(estilo)[atributo])
                else:
                    vars(estilo)[atributo] = altera_elementos(CONFIG_ESTILOS_LEGENDAS[nome_estilo][atributo],
                                                              vars(estilo)[atributo])
            except:
                continue

        #Verifica se um Stylo está sendo usado
        contador = 0
        for line in subs:
            if nome_estilo == line.style:
                contador += 1

        lista_com_contadores_de_estilos[nome_estilo] = contador

    # Remove o estilo caso ele não esteja sendo usado
    for estilo in lista_com_contadores_de_estilos:
        if lista_com_contadores_de_estilos[estilo] == 0:
            subs.styles.pop(estilo)


def resize_subs(subs, res_x_dest=640):
    res_x_src = int(subs.info["PlayResX"])
    # res_y_src = int(subs.info["PlayResY"])
    escala = res_x_dest / float(res_x_src)
    # res_y_dest = int(escala * res_y_src)

    for style in subs.styles.values():
        style.fontsize = int(style.fontsize * escala)
        style.marginl = int(style.marginl * escala)
        style.marginr = int(style.marginr * escala)
        style.marginv = int(style.marginv * escala)
        style.outline = int(style.outline * escala)
        style.shadow = int(style.shadow * escala)
        style.spacing = int(style.spacing * escala)
        try:
            style.fontname = fontes_legendas_otaku[style.fontname]
        except:
            continue

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
                novas_coordenadas.append("{:.0f}".format(float(int(busca_padrao[0]) * escala)))
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


def cheque_fontes_instaladas(subs,arquivo):
    for style in subs.styles.values():
        if ntpath.basename(font_manager.findfont(style.fontname.replace('-', " "))) == 'DejaVuSans.ttf':
            arquivo.write("Fonte: --> " + style.fontname + '\n')


def trocar_caractere(texto):
    replacements = {
        "?": "^",
        ":": "_",
        "/": "~"
    }

    return "".join([replacements.get(c, c) for c in texto])

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Um programa de exemplo.',
                                     argument_default=argparse.SUPPRESS)

    choices=range(5, 10)

    parser.add_argument(
        '-m',
        action='store',
        dest='cod_m',
        required=True,
        default=None,
        choices=['crunchroll', 'anidb', 'tvmaze'],
        help=
        'Indica o código do animes para buscar as informações no site da TVMaze'
    )

    parser.add_argument(
        '-anidb',
        action='store',
        dest='cod_anidb',
        required=False,
        default=None,
        help=
        'Indica o código do animes para buscar as informações no site da TVMaze'
    )

    parser.add_argument(
        '-anidb-cliente',
        action='store',
        dest='cod_anidb_cliente',
        required=False,
        default=None,
        help=
        'Indica o código do animes para buscar as informações no site da TVMaze'
    )

    parser.add_argument(
        '-versao-cliente',
        action='store',
        dest='cod_anidb_versao_cliente',
        required=False,
        default=None,
        help=
        'Indica o código do animes para buscar as informações no site da TVMaze'
    )

    parser.add_argument(
        '-tvmaze',
        action='store',
        dest='cod_tvmaze',
        required=False,
        default=None,
        help='Indica o código do animes para buscar as informações no site da TVMaze'
    )

    parser.add_argument(
        '-t',
        action='store',
        dest='temporada',
        required=False,
        default=-1,
        help='Indica a temporada do anime'
    )

    parser.add_argument(
        '-d',
        action='store',
        dest='dir_trabalho',
        required=True,
        help='Indica o diretorio que os arquivos estão'
    )

    argumentos = parser.parse_args()

    modo_de_operacao = argumentos.cod_m
    lista_de_episodios_tvmaze = argumentos.cod_tvmaze
    lista_de_episodios_anidb = argumentos.cod_anidb

    if argumentos.cod_anidb and (argumentos.cod_anidb_cliente is None or argumentos.cod_anidb_versao_cliente is None):
        parser.error("-anidb [CÓDIGO] -anidb-cliente [CLIENTE] -versao-cliente [INT]")

    if lista_de_episodios_tvmaze != None:
        lista_de_episodios_tvmaze = baixa_tvmaze_legendas(argumentos.cod_tvmaze)
        temporada_episodios = int(argumentos.temporada)

    if lista_de_episodios_anidb != None:
        lista_de_episodios_anidb = baixa_anidb_legendas(argumentos.cod_anidb_cliente, argumentos.cod_anidb_versao_cliente, argumentos.cod_anidb)

    # try:
    #     temporada_episodios = int(argumentos.temporada)
    # except:
    #     temporada_episodios = None

    dir_trabalho = argumentos.dir_trabalho

    arq_dir_trabalho = os.listdir(dir_trabalho)
    dir_bak_leg(dir_trabalho, arq_dir_trabalho)

    dir_c_leg = os.listdir(dir_trabalho + CONFIG["dirLegendaAntiga"])

    lista_de_fontes = open('listaDeFontes.txt', 'w+')

    for arquivo_de_legenda in dir_c_leg:
        if arquivo_de_legenda.endswith(".ass"):
            subs = pysubs2.load(dir_trabalho + CONFIG["dirLegendaAntiga"] +'/'+ arquivo_de_legenda, encoding="utf-8")
            if modo_de_operacao == 'crunchroll':
                for style in subs.styles.values():
                    try:
                        style.fontname = fontes_legendas_otaku[style.fontname]
                    except:
                        continue
            else:
                resize_subs(subs)
                corrigi_estilos_subs(subs, dir_trabalho, arquivo_de_legenda)
            cheque_fontes_instaladas(subs,lista_de_fontes)
            subs.save(dir_trabalho + '/' + arquivo_de_legenda)

    lista_de_fontes.close()

    # LerAquivos
    dir_episodios = [x for x in os.listdir(dir_trabalho) if x.endswith(".mkv")]
    dir_legendas = [x for x in os.listdir(dir_trabalho) if x.endswith(".ass")]

    # Ordena Nomes
    dir_episodios = natsort.natsorted(dir_episodios, reverse=False)
    dir_legendas = natsort.natsorted(dir_legendas, reverse=False)

    # Criar Lista de nomes de Episódios
    lista_de_nomes_de_episodios = []
    lista_de_nomes_de_ovas = []

    if modo_de_operacao == 'crunchroll':
        lista_de_nomes_de_episodios = ['#' + os.path.splitext(x.split('Episódio ')[1])[0].replace(".ptBR","") for x in dir_legendas]

    if lista_de_episodios_tvmaze != None:
        for episodio in lista_de_episodios_tvmaze:
            if episodio["number"] != None and episodio["season"] == temporada_episodios:
                lista_de_nomes_de_episodios.append("#" + str(episodio["number"]) + ' - ' + episodio["name"])
            else:
                lista_de_nomes_de_ovas.append("#S(" + episodio["airdate"] +") - " + episodio["name"])

    if lista_de_episodios_anidb != None:
        for episodio in lista_de_episodios_anidb.iter("episode"):
            for titulo in episodio.findall('title'):
                if titulo.attrib['{http://www.w3.org/XML/1998/namespace}lang'] == 'en':
                    try:
                        lista_de_nomes_de_episodios.append('#' + str(int(episodio.find("epno").text)) + ' - ' + titulo.text)
                    except:
                        lista_de_nomes_de_ovas.append('#' + episodio.find("epno").text + ' - ' + titulo.text)

    lista_de_nomes_de_episodios = natsort.natsorted(lista_de_nomes_de_episodios, reverse=False)
    lista_de_nomes_de_ovas = natsort.natsorted(lista_de_nomes_de_ovas, reverse=False)

    print(
        tabulate(
            [
                list(ele) for ele in zip(lista_de_nomes_de_episodios, dir_legendas, dir_episodios)
            ],
            headers=[
                'Novo Nome Dos Arquivos',
                'Arquivos de Legendas',
                'Arquivo de Vídeo'
            ],
            tablefmt="fancy_grid"
        )
    )

    input('Aperte \'Enter\' para contirnuar:')

    for nn_episodio, tn_leg, tn_ep in zip(lista_de_nomes_de_episodios, dir_legendas, dir_episodios):
        # Renomeando os arquivos
        shutil.move(dir_trabalho + '/' + tn_leg, dir_trabalho + '/' + trocar_caractere(nn_episodio.rstrip()) + '.ass')
        shutil.move(dir_trabalho + '/' + tn_ep, dir_trabalho + '/' + trocar_caractere(nn_episodio.rstrip()) + '.mkv')
