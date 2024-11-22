from http.client import responses

import requests
import json


#url = "https://mindicador.cl/api"

#response = requests.get(url)
#data = json.loads(response.text.encode("utf-8"))
#pretty_json = json.dumps(data, indent=2)
#print(pretty_json)

def divisaFunction(divisa,fecha):
    url = f"https://mindicador.cl/api/{divisa}/{fecha}"

    response = requests.get(url)
    datafecha = response.json()
    valor = None
    pretty_json = json.dumps(datafecha, indent=2)
    print(pretty_json)

    try:
        valor = datafecha["serie"][0]["valor"]
    except(KeyError, IndexError):
        valor = None
        return valor

    if divisa == "ipc":
        porcentaje = valor
        valor = "{}%".format(porcentaje)

    print(valor)

    return valor

divisaFunction("ipc","11-11-2024")