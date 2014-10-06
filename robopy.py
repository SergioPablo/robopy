# -*- coding: utf-8 -*-
__author__ = 'sergiopablo'
import itertools
import random

# ACÁ SE CREA EL MAPA A PARTIR DEL ARCHIVO 'mapa'
def crear_mapa():
    archivo = open('mapa')
    mapa = list()
    for linea in archivo:
        mapa.append((list(map(int,linea.strip().split('   ')))))
    return mapa

# ACÁ SE DEFINE EL NUMERO TOTAL DE FILAS Y COLUMNAS
filas = 3
columnas = 4

# ESTA FUNCION BUSCA UN PUNTO "p" EN UN MAPA EN FORMA DE LSITA Y RETORNA LA COORDENADA
def buscar_punto(p, lista):
    columna_actual = 0
    fila_actual = 0
    for fila in lista:
        for punto in fila:
            if punto == p:
                return [columna_actual, fila_actual]
            columna_actual += 1
        fila_actual += 1
        columna_actual = 0

# ESTA FUNCION RECIBE LA COORDENADA ACTUAL Y LA DIRECCION EN FORMA DE STRING Y RETORNA LA NUEVA COORDENADA ACTUAL DEL ROBOT
def moverse(coord_actual, dir):
    diccionario_prob = {"N": ['N','N','N','N','N','N','N','N','E','O'],
                    "S": ['S','S','S','S','S','S','S','S','E','O'],
                    "E": ['E','E','E','E','E','E','E','E','N','S'],
                    "O": ['O','O','O','O','O','O','O','O','N','S'],
                    }

    direccion = random.choice(diccionario_prob[dir])
    prob = 0
    if direccion == dir:
        prob = 0.8
    else:
        prob = 0.1

    coord_nueva = coord_actual
    coord_vieja = coord_nueva
    if direccion == 'N':
        coord_nueva = [coord_actual[0],coord_actual[1]+1]
    elif direccion == "S":
        coord_nueva = [coord_actual[0],coord_actual[1]-1]
    elif direccion == 'E':
        coord_nueva = [coord_actual[0]+1,coord_actual[1]]
    elif direccion == 'O':
        coord_nueva = [coord_actual[0]-1,coord_actual[1]]

    if coord_nueva == coord_pared:

        return (coord_vieja, prob)

    elif (coord_nueva[0] >= 0 and coord_nueva[1] >= 0) and (coord_nueva[0] < columnas and coord_nueva[1] < filas):
        return (coord_nueva, prob)
    else:
        return (coord_vieja, prob)


def crear_diccionario_mapa(politica):
    diccionario_celdas = dict()
    contador = -1
    for celda in range(1,filas*columnas+1):
        if celda not in conjunto_restriccion:
            contador +=1
            diccionario_celdas[celda] = politica[contador]
    return diccionario_celdas



mapa = crear_mapa()

# ACÁ SE CREAN TODAS LAS POLÍTICAS POSIBLES Y SE ALMACENAN EN UNA LISTA GRACIAS AL MODULO "itertools"
politicas = [item for item in itertools.product("NSEO", repeat=9)]


# ACÁ SE DEFINEN LOS PARÁMETROS
salida = int(input('Estado de Salida: '))
llegada = int(input('Estado de Llegada: '))
restriccion = int(input('Estado No Accesible: '))
pared = int(input('Estado Pared: '))

coord_salida = buscar_punto(salida, mapa)
coord_llegada = buscar_punto(llegada, mapa)
coord_restriccion = buscar_punto(restriccion, mapa)
coord_pared = buscar_punto(pared, mapa)

conjunto_restriccion = (llegada,restriccion,pared)

#########################################################3

mejor_politica = ''
coord_robot = coord_salida
punto_actual = mapa[coord_robot[1]][coord_robot[0]]
mejor_puntaje = -10.0
numero_trayectorias = 20
numero_pasos = 10
total = round(0)
porcentaje = int(0)
print (len(politicas))

for politica in politicas:
    total += 1
    politica_actual = crear_diccionario_mapa(politica)
    probabilidad_acumulada = list()
    lista_puntajes = list()

    for trayectoria in range(numero_trayectorias):
        prob_actual = 1
        coord_robot = coord_salida
        punto_actual = mapa[coord_robot[1]][coord_robot[0]]
        puntaje_trayectoria = 0

        for paso in range(numero_pasos):

            coord_robot, prob = moverse(coord_robot, politica_actual[punto_actual])

            prob_actual *= prob
            punto_actual = mapa[coord_robot[1]][coord_robot[0]]
            if punto_actual not in conjunto_restriccion:
                puntaje_trayectoria -= 0.02
            elif punto_actual == llegada:
                puntaje_trayectoria += 1
                break
            else:
                puntaje_trayectoria -= 1
                break
        probabilidad_acumulada.append(prob_actual)
        lista_puntajes.append(puntaje_trayectoria)

    puntaje_ponderado = 0

    for puntaje in range(numero_trayectorias):
        puntaje_ponderado += (lista_puntajes[puntaje])*(probabilidad_acumulada[puntaje]/sum(probabilidad_acumulada))


    if puntaje_ponderado >= mejor_puntaje:
        mejor_puntaje = puntaje_ponderado
        mejor_politica = politica_actual

    p_actual = int(total/len(politicas)*100)
    if p_actual != porcentaje:
        porcentaje = p_actual
        print (str(porcentaje) + "%")


print (mejor_politica)
print (mejor_puntaje)



