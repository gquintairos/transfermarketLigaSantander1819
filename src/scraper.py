# -*- coding: utf-8 -*-
"""
Created on Sat Apr 06 11:27:50 2019

@author: gquintairos
"""

#importamos las librerias necesarias
from bs4 import BeautifulSoup
import requests, csv

###leemos el fichero robots.txt
headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36'} #necesario para poder entrar en transfermarkt sin error 404
robots=requests.get('https://www.transfermarkt.es/robots.txt', headers=headers) #con esto le mandamos un GET a la URL donde esta el fichero robots.txt
soup_robots = BeautifulSoup(robots.content, 'html.parser') #leemos el html recibido y lo parseamos
print (soup_robots)

r=requests.get('https://www.transfermarkt.es/jumplist/startseite/wettbewerb/ES1', headers=headers) #con esto le mandamos un GET a la url de la pagina principal de la Liga Santander
soup = BeautifulSoup(r.content, 'html.parser') #leemos el html recibido y lo parseamos

equipos = soup.find_all("div", class_="grid-view") #con esto obtenemos los div donde estan los equipos y los leemos y guardamos en un array

direcciones = equipos[0].find_all(class_="vereinprofil_tooltip") #ahora dentro de cada equipo nos quedamos con el campo donde esta el enlace y los guardamos en un array

#esto sera necesario luego pues los href van por referencia en la web y les quitan el prefijo
prefix = "http://www.transfermarkt.es"

#Creamos el fichero donde vamos a escribir y rellenamos la cabecera
with open("../data/ligaSantander1819.csv", "w") as toWrite:
    writer = csv.writer(toWrite, delimiter=",", lineterminator='\n') #asignamos la coma como separador de campos y el \n como caracter de fin de linea
    writer.writerow(["equipo", "dorsal", "posicion", "nombre", "fecha de nacimiento (edad)", "nacionalidad", "valor de mercado"]) #escribimos una linea con la cabecera

i = 0
#NOTA: cada equipo ocupa 3 filas y no se por que. O sea que el primero lo leemos en la posicion 1, pero el segundo lo leemos en la posicion 4 y así sucesivamente
while i < (len(direcciones) - 1): #haremos un bucle que vaya leyendo el array direcciones, en el cual estan los enlaces correspondientes a la pagina de cada equipo
    element = direcciones[i] #le asignamos el enlace a una variable
    r_aux = requests.get(prefix + element["href"], headers=headers) #hacemos un GET a cada equipo, poniendo el prefijo seguido del enlace que obtuvimos antes
    soup_aux = BeautifulSoup(r_aux.content, 'html.parser') #leemos el html recibido y lo parseamos
    plantilla = soup_aux.find_all("div", class_="grid-view") #con esto obtenemos el div donde estan los jugadores y los leemos
    jugadores = plantilla[0].find_all("tr") #Aqui leemos todas las filas, en cada una esta un jugador. Debemos descartar la primera fila que son los titulos. Guardamos los jugadores en un array
    #NOTA: cada jugador ocupa 3 filas y no se por que. O sea que el primero lo leemos en la posicion 1, pero el segundo lo leemos en la posicion 4 y así sucesivamente
    j = 1
    while j < (len(jugadores) - 1): #hacemos otro bucle que vaya recorriendo el array donde hemos guardado la informacion de los jugadores
        with open("../data/ligaSantander1819.csv", "a") as toWrite: #para cada jugador, abrimos el fichero en modo escritura y añadimos una linea al final con los datos de ese jugador
            writer = csv.writer(toWrite, delimiter=",", lineterminator='\n') #de nuevo utilizamos la coma como separador de campos y el \n como caracter de fin de linea
            #utilizaremos la funcion find para obtener el contenido de cada etiqueta que queramos. utilizaremos la funcion get_text() para obtener el texto de un elemento que nos interese
            writer.writerow([soup_aux.find("div", class_="table-footer").find("a")["title"], jugadores[j].find("div", class_="rn_nummer").get_text(), jugadores[j+2].get_text(), 
                             jugadores[j].find("a", class_="spielprofil_tooltip").get_text(), jugadores[j].find_all(class_="zentriert")[1].get_text(),
                             jugadores[j].find_all(class_="zentriert")[2].find("img")["title"], jugadores[j].find(class_="rechts hauptlink").get_text()]) #escribimos una fila con los datos del jugador
        j += 3 #cada jugador ocupa 3 posiciones, por eso saltamos de 3 en 3
    i += 3 #cada equipo ocupa 3 posiciones, por eso saltamos de 3 en 3
