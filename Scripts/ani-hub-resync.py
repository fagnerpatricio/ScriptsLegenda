#!/usr/bin/env python

#Importações do Sistema
import argparse
import os

#Importações Personalizadas
import LibAniHubSub

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Um programa de exemplo.', argument_default=argparse.SUPPRESS)

    parser.add_argument(
        '-hi',
        action='store',
        dest='hi',
        required=False,
        type=int,
        default=0,
        help='Indica o tempo inicial para começar a sincronização'
    )

    parser.add_argument(
        '-mi',
        action='store',
        dest='mi',
        required=False,
        type=int,
        default=0,
        help='Indica o tempo inicial para começar a sincronização'
    )

    parser.add_argument(
        '-si',
        action='store',
        dest='si',
        required=False,
        type=int,
        default=0,
        help='Indica o tempo inicial para começar a sincronização'
    )

    parser.add_argument(
        '-hf',
        action='store',
        dest='hf',
        required=False,
        type=int,
        default=0,
        help='Indica o tempo inicial para começar a sincronização'
    )

    parser.add_argument(
        '-mf',
        action='store',
        dest='mf',
        required=False,
        type=int,
        default=0,
        help='Indica o tempo inicial para começar a sincronização'
    )

    parser.add_argument(
        '-sf',
        action='store',
        dest='sf',
        required=False,
        type=int,
        default=0,
        help='Indica o tempo inicial para começar a sincronização'
    )

    parser.add_argument(
        '-des',
        action='store',
        dest='deslocamento',
        required=False,
        type=int,
        default=0,
        help='Indica o tempo inicial para começar a sincronização'
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

        # lista_de_episodios_tvmaze = LibAniHubSub.baixa_tvmaze_legendas(argumentos.cod_tvmaze)

        LibAniHubSub.resincroniza_legendas(
            dir_trabalho=argumentos.dir_trabalho,
            h=argumentos.hi,
            m=argumentos.mi,
            s=argumentos.si,
            delta_deslocamento=argumentos.deslocamento
        )

        print('SUCESSO :DDDD')
    except:
        print('ALGO DEU ERRADO :((((')
