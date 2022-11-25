# Generated by Selenium IDE
# import pytest
from http import client

import time

from selenium import webdriver
from datetime import datetime
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support import expected_conditions as ec
from pymongo import MongoClient


# client = MongoClient("mongodb+srv://user_jaime:XhA7pqTDWKfQy6Nh@micluster.pns9q58.mongodb.net")
# db  = client.get_database("tesis-tottus")
cliente=MongoClient('localhost')
db=cliente['tesis-tottus']

def BuscarMongo(coleccion ,valor):
    col = db[coleccion]
    try:
        id = col.find_one({"_id": valor})
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
                "_id2": valor["_id2"],
                "url": valor["url"],
                "nombre": valor["nombre"],
                fechaExtraccionclean : valor[fechaExtraccionclean],
            }
        }, upsert=True)
        print("Update Correct - Tottus", valor)
        return True
    except NameError:
        print("ERROR")
        print(NameError)
        return False


        
def InsertarMongo(coleccion ,valor):
    col = db[coleccion]
    try:
        id = col.insert_one(valor)
        print("Insert Correct - tottus", valor)
        return id
    except NameError:
        print("ERROR")
        print(NameError)
        

class reportingTottus():
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
        condicion = "next"
        it = 1
        while( condicion == "next" ):
            try:
                time.sleep(10)
                filas = self.driver.find_elements(By.XPATH, "/html/body/div[1]/section/div[1]/section/div[1]/div[3]/ul/li")
                utlimo = filas.pop()
                condicion = utlimo.get_attribute('class')
            except:
                condicion = "null"
            self.driver.execute_script("window.scrollTo(0, window.scrollY + 900)")
            time.sleep(4)
            self.driver.execute_script("window.scrollTo(0, window.scrollY + 900)")
            time.sleep(4)
            self.driver.execute_script("window.scrollTo(0, window.scrollY + 900)")
            time.sleep(4)
            self.driver.execute_script("window.scrollTo(0, window.scrollY + 900)")
            productos = self.driver.find_elements(By.XPATH, "/html/body/div[1]/section/div[1]/section/div[2]/div[2]/ul[1]/li")
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
            
            for producto in productos:
                print("producto", it)
                nombre = ""
                url = ""
                precio = ""
                data_id = ""
                data_sku = ""
                try:
                    url = producto.find_element(By.XPATH, './section/div/a').get_attribute('href')
                    data_id = producto.find_element(By.XPATH, './section').get_attribute('class').split(" ")[2]
                    img = producto.find_element(By.XPATH, './section/div/a/div[1]/img').get_attribute('src')
                    marca = ""
                    nombre = ""
                    try:
                        marca = producto.find_element(By.XPATH, './section/div/a/div[2]/h3').text
                        nombre = producto.find_element(By.XPATH, './section/div/a/div[2]/h2').text
                    except:
                        marca = producto.find_element(By.XPATH, './section/div/a/div[3]/h3').text
                        nombre = producto.find_element(By.XPATH, './section/div/a/div[3]/h2').text
                    precio = producto.find_element(By.XPATH, './section/div/div[4]/span/span').text
                    json = {
                        "_id": data_id,
                        "_id2": data_sku,
                        "url": url, 
                        "nombre": nombre, 
                        "img": img,
                        fechaExtraccionclean: precio,
                        "marca": marca,
                        "tienda": tienda,
                        "categoria": categoria,
                        "subcategoria": subcategoria
                    }
                    busqueda  = BuscarMongo(categoria, data_id)
                    if busqueda:
                        UpdateMongo(categoria,json, fechaExtraccionclean)
                    else:
                        InsertarMongo(categoria , json)
                except:
                    print("")
            
                it = it + 1
            try:

                self.driver.execute_script("window.scrollTo(0, window.scrollY - 3700)")
                time.sleep(3)
                try:
                    self.wait.until(ec.presence_of_element_located((By.XPATH, '/html/body/div[5]/div/div/div[2]/button[2]'))) 
                    self.driver.find_element(By.XPATH, "/html/body/div[5]/div/div/div[2]/button[2]").click()
                except:
                    pass
                utlimo.click()
            except:
                condicion = "null"

           
        self.driver.quit()
        return 0   
        
      
        




        