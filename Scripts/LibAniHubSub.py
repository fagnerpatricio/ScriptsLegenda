import ntpath
import os
import shutil
import natsort
import requests
import re
import json

import pysubs2
from tabulate import tabulate
from matplotlib import font_manager

# Bloco de Configurações
CONFIG = {
    "dirLegendaAntiga": "Legendas Originais"
}

fontes_legendas_otaku = {
    'Arial':'Roboto',
    'Comic Sans MS': 'Comic Neue',
    'Times New Roman':'Roboto Slab',
    'Trebuchet MS': 'Fira Sans',
    'Verdana': 'Arimo'
}

fontes_legendas_otaku_extendido = {
    'Arial':'Roboto',
    'Comic Sans MS': 'Comic Neue',
    'Times New Roman':'Roboto Slab',
    'TimesNewRoman':'Roboto Slab',
    'Trebuchet MS': 'Allerta',
    'Verdana': 'Arimo',
    'Ad Hoc': 'Metal Mania',
    'Franklin Gothic Book': 'Libre Franklin',
    'Utopia Std Display': 'Playfair Display'
}


Padrao = {
        "fontname": "Merriweather Sans",
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
        "fontname": "Merriweather Sans",
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
    "fontname": "Merriweather Sans"
    }

estilos = {
    'Default': Padrao,
    'Default-Alt': Padrao,
    'Default Italic': Italico
}

CONFIG_ESTILOS_LEGENDAS = json.loads(json.dumps(estilos))

def trocar_caractere(texto):
    replacements = {
        "?": "^",
        ":": "_",
        "/": "~"
    }

    return "".join([replacements.get(c, c) for c in texto])


def exibe_previa(lista_de_nomes_de_episodios, dir_legendas, dir_episodios):
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

def renomeia_arquivos(dir_trabalho,lista_de_nomes_de_episodios, dir_legendas, dir_episodios,extensao_legendas='.ass',extensao_video='.mkv'):
    for nn_episodio, tn_leg, tn_ep in zip(lista_de_nomes_de_episodios, dir_legendas, dir_episodios):
    # Renomeando os arquivos
        shutil.move(dir_trabalho + '/' + tn_leg, dir_trabalho + '/' + trocar_caractere(nn_episodio.rstrip()) + extensao_legendas)
        shutil.move(dir_trabalho + '/' + tn_ep, dir_trabalho + '/' + trocar_caractere(nn_episodio.rstrip()) + extensao_video)

def dir_bak_leg(dir_trabalho=None, arquivos_de_legenda=None,dir_backup='Legendas Originais',extensao_legenda='.ass'):
    # Criando o Diretório onde ficaram as legendas originais da Crunchroll
    try:
        original_umask = os.umask(0)
        os.mkdir(dir_trabalho + '/' + dir_backup)
    except OSError:
        print("Falha na cricao do diretorio porque ele ja existe" + dir_trabalho + '/' + dir_backup)
    else:
        print("Successfully created the directory %s " + dir_trabalho + '/' + dir_backup)
    finally:
        os.umask(original_umask)

    # Move os arquivos de legendas para o diretorio de Backup
    for arquivo_de_legenda in arquivos_de_legenda:
        if arquivo_de_legenda.endswith(extensao_legenda):
            try:
                shutil.move(dir_trabalho +'/'+ arquivo_de_legenda, dir_trabalho + '/' + dir_backup)
            except OSError:
                print("Arquivo já existe no destino" + arquivo_de_legenda)

def cheque_fontes_instaladas(subs,arquivo):
    for style in subs.styles.values():
        if ntpath.basename(font_manager.findfont(style.fontname.replace('-', " "))) == 'DejaVuSans.ttf':
            arquivo.write("Fonte: --> " + style.fontname + '\n')

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

    n = lambda v: str("{:.3f}".format(float(v) * escala)) if v.replace('.','').lstrip('-').isdigit() else v
    j = lambda x: " ".join([n(c) for c in re.split(r'[,\s]\s*', x[-1:][0])]) if x[0] == 'm' else ",".join([n(c) for c in re.split(r'[,\s]\s*', x[-1:][0])])
    for line in subs:
        busca_de_padroes = [tuple(i for i in m if i) for m in re.findall(r'[\\|\(|\}](m)(\s.+?)[\)|\{]|(pos|move|org|clip)(\()(.+?)\)|(fs)(\d+\.?\d+)',line.text)]
        for padrao in busca_de_padroes:
            try:
                line.text = line.text.replace("".join(padrao),"".join(padrao[:-1]) + j(padrao))
            except:
                continue

def tratamento_legendas_crunchroll(dir_trabalho=None, dir_legenda=None,dir_backup='Legendas Originais',extensao_legenda='.ass'):
    lista_de_fontes = open(dir_trabalho + '/' + 'listaDeFontes.txt', 'w+')

    for arquivo_de_legenda in dir_legenda:
        if arquivo_de_legenda.endswith(extensao_legenda):
            subs = pysubs2.load(dir_trabalho + '/' + dir_backup +'/'+ arquivo_de_legenda, encoding="utf-8")
            corrigi_estilos_crunchroll(subs)
            cheque_fontes_instaladas(subs,lista_de_fontes)
            subs.save(dir_trabalho + '/' + arquivo_de_legenda)

    lista_de_fontes.close()

