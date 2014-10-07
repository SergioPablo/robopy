# -*- coding: utf-8 -*-
# SE DEBE EJECUTAR EN PYTHON 3

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

# ESTA FUNCION RECIBE LA COORDENADA ACTUAL Y LA DIRECCION EN FORMA DE STRING Y RETORNA LA NUEVA COORDENADA Y LA PROBABILIDAD QUE TUVO EL MOVIMIENTO
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


# SE CREA UN DICCIONARIO A PARTIR DE UNA POLÍTICA QUE TIENE LA FORMA cuadro_x: 'SENTIDO', cuadro_y: 'SENTIDO'.........
def crear_diccionario_mapa(politica):
    diccionario_celdas = dict()
    contador = -1
    for celda in range(1,filas*columnas+1):
        if celda not in conjunto_restriccion:
            contador +=1
            diccionario_celdas[celda] = politica[contador]
    return diccionario_celdas


# ACÁ SE DEFINE EL NUMERO TOTAL DE FILAS Y COLUMNAS
filas = 3
columnas = 4

# ACÁ SE CREA EL MAPA
mapa = crear_mapa()

# ACÁ SE CREAN TODAS LAS POLÍTICAS POSIBLES Y SE ALMACENAN EN UNA LISTA GRACIAS AL MODULO "itertools"
politicas = [item for item in itertools.product("NSEO", repeat=filas*columnas-3)]

valores_utilizados = list()

# ACÁ SE DEFINEN LOS PARÁMETROS Y SE VERIFICA SI SON VÁLIDOS

salida = 0
while salida not in valores_utilizados:
    valor = int(input('Estado de Salida: '))
    if valor in valores_utilizados or valor < 1 or valor > filas*columnas:
        print("Valor ya utilizado o valor inválido, ingrese otro")
    else:
        salida = valor
        valores_utilizados.append(salida)

llegada = 0
while llegada not in valores_utilizados:
    valor = int(input('Estado de Salida: '))
    if valor in valores_utilizados or valor < 1 or valor > filas*columnas:
        print("Valor ya utilizado o valor inválido, ingrese otro")
    else:
        llegada = valor
        valores_utilizados.append(llegada)

restriccion = 0
while restriccion not in valores_utilizados:
    valor = int(input('Estado de Llegada: '))
    if valor in valores_utilizados or valor < 1 or valor > filas*columnas:
        print("Valor ya utilizado o valor inválido, ingrese otro")
    else:
        restriccion = valor
        valores_utilizados.append(restriccion)

pared = 0
while pared not in valores_utilizados:
    valor = int(input('Estado de Pared: '))
    if valor in valores_utilizados or valor < 1 or valor > filas*columnas:
        print("Valor ya utilizado o valor inválido, ingrese otro")
    else:
        pared = valor
        valores_utilizados.append(pared)

# SE DEFINEN LAS COORDENADAS
coord_salida = buscar_punto(salida, mapa)
coord_llegada = buscar_punto(llegada, mapa)
coord_restriccion = buscar_punto(restriccion, mapa)
coord_pared = buscar_punto(pared, mapa)

# SE DEFINE EL CONJUNTO RESTRICCIÓN
conjunto_restriccion = (llegada,restriccion,pared)

###############################################################################

mejor_politica = ''
coord_robot = coord_salida
punto_actual = mapa[coord_robot[1]][coord_robot[0]]
mejor_puntaje = -10.0
numero_trayectorias = 20
numero_pasos = 10

#PARÁMETROS PARA LLEVAR EL PORCENTAJE
total = round(0)
porcentaje = int(0)


print ("Total de politicas: " + str(len(politicas)))

#COMIENZA LA ITERACIÓN

