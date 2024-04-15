import cv2
import time
import requests
import numpy as np
import urllib.request
from medidor import encontrar_dial_y_calcular_porcentaje

def enviar_porcentaje(url, topico, valor):
    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json',
    }
    data = {
        "topico": topico,
        "valor": str(valor),
    }
    response = requests.post(url, json=data, headers=headers)
    return response

def procesar_imagen_desde_url():
    url = 'http://192.168.1.33/800x600.jpg'
    # Intenta abrir la URL y leer la imagen
    respuesta = urllib.request.urlopen(url)
    imagen_array = np.array(bytearray(respuesta.read()), dtype=np.uint8)
    imagen = cv2.imdecode(imagen_array, -1)  # Leer la imagen desde la cadena de bytes
    
    if imagen is not None:
        porcentaje = encontrar_dial_y_calcular_porcentaje(imagen, debug=True)
        print(f'La imagen desde {url} tiene un porcentaje de: {porcentaje}%')
        return porcentaje
    else:
        print(f'No se pudo cargar la imagen desde {url}')
        return "error"

def main():
    url_api = 'http://192.168.1.40:8099/api/v1/post-simple-data'
    topico = "cv2/temperatura"

    while True:
        # Procesar la imagen desde la URL
        porcentaje = procesar_imagen_desde_url()  # Asegúrate de que esta función devuelve el porcentaje
        
        # Enviar el porcentaje a la API
        if porcentaje != "error":
            response = enviar_porcentaje(url_api, topico, porcentaje)
            print(f'Respuesta de la API: {response.status_code}, {response.text}')
        else:
            print("Error al obtener el porcentaje de la imagen")
        
        # Esperar 5 minutos antes de la próxima ejecución
        time.sleep(300)

if __name__ == "__main__":
    main()