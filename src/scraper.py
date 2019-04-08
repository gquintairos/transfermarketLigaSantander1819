# -*- coding: utf-8 -*-
"""
Created on Sat Apr 06 11:27:50 2019

@author: gquintairos
"""

from bs4 import BeautifulSoup
import requests, csv
#import sys
#reload(sys)
#sys.setdefaultencoding('utf8')

headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36'} #necesario para poder entrar en transfermarkt sin error 404
r=requests.get('https://www.transfermarkt.es/jumplist/startseite/wettbewerb/ES1', headers=headers) #con esto le mandamos un GET a la url indicada
soup = BeautifulSoup(r.content, 'html.parser') #leemos el html recibido y lo parseamos

equipos = soup.find_all("div", class_="grid-view") #con esto pillamos los div donde estan los equipos y los leemos

direcciones = equipos[0].find_all(class_="vereinprofil_tooltip") #ahora dentro de cada equipo nos quedamos con el campo donde esta el enlace

#esto sera necesario luego pues los href van por referencia en la web y les quitan el prefijo
prefix = "http://www.transfermarkt.es"

#Creamos el fichero donde vamos a escribir y rellenamos la cabecera
with open("../data/ligaSantander1819.csv", "w") as toWrite:
    writer = csv.writer(toWrite, delimiter=",", lineterminator='\n')
    writer.writerow(["equipo", "dorsal", "posicion", "nombre", "fecha de nacimiento (edad)", "nacionalidad", "valor de mercado"])

i = 0
while i < (len(direcciones) - 1):
    element = direcciones[i]
    r_aux = requests.get(prefix + element["href"], headers=headers) #hacemos un GET a cada equipo, poniendo el prefijo seguido del enlace que obtuvimos antes
    soup_aux = BeautifulSoup(r_aux.content, 'html.parser') #leemos el html recibido y lo parseamos
    plantilla = soup_aux.find_all("div", class_="grid-view") #con esto pillamos el div donde estan los jugadores y los leemos
    jugadores = plantilla[0].find_all("tr") #Aqui leemos fila por fila donde esta cada jugador, debemos descartar la primera fila que son los titulos
    #NOTA: cada jugador ocupa 9 filas y no se por que. O sea que el primero lo leemos en la posicion 1, pero el segundo lo leemos en la posicion 10 y así sucesivamente
    j = 1
    while j < (len(jugadores) - 1):
        with open("../data/ligaSantander1819.csv", "a") as toWrite:
            writer = csv.writer(toWrite, delimiter=",", lineterminator='\n')
            writer.writerow([soup_aux.find("div", class_="table-footer").find("a")["title"], jugadores[j].find("div", class_="rn_nummer").get_text(), jugadores[j+2].get_text(), 
                             jugadores[j].find("a", class_="spielprofil_tooltip").get_text(), jugadores[j].find_all(class_="zentriert")[1].get_text(),
                             jugadores[j].find_all(class_="zentriert")[2].find("img")["title"], jugadores[j].find(class_="rechts hauptlink").get_text()])
        j += 3
    i += 3
