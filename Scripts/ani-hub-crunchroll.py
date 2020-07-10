#!/usr/bin/env python

#Importações do Sistema
import argparse
import os

#Importações Personalizadas
import LibAniHubSub

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Um programa de exemplo.', argument_default=argparse.SUPPRESS)

    parser.add_argument(
        '-d',
        action='store',
        dest='dir_trabalho',
        required=True,
        help='Indica o diretorio que os arquivos estão'
    )

    try:
        argumentos = parser.parse_args()
        LibAniHubSub.dir_bak_leg(argumentos.dir_trabalho, os.listdir(argumentos.dir_trabalho))
        dir_c_leg = os.listdir(argumentos.dir_trabalho + '/' + LibAniHubSub.CONFIG["dirLegendaAntiga"])
        LibAniHubSub.tratamento_legendas_crunchroll(dir_trabalho=argumentos.dir_trabalho,dir_legenda=dir_c_leg)
        LibAniHubSub.renomeia_crunchroll(dir_trabalho=argumentos.dir_trabalho)
        print('SUCESSO :DDDD')
    except:
        print('ALGO DEU ERRADO :((((')
