import json
import os
import re
import shutil
import sys

import natsort as natsort
import pysubs2 as pysubs2
import requests

CONFIG: object = json.load(open('config.json', 'r'))
CONFIG_ESTILOS_LEGENDAS: object = json.load(open('estilos.json', 'r'))


def baixa_tvmaze_legendas(codigo=None):
    url = 'http://api.tvmaze.com/shows/' + codigo + '/episodes'
    anime_episodios = requests.get(url, verify=True)

    return anime_episodios.json()


def criar_diretorio_de_backup_legendas(dir_trabalho_temp=None, dir_legenda=None) -> object:
    # Criando o Diretório onde ficaram as legendas originais da Crunchroll
    try:
        original_umask = os.umask(0)
        os.mkdir(dir_trabalho_temp + CONFIG["dirLegendaAntiga"])
    except OSError:
        print("Creation of the directory %s failed" % dir_trabalho_temp)
    else:
        print("Successfully created the directory %s " % dir_trabalho_temp)
    finally:
        os.umask(original_umask)

    # Move os arquivos de legendas para o diretorio de Backup
    for arquivo_de_legenda in dir_legenda:
        if arquivo_de_legenda.endswith(".ass"):
            shutil.move(dir_trabalho_temp + '/' + arquivo_de_legenda, dir_trabalho_temp + CONFIG["dirLegendaAntiga"])


def listar_arquivos(directory, extension):
    lista_de_nomes = []
    for f in os.listdir(directory):
        if f.endswith('.' + extension):
            lista_de_nomes.append(f)
    return lista_de_nomes


def exibir_previa(nome_temp=None, temp_nome_legenda=None, temp_nome_episodio=None):
    """

    :rtype: object
    """
    print('<--------\t' + nome_temp + '\t-------->\n')
    print('Legenda:\t' + temp_nome_legenda)
    print('Episódio:\t' + temp_nome_episodio)


def corrigi_estilos_subs(temp_arq_de_legenda, temp_dir_salvar, temp_nome_salvar):
    subs = pysubs2.load(temp_arq_de_legenda, encoding="utf-8")

    novas_fontes_estilos = CONFIG["fontesEstilos"]

    for nome_estilo, estilo in zip(subs.styles.keys(), subs.styles.values()):
        try:
            estilo.fontname = CONFIG["fontesEstilos"][nome_estilo]
        except:
            estilo.fontname = CONFIG["fontePadrao"]

    subs.save(temp_dir_salvar + '/' + temp_nome_salvar)


def corrigi_estilos_subs2(subs, temp_dir_salvar, temp_nome_salvar):
    # subs = pysubs2.load(temp_arq_de_legenda, encoding="utf-8")

    subs.info = {"Title": "[Legendas-Otaku] Português (Brasil)", "PlayResX": 640, "PlayResY": 360,
                 "ScriptType": "v4.00+", "WrapStyle": "0"}

    subs.aegisub_project = {}

    novas_fontes_estilos = CONFIG["fontesEstilos"]

    altera_elementos = lambda x, y: x if x else y
    altera_cor = lambda x, y: pysubs2.Color(*x) if True else y
    for nome_estilo, estilo in zip(subs.styles.keys(), subs.styles.values()):
        for atributo in frozenset(estilo.FIELDS):
            try:
                if any(x == atributo for x in ["backcolor", "outlinecolor", "secondarycolor", "primarycolor"]):
                    vars(estilo)[atributo] = altera_cor(CONFIG_ESTILOS_LEGENDAS[nome_estilo][atributo], vars(estilo)[atributo])
                else:
                    vars(estilo)[atributo] = altera_elementos(CONFIG_ESTILOS_LEGENDAS[nome_estilo][atributo], vars(estilo)[atributo])
            except:
                estilo.fontname = CONFIG_ESTILOS_LEGENDAS["NaoAchou"]["fontname"]
                continue

def res_y_and_scale(subs, res_x_dest=640):
    res_x_src = int(subs.info["PlayResX"])
    res_y_src = int(subs.info["PlayResY"])
    scale = res_x_dest / float(res_x_src)
    res_y_dest = int(scale * res_y_src)

    return scale


def resize_subs(subs, scale=None, res_x_dest=640):
    # styles
    for style in subs.styles.values():
        style.fontsize = int(style.fontsize * scale)
        style.marginl = int(style.marginl * scale)
        style.marginr = int(style.marginr * scale)
        style.marginv = int(style.marginv * scale)
        style.outline = int(style.outline * scale)
        style.shadow = int(style.shadow * scale)
        style.spacing = int(style.spacing * scale)

    # subs.save(temp_arq_de_legenda)


