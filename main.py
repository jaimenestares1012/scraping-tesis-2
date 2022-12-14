# -*- coding: utf-8 -*-
from dotenv import load_dotenv
# import dotenv
import os
from pathlib import Path  # python3 only
import sys
from app import app
import json
from datetime import datetime
import unicodedata
from bson.objectid import ObjectId
from bson.json_util import dumps, loads
from pymongo import MongoClient
import re
from unicodedata import normalize
from flask import Flask, request

from datetime import datetime
import time


from palenca import reportingPalenca

from metro import reportingMetro

from tottus import reportingTottus


from reporting import reporteTipo1

# client = MongoClient()
# mongo = MongoClient(os.getenv("URL_MONGO"))






# Test


@app.route('/scrapers/<int:tipo>', methods=['GET', 'POST'])
def scrapers(tipo):
    print("inico sleep")
    time.sleep(5)
    print("fin sleep")
    if tipo == 1:
        if request.method == 'POST':
            global created
            json = request.get_json()
            abriendo = json["ruta"]
            cadena = abriendo.split("/")
            tienda = cadena[2]         
            buscar = "null"
            if tienda == 'www.wong.pe':
                print("<--------------------------- INICIO ESCRAPING WON ------------------------->")
                inicio = reportingPalenca(json["ruta"]) 
                try:
                    response = inicio.logica()
                    if response == 0:
                        json={
                            "codRes": "00",
                            "detalle": "Se hizo el scraping de manera correcta",
                            "return": response,
                            "url": json["ruta"]
                        }
                        return dumps(json)
                except: 
                    json={
                        "codRes": "99",
                        "detalle": "Hubo un error",
                        "detalle": "",
                        "url": json["ruta"]
                    }
                    return dumps(json)

            if tienda == 'www.metro.pe':
                print("<--------------------------- INICIO ESCRAPING METRO ------------------------->")
                inicio = reportingMetro(json["ruta"]) 
                try:
                    response = inicio.logica()
                    if response == 0:
                        json={
                            "codRes": "00",
                            "detalle": "Se hizo el scraping de manera correcta",
                            "return": response,
                            "url": json["ruta"]
                        }
                        return dumps(json)
                except: 
                    json={
                        "codRes": "99",
                        "detalle": "Hubo un error",
                        "detalle": "",
                        "url": json["ruta"]
                    }
                    return dumps(json)
            



            if tienda == "www.tottus.com.pe":
                print("<--------------------------- INICIO ESCRAPING TOTTUS ------------------------->")
                
                inicio = reportingTottus(json["ruta"]) 
                try:
                    response = inicio.logica()
                   
                    if response == 0:
                        json={
                            "codRes": "00",
                            "detalle": "Se hizo el scraping de manera correcta",
                            "return": response,
                            "url": json["ruta"]
                        }
                        return dumps(json)
                except: 
                    json={
                        "codRes": "99",
                        "detalle": "Hubo un error",
                        "detalle": "",
                        "url": json["ruta"]
                    }
                    return dumps(json)
            else:
                return buscar
    elif tipo == 2:
        print("opcion 2")
    else:
        return 'Tipo incorrecto'

@app.route('/get/data/<int:tipo>', methods=['GET', 'POST'])
def getData(tipo):
    if tipo == 1:
        print("es tipo 1", tipo)
        json = request.get_json()
        producto = json["nombreProducto"]
        categoria = json["categoria"]
        inicio = reporteTipo1( producto, categoria) 
        datos = inicio.logica()
        data={
            "codRes": "00",
            "detalle": "??xito",
            "data": datos
        }
        return data
    elif tipo == 2:
        print("tipo 2")
    else:
        return "tipo incorrecto"

try:
    enviro = sys.argv[1]
    if enviro == "dev":
        env_path = Path('.') / '.env.dev'
        load_dotenv(dotenv_path=env_path)
        print(os.getenv('ENVIRO'))
    if enviro == "pro":
        env_path = Path('.') / '.env.pro'
        load_dotenv(dotenv_path=env_path)
        print(os.getenv('ENVIRO'))
    if __name__ == '__main__':
        # app.run()
        app.run(host='0.0.0.0', debug=True)
except:
    print("Debe definir el entorno dev o pro (ejm: python app.py dev)")
    # print(NameError)
