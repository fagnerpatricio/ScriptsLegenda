import ntpath
from matplotlib import font_manager
import re

print(font_manager.findfont('ComicNeue'))

lines = [
   r'Dialogue: 0,0:01:31.50,0:01:33.94,Signs,,0,0,0,,{\fad(510,0)\an7\blur0.5\fs21.500\3c&H9B3FAB&\fnImpress BT\bord0.1\b1\p1\fscx80\fscy80\c&HA43973&\pos(-20,176)}m 48 162 b 48 162 48 162 48 162 b 48 162 48 162 48 162 b 58 143 72 134 90 136 b 76 148 88 159 96 157 b 88 160 86 164 86 171 b 83 164 76 164 71 174 b 75 152 65 152 48 162  {\p0}'
]
# lines = [
#     '0,0:01:09.50,0:01:12.38,Logo,,0,0,0,,{\clip(m 460 118 l 609 118 609 118 460 118)\pos(535,137)\bord3\shad0\blur1.5\fnSubway\fs19.667\c&HF5C110&\3c&HFFFFFF&\alpha&HFF&\t(0,253,1,\alpha&H00&)}Infinite Fansub',
#     'Dialogue: 0,0:04:10.73,0:04:14.98,Title,,0,0,0,,{\clip(648,768,1277,771)\pos(320,275)\1c&HF9E902&}Equipe E601'
# ]



escala = 0.5
for line in lines:

    try:
        # busca_padrao = re.findall(r'(pos|clip)\((.+?)\)', line)
        # busca_padrao = re.findall(r'fs([0-9]+)',line)

        # b = [tuple(i for i in m if i) for m in re.findall(r'(p[1-4])\\(.+?)(?={)|(pos|move|org|clip)\((.+?)\)|fs([0-9]+.?[0-9]+)?',line)]

        # busca_padrao = re.findall(r'(p[1-4])\\(.+?)(?={)', line)

        # novos_valores = []
        # print(type(line))
        # t = re.findall(r'(?P<tag>(fs|clip))+',line)
        busca_de_padroes = [tuple(i for i in m if i) for m in re.findall(r'[\\|\(|\}](m)(\s.+?)[\)|\{]|(pos|move|org|clip)(\()(.+?)\)|(fs)(\d+\.?\d+)',line)]

        n = lambda v: str("{:.3f}".format(float(v) * escala)) if v.replace('.','').lstrip('-').isdigit() else v
        j = lambda x: " ".join([n(c) for c in re.split(r'[,\s]\s*', x[-1:][0])]) if x[0] == 'm' else ",".join([n(c) for c in re.split(r'[,\s]\s*', x[-1:][0])])
        for padrao in busca_de_padroes:
            try:
                line = line.replace("".join(padrao),"".join(padrao[:-1]) + j(padrao))
                # line = line.replace("".join(padrao),"".join(padrao[:-1]) + " ".join([n(c) for c in re.split(r'[,\s]\s*', padrao[-1:][0])]))
                # if any(padrao[0] == y for y in ('pos','move','org')):
                #     line = line.replace((padrao[1]),','.join(["{:.3f}".format(float(c) * escala) for c in padrao[1].split(',')]))
                # elif any(padrao[0] == y for y in ('clip','p1','p2','p3','p4')):
                #     n = lambda v: str("{:.3f}".format(float(v) * escala)) if v.isdigit() else v
                #     line = line.replace((padrao[1])," ".join([n(c) for c in re.split(r'[,\s]\s*', padrao[1])]))
                    # t3 = re.split(r'[,\s]\s*', padrao[1])
                    # for c in t3:
                    #     if c.isdigit():
                    #         print("{:.3f}".format(float(c) * escala))
                    #     print(c.isdigit())
                    # t2 = [n(c) for c in t3]
                    # t = " ".join([n(c) for c in re.split(r'[,\s]\s*', padrao[1])])
                    # print(line)
                    # valores = padrao[1].split(' ')
                    # novo_valor = []
                    # n = lambda v: str("{:.3f}".format(float(valor) * escala)) if v.isdigit() else v
                    # for valor in valores:
                    #     novo_valor.append(n(valor))
                    #     # try:
                    #     #     novo_valor.append(str("{:.3f}".format(float(valor) * escala)))
                    #     # except:
                    #     #     novo_valor.append(valor)
                    #     #     continue
                    # line = line.replace(padrao[1], " ".join(novo_valor))
                    # print(" ".join(novo_valor))
            except:
                continue

                # padrao = padrao[1].split(',')
                    # for coordenadas in padrao[1].split(','):
                    # # for coordenadas in [padrao[i: i+2] for i in range(0, len(padrao), 2)]:
                    #     line = line.replace(padrao[1]),','.join(["{:.3f}".format(float(c) * escala) for c in padrao[1].split(',')]))
                        # n = ["{:.3f}".format(float(c) * escala) for c in coordenadas]
                        # novas_coordenadas = []
                        # novas_coordenadas.append("{:.3f}".format(float(coordenadas[0]) * escala))
                        # novas_coordenadas.append("{:.3f}".format(float(coordenadas[1]) * escala))
                        # c = ",".join(coordenadas)
                        # line = line.replace(coordenadas[0] + ',' + coordenadas[1], ','.join(novas_coordenadas))
        print(line)

        # if busca_padrao[0][0] == 'm':
        #     antigos_valores = busca_padrao[0].split('m')[1].split(" ")[1:]
        #     novo_valor = ''
        #     for valor in antigos_valores:
        #         try:
        #             novo_valor += str("{:.0f}".format(float(int(valor) * escala)) + ',')
        #         except:
        #             novo_valor += valor + ','
        #             continue
        #         novo_valor = novo_valor.replace(','," ")
        #     line = line.replace(busca_padrao[0].split('m')[1]," " + novo_valor[:-1])
        #     print(line)
        # else:
            # busca_padrao = busca_padrao[0].split(',')

            # for coordenadas in [busca_padrao[i:i + 2] for i in range(0, len(busca_padrao), 2)]:
            #     novas_coordenadas = []
            #     novas_coordenadas.append("{:.0f}".format(float(coordenadas[0]) * escala))
            #     novas_coordenadas.append("{:.0f}".format(float(coordenadas[1]) * escala))
            #     lista_de_novas_cordenada = ','.join(novas_coordenadas)
            #     antigas_coordenadas = coordenadas[0] + ',' + coordenadas[1]
            #     line = line.replace(antigas_coordenadas, lista_de_novas_cordenada)
            # print(line)
    except:
        continue