for politica in politicas:
    # LA VARIABLE total ES PARA LLEVAR EL PORCENTAJE
    total += 1

    # SE CREA UN DICCIONARIO DE LA POLÍTICA DONDE CADA CUADRO TIENE SU RESPECTIVO SENTIDO
    politica_actual = crear_diccionario_mapa(politica)

    # SE LLEVA LA LISTA DE PROBABILIDAD POR CADA TRAYECTORIA
    probabilidad_acumulada = list()

    # SE LLEVA LA LISTA DE PUNTAJE POR CADA TRAYECTORIA
    lista_puntajes = list()

    # SE EVLUAN UN NUMERO DEFINIDO DE TRAYECTORIAS
    for trayectoria in range(numero_trayectorias):

        #LA PROBABILIDAD ACTUAL DE LA TRAYECTORIA
        prob_actual = 1

        coord_robot = coord_salida

        punto_actual = mapa[coord_robot[1]][coord_robot[0]]

        puntaje_trayectoria = 0

        for paso in range(numero_pasos):
            # AL EJECUTAR LA FUNCIÓN moverse SE RETORNAN 2 VARIABLES, LA PRIMERA ES LA NUEVA POSICIÓN DEL ROBOT Y LA SEGUNDA
            # LA PROBABILIDAD DEL MOVIMIENTO, DONDE ES 0.8 SI FUE A LA DIRECCIÓN INDICADA O ES 0.1 SI SIGUIÓ OTRA
            coord_robot, prob = moverse(coord_robot, politica_actual[punto_actual])

            # LA PROBABILIDAD SE MULTIPLICA CON LA PROBABILIDAD QUE LLEVA
            prob_actual *= prob

            # EL PUNTO ACTUAL VA A SER LA COORDENADA DEL ROBOT
            punto_actual = mapa[coord_robot[1]][coord_robot[0]]

            # CUALQUIER PUNTO VALE 0.02 Y SE SUMARA EL PUNTAJE DE ESTA TRAYECTORIA
            if punto_actual not in conjunto_restriccion:
                puntaje_trayectoria -= 0.02

            # SI LLEGA A LA SALIDA SE SUMA 1 Y NO SE SIGUE MOVIENDO
            elif punto_actual == llegada:
                puntaje_trayectoria += 1
                break
            # SI LLEGA AL OTRO PUNTO, SE RESTA 1 Y NO SE SIGUE MOVIENDO
            else:
                puntaje_trayectoria -= 1
                break

        # ACÁ SE AGREGA LA PROBABILIDAD Y EL PUNTAJE DE ESTA TRAYECTORIA EN PARTICULAR A SUS RESPECTIVAS LISTAS
        probabilidad_acumulada.append(prob_actual)
        lista_puntajes.append(puntaje_trayectoria)

    # ACÁ SE DETERMINARÁ EL PUNTAJE PONDERADO DE LA POLITICA
    puntaje_ponderado = 0

    # ACÁ SE HACE UNA ITERACIÓN Y SE USA LA FÓRMULA DE PONDERACIÓN EN EL PPT
    # PUNTAJE PONDERADO DE TRAYECTORIA = p1*RT1+p2*RT2+p3*RT3...........
    # px=qx/(q1+q2+q3.......)
    # RTx = 0.02-0.02-0.02-0.02-0.02-0.02+1 (o cualquier puntaje que pudo haber dado la tratectoria)

    for puntaje in range(numero_trayectorias):
        puntaje_ponderado += (lista_puntajes[puntaje])*(probabilidad_acumulada[puntaje]/sum(probabilidad_acumulada))


    if puntaje_ponderado >= mejor_puntaje:
        mejor_puntaje = puntaje_ponderado
        mejor_politica = politica_actual

    # ACÁ SE LLEVA EL PORCENTAJE
    p_actual = int(total/len(politicas)*100)
    if p_actual != porcentaje:
        porcentaje = p_actual
        print (str(porcentaje) + "%")


print ("La mejor politica fue: " + str(mejor_politica) + " con un puntaje de: " + str(mejor_puntaje))



