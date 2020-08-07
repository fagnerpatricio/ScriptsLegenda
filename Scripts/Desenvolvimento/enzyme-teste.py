#!/usr/bin/env python

# Importações do Sistema
import argparse
import os
import enzyme
import natsort
import pysubs2

# Importações Personalizadas
# import LibAniHubSub

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Um programa de exemplo.', argument_default=argparse.SUPPRESS)

    parser.add_argument(
        '-ci',
        action='store',
        dest='ci',
        required=False,
        type=int,
        default=0,
        help='Indica o tempo inicial para começar a sincronização'
    )

    parser.add_argument(
        '-cf',
        action='store',
        dest='cf',
        required=False,
        type=int,
        default=-1,
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

        # LerAquivos
        dir_episodios = [x for x in os.listdir(argumentos.dir_trabalho) if (x.endswith(".mp4") or x.endswith(".mkv"))]
        dir_legendas = [x for x in os.listdir(argumentos.dir_trabalho) if x.endswith(".ass")]

        # Ordena Nomes
        dir_episodios = natsort.natsorted(dir_episodios, reverse=False)
        dir_legendas = natsort.natsorted(dir_legendas, reverse=False)

        # Resincroniza Legendas
        for ep, lg in zip(dir_episodios, dir_legendas):
            video = enzyme.MKV(open(argumentos.dir_trabalho + ep, 'rb'))
            tempo_inicial_sync = video.chapters[argumentos.ci].start.seconds * 1000
            tempo_final_sync = video.chapters[argumentos.cf].start.seconds * 1000
            subs = pysubs2.load(argumentos.dir_trabalho + lg, encoding="utf-8")

            for line in subs:
                if (line.start > tempo_inicial_sync) and (line.start < tempo_final_sync):
                    line.start += argumentos.deslocamento
                    line.end += argumentos.deslocamento
                    # print(line.text)

            subs.save(argumentos.dir_trabalho + lg)

        print('SUCESSO :DDDD')
    except:
        print('ALGO DEU ERRADO :((((')



