'''
Devuelve archivo listProducts.json con Descripción, Imagen Url, Precio y Precio anterior
de cada uno de los productos obtenitos por el scrapping.

Es necesario tener el archivo products.txt generado con el archvio getData.py
'''

#Librerias
import requests
from bs4 import BeautifulSoup as bs
import json
import threading
import re

#Lectura de archvio products.txt
with open("products.txt","r") as page:
	soup = bs(page, 'html.parser')

#Lista final para guardar información de los prodcutos
dataFinal = []

def getData(product):
	'''
	Crea un diccionario con la información del producto

	prodcut: parametro de tipo bs
	
	retorna un diccionario con la información del producto
	'''
	productFinal = {}
	productData = bs(str(product), 'html.parser')

	#Iteraciones para obtener la información
	for description in productData.find_all("h2", {"class": "ui-search-item__title"}):
		productFinal['Description'] = description.text
	
	for img in productData.find_all("img", {"class": "ui-search-result-image__element"}):
		productFinal['ImageURL'] = img['data-src']
		
	for price in productData.find_all(text=re.compile("pesos")):
		if not price.text[0] == 'A':
			productFinal['Price'] = price.text

	for price in productData.find_all(text=re.compile("Antes: ")):
		productFinal['Old price'] = price.text
	
	return productFinal

#Iterar sobres los productos obtenidos con el scrapping.
for product in soup.find_all("div", {"class": "ui-search-result__wrapper"}):
	productFinal = getData(product)
	dataFinal.append(productFinal)

#Guardar en archvio json la información
with open("listProducts.json", "w") as writeJSON:
    json.dump(dataFinal, writeJSON, ensure_ascii=False, indent=4)
	

