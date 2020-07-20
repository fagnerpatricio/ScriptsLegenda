#!/usr/bin/env python

# Importações do Sistema
import argparse
import os
import natsort
import re
import shutil

# Importações Personalizadas
import LibAniHubSub

# dir_trabalho = '/media/Multimedia/Animes/Okami-san and Her Seven Companions/'
EXT_LEG = ".ass"
EXT_MKV = ".mkv"
EXT_MP4 = ".mp4"
TEMPORADA = "01"
FORMATO_NOME_EP = "Episode_S" + TEMPORADA + "_E"

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Um programa de exemplo.', argument_default=argparse.SUPPRESS)

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
        help='Indica a resolução em X'
    )

    parser.add_argument(
        '-ry',
        action='store',
        dest='res_y',
        required=False,
        help='Indica a resolução em Y'
    )

    parser.add_argument(
        '-ext',
        action='store',
        dest='extensao',
        required=False,
        help='Indica a extensao do arquivo a ser renomeado'
    )

    argumentos = parser.parse_args()

    nomes_atuais_episodios = [x for x in os.listdir(argumentos.dir_trabalho) if (x.endswith(EXT_MP4) or x.endswith(EXT_MKV))]
    nomes_atuais_episodios = natsort.natsorted(nomes_atuais_episodios, reverse=False)
    nomes_novos_episodios = ["Episode_S" + argumentos.temporada.zfill(2) + "_E" + str(c).zfill(2) for c, a in enumerate(nomes_atuais_episodios, 1)]

        dir_trabalho=argumentos.dir_trabalho,
        lista_de_nomes_antigos=nomes_atuais_episodios,
        lista_de_nomes_novos=nomes_novos_episodios,
        extensao=argumentos.extensao
    )

    # LibAniHubSub.dir_bak_leg(
    #     dir_trabalho=argumentos.dir_trabalho,
    #     arquivos_de_legenda=os.listdir(argumentos.dir_trabalho)
    # )

    # LibAniHubSub.tratamento_legendas(
    #     dir_trabalho=argumentos.dir_trabalho,
    #     arquivos_de_legenda=os.listdir(argumentos.dir_trabalho + '/' + LibAniHubSub.CONFIG["dirLegendaAntiga"]),
    #     res_x=argumentos.res_x,
    #     res_y=argumentos.res_y
    # )

    # # LerAquivos
    # arq_episodios = [x for x in os.listdir(argumentos.dir_trabalho) if (x.endswith(EXT_MP4) or x.endswith(EXT_MKV))]
    # arq_legendas = [x for x in os.listdir(argumentos.dir_trabalho) if x.endswith(EXT_LEG)]

    # arq_episodios = natsort.natsorted(arq_episodios, reverse=False)
    # arq_legendas = natsort.natsorted(arq_legendas, reverse=False)

    # for c, a in enumerate(arq_episodios, 1):
    #     shutil.move(argumentos.dir_trabalho + a, argumentos.dir_trabalho + "Episode_S" +
    #                 argumentos.temporada.zfill(2) + "_E" + str(c).zfill(2) + EXT_MKV)

    # for c, a in enumerate(arq_legendas, 1):
    #     shutil.move(argumentos.dir_trabalho + a, argumentos.dir_trabalho + "Episode_S" +
    #                 argumentos.temporada.zfill(2) + "_E" + str(c).zfill(2) + ".ptBR" + EXT_LEG)

    print("SUCESSO")
