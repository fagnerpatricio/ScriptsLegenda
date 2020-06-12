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

    try:
        argumentos = parser.parse_args()

        LibAniHubSub.dir_bak_leg(
            dir_trabalho=argumentos.dir_trabalho,
            arquivos_de_legenda=os.listdir(argumentos.dir_trabalho)
        )

        lista_de_episodios_tvmaze = LibAniHubSub.baixa_tvmaze_legendas(argumentos.cod_tvmaze)

        LibAniHubSub.tratamento_legendas_tvmaze(
            dir_trabalho=argumentos.dir_trabalho,
            arquivos_de_legenda=os.listdir(argumentos.dir_trabalho + '/' + LibAniHubSub.CONFIG["dirLegendaAntiga"])
        )

        LibAniHubSub.renomeia_tvmaze(
            dir_trabalho=argumentos.dir_trabalho,
            lista_de_episodios_tvmaze=lista_de_episodios_tvmaze,
            temporada_episodios=argumentos.temporada
        )

        print('SUCESSO :DDDD')
    except:
        print('ALGO DEU ERRADO :((((')
