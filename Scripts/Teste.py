import ntpath
from matplotlib import font_manager
import re

print(font_manager.findfont('ComicNeue'))

lines = [
    '\clip(m 460 118 l 609 118 609 118 460 118){\\blur1\\fs23\\olap1\m m 0 0 l 300 0 300 45 0 45{\p0}\
    pos(535,137)\clip(648,768,1277,771)\pos(320,275)\clip(m 460 118 l 609 118 609 119 460 19)\pos(535,137)\
    move(508,218,528,218)\move(508,218,528,218){\blur1\p1\m m 0 0 l 300 0 300 45 0 45{\p0}\\fs22.500'
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

        novos_valores = []
        busca_de_padroes = [tuple(i for i in m if i) for m in re.findall(r'(p[1-4])\\(.+?)(?={)|(pos|move|org|clip)\((.+?)\)|fs([0-9]+.?[0-9]+)?',line)]

        for padrao in busca_de_padroes:
            try:
                if any(padrao[0] == y for y in ('pos','move','org')):
                    line = line.replace((padrao[1]),','.join(["{:.3f}".format(float(c) * escala) for c in padrao[1].split(',')]))
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
                elif any(padrao[0] == y for y in ('clip','p1','p2','p3','p4')):
                    valores = padrao[1].split(' ')
                    novo_valor = []
                    for valor in valores:
                        try:
                            novo_valor.append(str("{:.3f}".format(float(valor) * escala)))
                        except:
                            novo_valor.append(valor)
                            continue
                    line = line.replace(padrao[1], " ".join(novo_valor))
                    print(" ".join(novo_valor))
            except:
                continue

        print(line)

        if busca_padrao[0][0] == 'm':
            antigos_valores = busca_padrao[0].split('m')[1].split(" ")[1:]
            novo_valor = ''
            for valor in antigos_valores:
                try:
                    novo_valor += str("{:.0f}".format(float(int(valor) * escala)) + ',')
                except:
                    novo_valor += valor + ','
                    continue
                novo_valor = novo_valor.replace(','," ")
            line = line.replace(busca_padrao[0].split('m')[1]," " + novo_valor[:-1])
            print(line)
        else:
            busca_padrao = busca_padrao[0].split(',')

            for coordenadas in [busca_padrao[i:i + 2] for i in range(0, len(busca_padrao), 2)]:
                novas_coordenadas = []
                novas_coordenadas.append("{:.0f}".format(float(coordenadas[0]) * escala))
                novas_coordenadas.append("{:.0f}".format(float(coordenadas[1]) * escala))
                lista_de_novas_cordenada = ','.join(novas_coordenadas)
                antigas_coordenadas = coordenadas[0] + ',' + coordenadas[1]
                line = line.replace(antigas_coordenadas, lista_de_novas_cordenada)
            print(line)
    except:
        continue

