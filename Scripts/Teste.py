import ntpath
from matplotlib import font_manager
import re

print(font_manager.findfont('ComicNeue'))

line = 'Dialogue: 0,0:09:27.53,0:09:31.28,Signs,,0,0,0,,{\p1\pos(1194.6,481.2)\c&HF6F7F8&{m -233 -71 l -233 -71 l -210 -102 l -135 -140 l -46 -188 l -19 -200 l -2 -185 l -4 -112 l -231 -8 l -233 -71'
line2 = 'Dialogue: 0,0:07:13.74,0:07:16.24,Signs,,0,0,0,,{\blur1\fax0.03\move(1017,435,1056,435)\p1\c&H2F2628&\frz359.665}m 0 0 l 173 0 173 35 0 35{\p0}'

busca_padrao = line.split(re.findall('(?<=p1).*?(?=m)', line)[0])[1][2:].split(" ")


print(busca_padrao)
