import ntpath
from matplotlib import font_manager
import re

print(font_manager.findfont('ComicNeue'))

lines = [
    '0,0:01:09.50,0:01:12.38,Logo,,0,0,0,,{\clip(m 460 118 l 609 118 609 118 460 118)\pos(535,137)\bord3\shad0\blur1.5\fnSubway\fs19.667\c&HF5C110&\3c&HFFFFFF&\alpha&HFF&\t(0,253,1,\alpha&H00&)}Infinite Fansub',
    'Dialogue: 0,0:04:10.73,0:04:14.98,Title,,0,0,0,,{\clip(648,768,1277,771)\pos(320,275)\1c&HF9E902&}Equipe E601'
]


escala = 0.5
for line in lines:
    try:
        busca_padrao = re.findall(r'(pos|clip)\((.+?)\)', line)

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

