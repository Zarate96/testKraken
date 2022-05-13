'''
Devuelve un archivo products.txt con los resultados del scrapping de la lista de urls
incluido en el archivo categories.txt
'''

#librerias
import requests
import json
import threading
import lxml
import requests
from bs4 import BeautifulSoup as bs
from multiprocessing.pool import ThreadPool as Pool

#lista para guardar urls a reccorer
urls = []

#Leer archvio de categoires.txt para llenar lista urls
with open("categories.txt", "r") as file:
    for readline in file: 
        urls.append(readline.strip())

#definir el tamña del pool de acuerdo a list urls
pool_size = len(urls)

#definir lista de url para obtener primeras 10 paginas
indexList = ['','_Desde_50_NoIndex_True','_Desde_100_NoIndex_True','_Desde_150_NoIndex_True','_Desde_200_NoIndex_True','_Desde_250_NoIndex_True','_Desde_300_NoIndex_True',
            '_Desde_350_NoIndex_True','_Desde_400_NoIndex_True','_Desde_450_NoIndex_True']

def getData(urlBase):
    '''
    Agregar a archivo products.txt los elementos con la clase ui-search-result__wrapper
    que son los prodcutos
    '''
    for page in indexList:
        req = requests.get(urlBase + str(page)).text
        soup = bs(req, "lxml")
        elements = soup.find_all('div',attrs={'class','ui-search-result__wrapper'})
        with open('products.txt', 'a') as f:
            f.write(str(elements))

#crear pool
pool = Pool(pool_size)

#ejecutar pool para obtner los productos de cada categoria.
for url in urls:
    pool.apply_async(getData, (url,))

pool.close()
pool.join()

