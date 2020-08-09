#!/usr/bin/env python

#Importações do Sistema
import argparse
import os

#Importações Personalizadas
import LibAniHubSub

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
        type=int,
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
        help='Indica a resolução em X'
    )

    parser.add_argument(
        '-ry',
        action='store',
        dest='res_y',
        required=False,
        help='Indica a resolução em Y'
    )

    try:
        argumentos = parser.parse_args()

        LibAniHubSub.dir_bak_leg(
            dir_trabalho=argumentos.dir_trabalho,
            arquivos_de_legenda=os.listdir(argumentos.dir_trabalho)
        )

        info_serie, lista_de_episodios_tvmaze = LibAniHubSub.baixa_tvmaze_infos(argumentos.cod_tvmaze)

        LibAniHubSub.tratamento_legendas_tvmaze(
            dir_trabalho=argumentos.dir_trabalho,
            arquivos_de_legenda=os.listdir(argumentos.dir_trabalho + '/' + LibAniHubSub.CONFIG["dirLegendaAntiga"]),
            res_x=argumentos.res_x,
            res_y=argumentos.res_y
        )

        LibAniHubSub.renomeia_tvmaze(
            dir_trabalho=argumentos.dir_trabalho,
            lista_de_episodios_tvmaze=lista_de_episodios_tvmaze,
            temporada_episodios=argumentos.temporada
        )

        print('SUCESSO :DDDD')
    except:
        print('ALGO DEU ERRADO :((((')
