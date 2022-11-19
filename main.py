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


from palenca import reportingPalenca

from metro import reportingMetro

from tottus import reportingTottus

# client = MongoClient()
# mongo = MongoClient(os.getenv("URL_MONGO"))






# Test


@app.route('/scrapers/<int:tipo>', methods=['GET', 'POST'])
def scrapers(tipo):
    if tipo == 1:
        print("en esta ruta")
        if request.method == 'POST':
            global created
            json = request.get_json()
            abriendo = json["ruta"]
            cadena = abriendo.split("/")
            tienda = cadena[2]
            print("TIENDA", tienda)            
            buscar = "null"
            # getFecha = loads(buscar)
            # try:
            #     print("entramos al try")
            #     # created = diferenviaDias(getFecha['created_at'])
            #     print("created", created)
            # except:
            #     created = 3
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
                print("cd")
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
        # return todas(json_forma)


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
