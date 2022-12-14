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
# db  = client.get_database("tesis-metro")

cliente=MongoClient('localhost')
db=cliente['tesis-metro']


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
        print("Update Correct - Metro", valor)
        return True
    except NameError:
        print("ERROR UPDATE")
        print(NameError)
        return False


        
def InsertarMongo(coleccion ,valor):
    col = db[coleccion]
    try:
        id = col.insert_one(valor)
        print("Insert Correct - Metro", valor)
        return id
    except NameError:
        print("ERROR INSERT")
        print(NameError)
        

class reportingMetro():
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
            time.sleep(10)
            print("click cookis")
            self.wait.until(ec.presence_of_element_located((By.XPATH, '/html/body/div[29]/div/div[3]/button[1]')))
            self.driver.find_element(By.XPATH, "/html/body/div[29]/div/div[3]/button[1]").click()
            print("fin click")
        except:
            print("ERROR cookis")
            time.sleep(2)
        

        try:
            print("click modal")
            self.wait.until(ec.presence_of_element_located((By.XPATH, '/html/body/div[30]/div/div/div[2]/button[2]')))
            self.driver.find_element(By.XPATH, "/html/body/div[30]/div/div/div[2]/button[2]").click()
            print("fin click ")
        except:
            print("ERRO modal")
            time.sleep(2)

        try:
            print("click modal")
            self.wait.until(ec.presence_of_element_located((By.XPATH, '/html/body/div[29]/div/div/div[2]/button[2]')))
            self.driver.find_element(By.XPATH, "/html/body/div[30]/div/div/div[2]/button[2]").click()
            print("fin click ")
        except:
            print("ERRO modal")
            time.sleep(2)



        self.driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
        repeticion = ""
        estado = self.driver.find_element(By.XPATH, "/html/body/div[26]/div/div[2]/div[7]/div[1]").get_attribute('style')
        repeticion = estado.split()[1]
        while repeticion != "none;":
            self.driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
            time.sleep(1)
            self.driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
            estado = self.driver.find_element(By.XPATH, "/html/body/div[26]/div/div[2]/div[7]/div[1]").get_attribute('style')
            repeticion = estado.split()[1]
            if repeticion == "none;":
                self.driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
                time.sleep(1)
                self.driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
                estado = self.driver.find_element(By.XPATH, "/html/body/div[26]/div/div[2]/div[7]/div[1]").get_attribute('style')
                repeticion = estado.split()[1]

        
        productos = self.driver.find_elements(By.XPATH, "/html/body/div[26]/div/div[2]/div[7]/div[2]/div[2]/div[2]/div/ul/li")
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
            nombre = ""
            url = ""
            precio = ""
            data_id = ""
            data_sku = ""
            try:
                url = producto.find_element(By.XPATH, './div').get_attribute('data-uri')
                data_id = producto.find_element(By.XPATH, './div').get_attribute('data-id')
                data_sku = producto.find_element(By.XPATH, './div').get_attribute('data-sku')
                marca = producto.find_element(By.XPATH, './div').get_attribute('data-brand')
                nombre = producto.find_element(By.XPATH, './div[1]/div[3]/div[1]/a').text
                precio = producto.find_element(By.XPATH, './div[1]/div[3]/div[2]/div[2]/span[2]').text
                json = {
                    "_id": data_id,
                    "_id2": data_sku,
                    "url": url, 
                    "nombre": nombre, 
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
        self.driver.quit()
        return 0
        
      
        




        