import json

access = '{\"fontname\":\"Fira Sans\",\"fontsize\":22,\"backcolor\":[0,0,0,0],\"outlinecolor\":[25,25,25,0],\"secondarycolor\":[0,0,255,0],\"primarycolor\":[255,255,255,0],\"bold\":-1,\"italic\":0,\"underline\":0,\"strikeout\":0,\"scalex\":100,\"scaley\":100,\"spacing\":0,\"angle\":0,\"borderstyle\":1,\"outline\":2,\"shadow\":1,\"alignment\":2,\"marginl\":40,\"marginr\":40,\"marginv\":15,\"encoding\":0}'

secret = "XXX"

dct = {'Default': access,'D2': access}

json_str = json.dumps(dct, indent=True)
print (json_str)
