# Generated by Selenium IDE
# import pytest

import time
from lxml import etree 
import json
from bs4 import BeautifulSoup
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support import expected_conditions as ec
from pymongo import MongoClient


# client = MongoClient("mongodb+srv://user_jaime:XhA7pqTDWKfQy6Nh@micluster.pns9q58.mongodb.net")

# db  = client.get_database("tesis-won")

cliente=MongoClient('localhost')
db=cliente['tesis-won']


def BuscarMongo(coleccion ,valor):
    col = db[coleccion]
    try:
        id = col.find_one({"_id": valor})
        print("id", id)
        return id
    except NameError:
        print("ERROR")
        print(NameError)

def UpdateMongo(coleccion, valor, fechaExtraccionclean):
    col = db[coleccion]
    try:
        col.update_one({
            "_id": valor["_id"]
        },{
            "$set":{
                "_id":valor["_id"],
                "url": valor["url"],
                fechaExtraccionclean: valor[fechaExtraccionclean], 
            }
        }, upsert=True)
        print("Update Correct - Wong", valor)
        return True
    except NameError:
        print("ERROR")
        print(NameError)
        return False


def InsertarMongo(coleccion ,valor):
    col = db[coleccion]
    try:
        id = col.insert_one(valor)
        print("Insert Correct - Wong", valor)
        return id
    except NameError:
        print("ERROR")
        print(NameError)

class reportingPalenca():
    def __init__(self, objs):
        print(objs)
        self.objs = objs
        self.driver = webdriver.Remote(command_executor="http://192.168.54.215:4444/wd/hub", desired_capabilities=DesiredCapabilities.CHROME)
        self.vars = {}
        self.wait = WebDriverWait(self.driver, 10)

    def teardown_method(self):
        self.driver.quit()

    def logica(self):
    
        self.driver.get(self.objs)
        self.driver.maximize_window()        
        try:
            time.sleep(20)
            self.wait.until(ec.presence_of_element_located((By.XPATH, '/html/body/div[5]/div/div[3]/button[1]')))
            self.driver.find_element(By.XPATH, "/html/body/div[5]/div/div[3]/button[1]").click()
            time.sleep(5)
        except:
            time.sleep(2)


        numer= self.driver.find_element(By.XPATH, "/html/body/div[2]/div/div[1]/div/div[2]/div/div/section/div[2]/div/div/div/div[3]/section/div/div[2]/div/div/div/div/div[1]/div/div/div/div/div/div[3]/div/span").text

        asea = numer.split(' ')
        print(asea[0], type(int(float(asea[0]))))
        iteraciones  =  int(float(asea[0])) / 20
        iteraciones = int(iteraciones) + 2
        print("se dará ", iteraciones, "iteraciones")
        c=0
        while c< iteraciones :
            print("iteracion: ", c)
            self.driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
            time.sleep(4)
            c=c+1   
                                                        
        productos = self.driver.find_elements(By.XPATH, "/html/body/div[2]/div/div[1]/div/div[2]/div/div/section/div[2]/div/div/div/div[4]/div/div[2]/div/div[2]/div/div/div/div/div")

        print(productos, len(productos))  
        abriendo = self.objs
        fechaDateTime = datetime.now()
        fechaExtraccion = fechaDateTime.strftime("%Y-%m-%d %H:%M:%S")
        fechaExtraccion2 = fechaExtraccion.split(" ")
        fechaExtraccionclean = fechaExtraccion2[0]
        cadena = abriendo.split("/")
        tienda = cadena[2]
        categoria = cadena[3]
        subcategoria = ""
        try: 
            subcategoria = cadena[4]
        except:
            subcategoria = "Sin subcategoria"
        json = 0
        print("<----------------------------------------->")
        for producto in productos:
            nombre = ""
            url = ""
            precio = ""
            try:
                url = producto.find_element(By.XPATH, './section/a').get_attribute('href')
                # print(url)
                last = "0"
                try:
                    x = url.split("/")
                    nyc = x[3]
                    final = nyc.split("-")
                    last = final.pop()
                    last2 = final.pop()
                except:
                    print("error")
                nombre = producto.find_element(By.XPATH, './section/a/article/div[3]/h3/span').text
                cantidad = producto.find_elements(By.XPATH, './section/a/article/div')
                # print("cantidad", len(cantidad))
                if len(cantidad) == 10:
                    # print("nombre", nombre)
                    precio = producto.find_element(By.XPATH, './section/a/article/div[7]/div').text
                    precio = " ".join(precio.split())
                    # print("precio", precio)

                if len(cantidad) == 9:
                    # print("nombre", nombre)
                    precio = producto.find_element(By.XPATH, './section/a/article/div[6]').text
                    precio = " ".join(precio.split())
                    # print("precio", precio)
                if len(last) == 1:
                    json = {
                        "_id": last2,
                        "url": url, 
                        "nombre": nombre, 
                        "tienda": tienda,
                        fechaExtraccionclean : precio,
                        "categoria": categoria,
                        "subcategoria": subcategoria
                    }

                    busqueda  = BuscarMongo(categoria, last2)
                    respuesta = "null"
                    if busqueda:
                        UpdateMongo(categoria,json, fechaExtraccionclean)
                    else:
                        InsertarMongo(categoria , json)
                else:
                    json = {
                        "_id": last,
                        "url": url, 
                        "nombre": nombre, 
                        "tienda": tienda,
                        fechaExtraccionclean : precio,
                        "categoria": categoria,
                        "subcategoria": subcategoria
                    }
                    busqueda  = BuscarMongo(categoria, last)
                    respuesta = "null"
                    if busqueda:
                        respuesta  = UpdateMongo(categoria,json, fechaExtraccionclean)
                    else:
                        respuesta  = InsertarMongo(categoria , json)
                print("<----------------------------------------->")
            except:
                print("")
        self.driver.quit()
        # 
        return 0

        # self.driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
        # print("4")
        # repeticion = ""
        # estado = self.driver.find_element(By.XPATH, "/html/body/div[2]").get_attribute('style')
        # repeticion = estado.split()[1]
        # print("repeticion", repeticion)
        # while repeticion != "none;":
        #     self.driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
        #     time.sleep(1)
        #     self.driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
        #     estado = self.driver.find_element(By.XPATH, "/html/body/div[2]").get_attribute('style')
        #     repeticion = estado.split()[1]
        #     print("repeticion", repeticion, type(repeticion))
        #     if repeticion == "none;":
        #         self.driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
        #         time.sleep(1)
        #         self.driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
        #         estado = self.driver.find_element(By.XPATH, "/html/body/div[2]").get_attribute('style')
        #         repeticion = estado.split()[1]
        #     print("repeticion", repeticion, type(repeticion))
        #     print(repeticion != "none;")
        

       

        
     