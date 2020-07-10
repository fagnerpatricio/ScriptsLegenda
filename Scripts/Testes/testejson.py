import json

file = open('/home/fagner/ProjetosVSCode/anisubhub/legendasotaku/siteweb/templates/anime.json','r')

data = json.load(file)

print(data)
