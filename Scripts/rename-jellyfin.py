#!/usr/bin/env python

# Importações do Sistema
import argparse
import os
import natsort
import re
import shutil
import requests

# Importações Personalizadas
import LibAniHubSub

EXT_LEG = ".ass"
EXT_MKV = ".mkv"
EXT_MP4 = ".mp4"

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Um programa de exemplo.', argument_default=argparse.SUPPRESS)

    parser.add_argument(
        '-c',
        action='store',
        dest='cod_tvmaze',
        required=True,
        default=None,
        help='Indica o código do animes para buscar as informações no site da TVMaze'
    )

    parser.add_argument(
        '-t',
        action='store',
        dest='temporada',
        type=str,
        required=True,
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

    parser.add_argument(
        '-rx',
        action='store',
        dest='res_x',
        required=False,
        default=640,
        help='Indica a resolução em X'
    )

    parser.add_argument(
        '-ry',
        action='store',
        dest='res_y',
        required=False,
        default=360,
        help='Indica a resolução em Y'
    )

    parser.add_argument(
        '-ts',
        action='store',
        dest='titulo',
        required=False,
        help='Indica o título que será usado no arquivos: titulo.S01E01.mkv'
    )

    parser.add_argument(
        '-ext',
        action='store',
        dest='extensao',
        required=False,
        help='Indica a extensao do arquivo a ser renomeado'
    )

    argumentos = parser.parse_args()

    show = requests.get('http://api.tvmaze.com/shows/' + argumentos.cod_tvmaze + '?embed[]=episodes&embed[]=seasons', verify=True).json()

    nomes_atuais_episodios = [x for x in os.listdir(argumentos.dir_trabalho) if x.endswith(argumentos.extensao)]
    nomes_atuais_episodios = natsort.natsorted(nomes_atuais_episodios, reverse=False)

    f = lambda x: x if x != "" else show['name']
    nomes_novos_episodios = [f(show['_embedded']['seasons'][int(argumentos.temporada) - 1]['name']) + " (" + show['_embedded']['seasons'][int(
        argumentos.temporada) - 1]['premiereDate'].split("-")[0] + ") S" + argumentos.temporada.zfill(2) + "E" + str(c).zfill(2) for c, a in enumerate(nomes_atuais_episodios, 1)]

    if argumentos.extensao == EXT_LEG:

        LibAniHubSub.dir_bak_leg(
            dir_trabalho=argumentos.dir_trabalho,
            arquivos_de_legenda=os.listdir(argumentos.dir_trabalho)
        )

        LibAniHubSub.tratamento_legendas(
            dir_trabalho=argumentos.dir_trabalho,
            arquivos_de_legenda=os.listdir(argumentos.dir_trabalho + '/' + LibAniHubSub.CONFIG["dirLegendaAntiga"]),
            res_x=argumentos.res_x,
            res_y=argumentos.res_y
        )

    LibAniHubSub.renomeia_arquivos_generico(
        dir_trabalho=argumentos.dir_trabalho,
        lista_de_nomes_antigos=nomes_atuais_episodios,
        lista_de_nomes_novos=nomes_novos_episodios,
        extensao=argumentos.extensao
    )

    dirNameShow = show['name'] + " (" + show['premiered'].split("-")[0] + ")"

    try:
        # Create target Directory
        os.mkdir(argumentos.dir_trabalho + '/' + dirNameShow)
        print("Directory ", argumentos.dir_trabalho + '/' + dirNameShow,  " Created ")
    except FileExistsError:
        print("Directory ", argumentos.dir_trabalho + '/' + dirNameShow,  " already exists")

    dirNameTemporada = "Season " + argumentos.temporada

    try:
        # Create target Directory
        os.mkdir(argumentos.dir_trabalho + '/' + dirNameShow + '/' + dirNameTemporada)
        print("Directory ", argumentos.dir_trabalho + '/' + dirNameShow + '/' + dirNameTemporada,  " Created ")
    except FileExistsError:
        print("Directory ", argumentos.dir_trabalho + '/' + dirNameShow + '/' + dirNameTemporada,  " already exists")

    for arquivo in nomes_novos_episodios:
        shutil.move(argumentos.dir_trabalho + '/' + arquivo + argumentos.extensao,
                    argumentos.dir_trabalho + '/' + dirNameShow + '/' + dirNameTemporada + '/' + arquivo + argumentos.extensao)

    print("SUCESSO")
