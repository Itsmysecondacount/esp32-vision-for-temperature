import cv2
import numpy as np
import math

def calcular_angulo_con_lados(a, b, c):
    # Calcula el ángulo opuesto al lado c usando la ley de cosenos
    cos_c = (a**2 + b**2 - c**2) / (2 * a * b)
    angulo = math.acos(cos_c)  # acos devuelve el ángulo en radianes
    angulo_grados = math.degrees(angulo)  # Convertir a grados si es necesario
    return angulo_grados

def calcular_porcentaje(punto_manilla, inicio, final, punta_manilla):
    # Calcular la distancia entre los puntos
    dist_inicio_manilla = calcular_distancia(inicio, punto_manilla)
    dist_final_manilla = calcular_distancia(final, punto_manilla)
    dist_inicio_final = calcular_distancia(inicio, final)
    dist_inicio_punta = calcular_distancia(inicio, punta_manilla)
    dist_punta_manilla = calcular_distancia(punta_manilla, punto_manilla)
    
    # Calcular el ángulo en el punto de manilla
    angulo_total = calcular_angulo_con_lados(dist_inicio_manilla, dist_final_manilla, dist_inicio_final)
    angulo_parcial = calcular_angulo_con_lados(dist_inicio_manilla, dist_punta_manilla, dist_inicio_punta)
    
    # Suponiendo que el ángulo total representa el 100%, calculamos el porcentaje
    porcentaje = (angulo_parcial / angulo_total) * 100
    return porcentaje

def encontrar_contorno_mas_cercano(contornos, punto_manilla):
    contorno_mas_cercano = None
    min_dist_contorno = float('inf')

    # Buscar el contorno con un punto más cercano al punto de la manilla
    for cont in contornos:
        # Encuentra la distancia más cercana de este contorno al punto de la manilla
        min_dist_punto = min([calcular_distancia(p[0], punto_manilla) for p in cont])
        
        # Si esta distancia es la menor de todas, actualizamos el contorno más cercano
        if min_dist_punto < min_dist_contorno:
            min_dist_contorno = min_dist_punto
            contorno_mas_cercano = cont

    return contorno_mas_cercano

def encontrar_punta_manilla(contorno, punto_manilla):
    punta_manilla = None
    max_dist = 0

    # Solo buscamos en el contorno más cercano
    for punto in contorno:
        dist = calcular_distancia(punto[0], punto_manilla)
        if dist > max_dist:
            max_dist = dist
            punta_manilla = punto[0]
    
    return punta_manilla

def calcular_distancia(p1, p2):
    return np.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

def encontrar_dial_y_calcular_porcentaje(imagen, punto_manilla=(83,95), inicio=(42,57), final=(117,49), debug=False):
    # Reescalar la imagen 115 / 200  210/280
    ancho = int(imagen.shape[1] * 0.8)
    alto = int(imagen.shape[0] * 0.8)
    dimensiones = (ancho, alto)
    imagen_reescalada = cv2.resize(imagen, dimensiones, interpolation=cv2.INTER_AREA)
    if debug:
        cv2.imshow('Imagen Reescalada', imagen_reescalada)
        if cv2.waitKey(0) & 0xFF == ord('q'):
            cv2.destroyWindow('Imagen Reescalada')

    # Recortar el área de interés
    # Asegúrate de que las coordenadas estén escaladas también si es necesario
    x1, y1 = int(210), int(180)
    x2, y2 = int(360), int(340)
    imagen_recortada = imagen_reescalada[y1:y2, x1:x2]
    if debug:
        cv2.imshow('Imagen Recortada', imagen_recortada)
        if cv2.waitKey(0) & 0xFF == ord('q'):
            cv2.destroyWindow('Imagen Recortada')

    # Rotar imagen 90 grados
    
    imagen_rotada = cv2.rotate(imagen_recortada, cv2.ROTATE_90_CLOCKWISE)
    if debug:
        cv2.imshow('Rotacion', imagen_rotada)
        if cv2.waitKey(0) & 0xFF == ord('q'):
            cv2.destroyWindow('Rotacion')

    # Convertir la imagen a escala de grises
    gris = cv2.cvtColor(imagen_rotada, cv2.COLOR_BGR2GRAY)
    if debug:
        cv2.imshow('Escala de Grises', gris)
        if cv2.waitKey(0) & 0xFF == ord('q'):
            cv2.destroyWindow('Escala de Grises')

    # # Aplicar un desenfoque para reducir el ruido
    # desenfocado = cv2.GaussianBlur(gris, (9, 9), 0)
    # cv2.imshow('Desenfocado', desenfocado)
    # if cv2.waitKey(0) & 0xFF == ord('q'):
    #     cv2.destroyWindow('Desenfocado')

    # Detectar los bordes
    bordes = cv2.Canny(gris, 50, 150)
    if debug:
        cv2.imshow('Bordes', bordes)
        if cv2.waitKey(0) & 0xFF == ord('q'):
            cv2.destroyWindow('Bordes')

    # Encontrar contornos
    contornos, _ = cv2.findContours(bordes, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    if debug:
        imagen_contornos = imagen_rotada.copy()  # Crear una copia para dibujar los contornos
        cv2.drawContours(imagen_contornos, contornos, -1, (0, 255, 0), 2)
        cv2.imshow('Contornos', imagen_contornos)
        if cv2.waitKey(0) & 0xFF == ord('q'):
            cv2.destroyWindow('Contornos')
    
    contorno_mas_cercano = encontrar_contorno_mas_cercano(contornos, punto_manilla)
    
    if contorno_mas_cercano is None:
        return "error"
    
    if debug:
        cv2.drawContours(imagen_contornos, [contorno_mas_cercano], -1, (255, 255, 255), 3)
        cv2.imshow('Contorno mas cercano', imagen_contornos)
        if cv2.waitKey(0) & 0xFF == ord('q'):
                cv2.destroyWindow('Contorno mas cercano')
            
            
    # Identificar la punta de la manilla
    punta_manilla = encontrar_punta_manilla(contorno_mas_cercano, punto_manilla)
    if punta_manilla is not None:
        # Dibujar la punta de la manilla
        if debug:
            imagen_punta_manilla = imagen_contornos.copy()
            cv2.circle(imagen_punta_manilla, punta_manilla, 5, (255, 0, 255), -1)
            cv2.circle(imagen_punta_manilla, inicio, 5, (255, 0, 255), -1)
            cv2.circle(imagen_punta_manilla, final, 5, (255, 0, 255), -1)
            cv2.circle(imagen_punta_manilla, punto_manilla, 5, (255, 0, 255), -1)
            cv2.imshow('Punta Manilla', imagen_punta_manilla)
            if cv2.waitKey(0) & 0xFF == ord('q'):
                cv2.destroyWindow('Punta Manilla')
    
    porcentaje = calcular_porcentaje(punto_manilla, inicio, final, punta_manilla)

    return porcentaje