def resize_subs2(subs, scale=None, res_x_dest=640):
    for line in subs:
        try:
            # b = []
            busca_padrao = re.findall('move\((.+?)\)', line.text)
            if len(busca_padrao) == 0:
                busca_padrao = re.findall('pos\((.+?)\)', line.text)
            if len(busca_padrao) == 0:
                busca_padrao = re.findall('org\((.+?)\)', line.text)

            if busca_padrao[0]:
                novas_coordenadas = []
                novas_coordenadas.append("{:.3f}".format(float(busca_padrao[0].split(',')[0]) * scale))
                novas_coordenadas.append("{:.3f}".format(float(busca_padrao[0].split(',')[1]) * scale))
                lista_de_novas_cordenada = ','.join(novas_coordenadas)
                antigas_coordenadas = busca_padrao[0].split(',')[0] + ',' + busca_padrao[0].split(',')[1]
                line.text = line.text.replace(antigas_coordenadas, lista_de_novas_cordenada)
                print(line.text)
        except:
            continue

    # subs.save(temp_arq_de_legenda)


if sys.argv[1] == '-tvmaze':
    lista_de_episodios_tvmaze = baixa_tvmaze_legendas(sys.argv[2])  # sys.argv[2] possui o código da TVMaze
    temporada_episodios = int(sys.argv[3])
    # sys.argv[3] possui o diretório com os animes e legendas
    dir_trabalho = sys.argv[4]

    arquivos_no_diretorio_de_trabalho = os.listdir(dir_trabalho)
    criar_diretorio_de_backup_legendas(dir_trabalho, arquivos_no_diretorio_de_trabalho)

    diretorio_com_legendas = os.listdir(dir_trabalho + CONFIG["dirLegendaAntiga"])

    for arquivo_de_legenda in diretorio_com_legendas:
        if arquivo_de_legenda.endswith(".ass"):
            subs = pysubs2.load(dir_trabalho + CONFIG["dirLegendaAntiga"] + '/' + arquivo_de_legenda, encoding="utf-8")
            escala = res_y_and_scale(subs, res_x_dest=640)
            # temp_nome_nova_legenda = dir_trabalho + CONFIG["dirLegendaAntiga"] + '/' + arquivo_de_legenda.replace(".ptBR", '')
            resize_subs(subs, escala)
            resize_subs2(subs, escala)
            corrigi_estilos_subs2(subs, dir_trabalho, arquivo_de_legenda)
            subs.save(dir_trabalho + '/' + arquivo_de_legenda)

    # LerAquivos
    dir_episodios = listar_arquivos(dir_trabalho, "mkv")
    dir_legendas = listar_arquivos(dir_trabalho, "ass")

    # Ordena Nomes
    dir_episodios = natsort.natsorted(dir_episodios, reverse=False)
    dir_legendas = natsort.natsorted(dir_legendas, reverse=False)

    # Criar Lista de nomes de Episódios
    lista_de_nomes_de_episodios = []
    lista_de_nomes_de_ovas = []

    for episodio in lista_de_episodios_tvmaze:
        if episodio["number"] != None and episodio["season"] == temporada_episodios:
            lista_de_nomes_de_episodios.append("#" + str(episodio["number"]) + ' - ' + episodio["name"])
        else:
            lista_de_nomes_de_ovas.append("#S(" + episodio["airdate"] + ") - " + episodio["name"])

    lista_de_nomes_de_episodios = natsort.natsorted(lista_de_nomes_de_episodios, reverse=False)
    lista_de_nomes_de_ovas = natsort.natsorted(lista_de_nomes_de_ovas, reverse=False)

    for novo_nome_episodio, temp_nome_legenda, temp_nome_episodio in zip(lista_de_nomes_de_episodios, dir_legendas, dir_episodios):
        exibir_previa(novo_nome_episodio.rstrip(), temp_nome_legenda, temp_nome_episodio)
        input('Aperte \'Enter\' para contirnuar:')
        # Renomeando os arquivos
        os.rename(dir_trabalho + '/' + temp_nome_legenda, dir_trabalho + '/' + novo_nome_episodio.rstrip() + '.ass')
        os.rename(dir_trabalho + '/' + temp_nome_episodio, dir_trabalho + '/' + novo_nome_episodio.rstrip() + '.mkv')