def tratamento_legendas_tvmaze(dir_trabalho=None, arquivos_de_legenda=None,dir_backup='Legendas Originais',extensao_legenda='.ass'):
    lista_de_fontes = open('listaDeFontes.txt', 'w+')

    for arquivo_de_legenda in arquivos_de_legenda:
        if arquivo_de_legenda.endswith(extensao_legenda):
            subs = pysubs2.load(dir_trabalho + '/' + dir_backup +'/'+ arquivo_de_legenda, encoding="utf-8")
            resize_subs(subs)
            corrigi_estilos_tvmaze(subs)
            cheque_fontes_instaladas(subs,lista_de_fontes)
            subs.save(dir_trabalho + '/' + arquivo_de_legenda)

    lista_de_fontes.close()

def corrigi_estilos_crunchroll(subs):
    subs.info = {
        "Title": "[Legendas-Otaku] Português (Brasil)",
        "PlayResX": subs.info["PlayResX"],
        "PlayResY": subs.info["PlayResY"],
        "ScriptType": "v4.00+",
        "WrapStyle": "0"
    }

    subs.aegisub_project = {}
    lista_com_contadores_de_estilos = {}

    #Verifica se um Stylo está sendo usado
    for nome_estilo, estilo in zip(subs.styles.keys(), subs.styles.values()):
        contador = 0
        for line in subs:
            if nome_estilo == line.style:
                contador += 1

        lista_com_contadores_de_estilos[nome_estilo] = contador

        try:
            estilo.fontname = fontes_legendas_otaku[estilo.fontname]
        except:
            continue

    # Remove o estilo caso ele não esteja sendo usado
    for estilo in lista_com_contadores_de_estilos:
        if lista_com_contadores_de_estilos[estilo] == 0:
            subs.styles.pop(estilo)

def corrigi_estilos_tvmaze(subs):
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
                    vars(estilo)[atributo] = altera_cor(CONFIG_ESTILOS_LEGENDAS[nome_estilo][atributo], vars(estilo)[atributo])
                else:
                    vars(estilo)[atributo] = altera_elementos(CONFIG_ESTILOS_LEGENDAS[nome_estilo][atributo], vars(estilo)[atributo])
            except:
                continue

        try:
            estilo.fontname = fontes_legendas_otaku_extendido[estilo.fontname]
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

def renomeia_crunchroll(dir_trabalho):
    # LerAquivos
    dir_episodios = [x for x in os.listdir(dir_trabalho) if (x.endswith(".mp4") or x.endswith(".mkv"))]
    dir_legendas = [x for x in os.listdir(dir_trabalho) if x.endswith(".ass")]

    # Ordena Nomes
    dir_episodios = natsort.natsorted(dir_episodios, reverse=False)
    dir_legendas = natsort.natsorted(dir_legendas, reverse=False)

    # Criar Lista de nomes de Episódios
    lista_de_nomes_de_episodios = []
    lista_de_nomes_de_episodios = ['#' + os.path.splitext(x.split('Episódio ')[1])[0].replace(".ptBR","") for x in dir_legendas]
    lista_de_nomes_de_episodios = natsort.natsorted(lista_de_nomes_de_episodios, reverse=False)

    #Exibe prévia
    exibe_previa(lista_de_nomes_de_episodios,dir_legendas,dir_episodios)

    input('Aperte \'Enter\' para contirnuar:')

    renomeia_arquivos(
        dir_trabalho=dir_trabalho,
        lista_de_nomes_de_episodios=lista_de_nomes_de_episodios,
        dir_legendas=dir_legendas,
        dir_episodios=dir_episodios
    )

def renomeia_tvmaze(dir_trabalho,lista_de_episodios_tvmaze,temporada_episodios=1):
    # LerAquivos
    dir_episodios = [x for x in os.listdir(dir_trabalho) if x.endswith(".mkv")]
    dir_legendas = [x for x in os.listdir(dir_trabalho) if x.endswith(".ass")]

    # Ordena Nomes
    dir_episodios = natsort.natsorted(dir_episodios, reverse=False)
    dir_legendas = natsort.natsorted(dir_legendas, reverse=False)

    lista_de_nomes_de_episodios = []

    # Criar Lista de nomes de Episódios
    for episodio in lista_de_episodios_tvmaze:
        if episodio["number"] != None and episodio["season"] == temporada_episodios:
            lista_de_nomes_de_episodios.append("#" + str(episodio["number"]) + ' - ' + episodio["name"])

    #Exibe prévia
    exibe_previa(lista_de_nomes_de_episodios,dir_legendas,dir_episodios)

    input('Aperte \'Enter\' para contirnuar:')

    renomeia_arquivos(
        dir_trabalho=dir_trabalho,
        lista_de_nomes_de_episodios=lista_de_nomes_de_episodios,
        dir_legendas=dir_legendas,
        dir_episodios=dir_episodios
    )

def baixa_tvmaze_legendas(codigo=None):
    return requests.get('http://api.tvmaze.com/shows/' + codigo + '/episodes', verify=True).json()