if sys.argv[1] == '-ln':
    dir_trabalho = sys.argv[2]
    lista_de_nomes_de_episodios = open(sys.argv[3], "r").readlines()

    arquivos_no_diretorio_de_trabalho = os.listdir(dir_trabalho)
    criar_diretorio_de_backup_legendas(dir_trabalho, arquivos_no_diretorio_de_trabalho)

    diretorio_com_legendas = os.listdir(dir_trabalho + CONFIG["dirLegendaAntiga"])

    for arquivo_de_legenda in diretorio_com_legendas:
        if arquivo_de_legenda.endswith(".ass"):
            subs = pysubs2.load(dir_trabalho + CONFIG["dirLegendaAntiga"] + '/' + arquivo_de_legenda, encoding="utf-8")
            escala = res_y_and_scale(subs, res_x_dest=640)
            # temp_nome_nova_legenda = dir_trabalho + CONFIG["dirLegendaAntiga"] + '/' + arquivo_de_legenda.replace(".ptBR", '')
            resize_subs(subs, escala)
            resize_subs2(subs, escala)
            corrigi_estilos_subs2(subs, dir_trabalho, arquivo_de_legenda)
            subs.save(dir_trabalho + '/' + arquivo_de_legenda)

    # LerAquivos
    dir_episodios = listar_arquivos(dir_trabalho, "mkv")
    dir_legendas = listar_arquivos(dir_trabalho, "ass")

    # Ordena Nomes
    dir_episodios = natsort.natsorted(dir_episodios, reverse=False)
    dir_legendas = natsort.natsorted(dir_legendas, reverse=False)

    lista_de_nomes_de_episodios = natsort.natsorted(lista_de_nomes_de_episodios, reverse=False)

    for novo_nome_episodio, temp_nome_legenda, temp_nome_episodio in zip(lista_de_nomes_de_episodios, dir_legendas, dir_episodios):
        exibir_previa(novo_nome_episodio.rstrip(), temp_nome_legenda, temp_nome_episodio)
        input('Aperte \'Enter\' para contirnuar:')
        # Renomeando os arquivos
        os.rename(dir_trabalho + '/' + temp_nome_legenda, dir_trabalho + '/' + novo_nome_episodio.rstrip() + '.ass')
        os.rename(dir_trabalho + '/' + temp_nome_episodio, dir_trabalho + '/' + novo_nome_episodio.rstrip() + '.mkv')


# if sys.argv[1] == '-ln':
#     dir_trabalho = sys.argv[2]
#     lista_de_nomes = sys.argv[3]
#
#     arquivos_no_diretorio_de_trabalho = os.listdir(dir_trabalho)
#     arquivos_no_diretorio_de_trabalho = os.listdir(dir_trabalho)
#     criar_diretorio_de_backup_legendas(dir_trabalho, arquivos_no_diretorio_de_trabalho)
#     diretorio_com_legendas = os.listdir(dir_trabalho + CONFIG["dirLegendaAntiga"])
#
#     # LerAquivos
#     dir_episodios = listar_arquivos(dir_trabalho, "mkv")
#     dir_legendas = listar_arquivos(dir_trabalho, "ass")
#
#     # Ordena Nomes
#     dir_episodios = natsort.natsorted(dir_episodios, reverse=False)
#     dir_legendas = natsort.natsorted(dir_legendas, reverse=False)
#
#     # LerListaDeNome
#     arquivoComListaDeNomesDosEpisodios = open(lista_de_nomes, "r")
#     listaDeNomesDeEpisodios = arquivoComListaDeNomesDosEpisodios.readlines()
#
#     for nNomeEpisodio, nLegenda, nEpisodio in zip(listaDeNomesDeEpisodios, dirLegendas, dirEpisodios):
#         exibir_previa(nNomeEpisodio.rstrip())
#         input('Aperte \'Enter\' para contirnuar:')
#         # Renomeando os arquivos
#         os.rename(dir_trabalho + '/' + nLegenda, nNomeEpisodio.rstrip() + '.ass')
#         os.rename(dir_trabalho + '/' + nEpisodio, nNomeEpisodio.rstrip() + '.mkv')

################################################
# dirLegendas.sort(key=lambda f: int(re.sub('\D', '', f)))


# Apenas Corigir Legendas
# if sys.argv[1] == '-cl':
#     # sys.argv[2] possui o diretório com os animes e legendas
#     dir_trabalho = sys.argv[2]
#     arquivos_no_diretorio_de_trabalho = os.listdir(dir_trabalho)
#
#     for arquivo_de_legenda in arquivos_no_diretorio_de_trabalho:
#         if arquivo_de_legenda.endswith(".ass"):
#             corrigi_estilos_subs2(dir_trabalho + '/' + arquivo_de_legenda, dir_trabalho, arquivo_de_legenda)
#
# # Corrigi Legendas e Renomeia Arquivos
# if sys.argv[1] == '-clra':
#     resolucao_x_destino = int(sys.argv[2])
#     dir_trabalho = sys.argv[3]
#     arquivos_no_diretorio_de_trabalho = os.listdir(dir_trabalho)
#
#     dir_dest = dir_trabalho + '/' + 'Novas'
#     x = 0
#
#     for arquivo_de_legenda in arquivos_no_diretorio_de_trabalho:
#         if arquivo_de_legenda.endswith(".ass"):
#             caminho_da_legenda = dir_trabalho + '/' + arquivo_de_legenda
#             escala = res_y_and_scale(caminho_da_legenda, resolucao_x_destino)
#             resize_subs(caminho_da_legenda, escala, resolucao_x_destino)
#             resize_subs2(caminho_da_legenda, escala, resolucao_x_destino)
#             corrigi_estilos_subs2(caminho_da_legenda, dir_dest, "NovaLegenda" + str(x) + ".ass")
#             x += 1


