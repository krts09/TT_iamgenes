import os
import requests
from PIL import Image
from PIL.ExifTags import TAGS
import hashlib
import time

# API Key de Pexels
PEXELS_API_KEY = "7aQ2l0qElgQiB4fPvUIz98agkiMFbmfsNbtbXKhE6OOFXaV3A7Y1b0y4"

# Cabecera de autenticación
HEADERS = {
    "Authorization": PEXELS_API_KEY
}

# Diccionario de palabras clave organizado por temas y subtemas
palabras_clave_por_tema = {
    "Fundamentos de IA": {
        "Tipos de Inteligencia Artificial": [
            "Classification of AI types with visual examples",
            "Reactive and autonomous AI types diagrams",
            "Graphical representation of AI examples",
        ],
        "Agentes o Sistemas Inteligentes": [
            "Structure of intelligent agents illustrations",
            "Types of intelligent agents and applications graphics",
            "Real-world examples of intelligent systems",
        ],
        "Comparación de Algoritmos de Búsqueda": [
            "Comparative diagrams of heuristic search algorithms",
            "Visualization of A* and depth-first search algorithms",
            "Optimization in search algorithms graphical examples",
        ],
        "Algoritmos Basados en Instancias": [
            "Explanatory diagrams of the KNN algorithm",
            "Detailed graphics of K-means clustering",
            "Visual examples of distance-based classification",
        ],
    },
    "Matematicas Discretas": {
        "Reglas de Inferencia": [
            "Graphical diagrams of inference rules in logic",
            "Visual examples of propositions and conclusions",
            "Explanatory graphics of direct proofs",
        ],
        "Teoria de Conjuntos": [
            "Set operations graphics with examples",
            "Intersection, union, and difference diagrams",
            "Visual representation of set algebra",
        ],
        "Grafos y Arboles": [
            "Directed and undirected graphs visual representations",
            "Visualization of binary trees and traversals",
            "Graphical examples of shortest paths in graphs",
        ],
        "Releaciones de Orden y Relaciones de Equivalencia": [
            "Diagrams of reflexive and transitive relations",
            "Graphical visualization of equivalence classes",
            "Visual examples of antisymmetric order relations",
        ],
    },
    "Fundamentos de Programación": {
        "Arquitectura de Von Neumann": [
            "Von Neumann architecture schematic examples",
            "Diagrams of the Von Neumann model with explanations",
            "Data flow visualization in computational architecture",
        ],
        "Lenguaje C": [
            "Graphical examples of basic C programming code",
            "Visualization of programming structures in C",
            "Diagrams of functions and syntax in C",
        ],
        "Manejo de Archivos en C": [
            "Graphics for reading and writing file operations in C",
            "Diagrams of binary and sequential file handling",
            "Visualization of processes with files in C programming",
        ],
        "Arquitecturas de Memoria": [
            "Detailed diagrams of dynamic and static memory",
            "Visualization of Harvard and Von Neumann memory models",
            "Illustrations of memory allocation and access in C",
        ],
    },
    "Introducción a la Ciencia de Datos": {
        "Historia de la Computación": [
            "Historical advancements in computing visual representations",
            "Evolution of computer generations with graphic examples",
            "Development of computing technologies visualizations",
        ],
        "Revoluciones Industriales": [
            "Graphs showing the impact of industrial revolutions",
            "Visual representation of the shift to Industry 4.0",
            "Digital transformation with visual examples",
        ],
        "Campos de la Ciencia de Datos": [
            "Diagrams of data science applications in industries",
            "Visualization of data science tools and areas",
            "Graphic examples of applied data science",
        ],
    },
}


def obtener_hash_archivo(contenido):
    """
    Calcula un hash único para identificar el contenido de un archivo.

    :param contenido: Contenido del archivo en bytes.
    :return: Hash único como cadena.
    """
    return hashlib.sha256(contenido).hexdigest()

def descargar_imagenes(consulta, carpeta_destino, cantidad=150, hash_registro=set(), archivo_metadatos=""):
    """
    Descarga imágenes libres de derechos desde Pexels.

    :param consulta: Término de búsqueda (palabra clave).
    :param carpeta_destino: Carpeta donde se guardarán las imágenes.
    :param cantidad: Número de imágenes a descargar.
    :param hash_registro: Conjunto para almacenar hashes de imágenes únicas.
    :param archivo_metadatos: Archivo donde se guardarán los metadatos.
    """
    url = f"https://api.pexels.com/v1/search?query={consulta}&per_page={cantidad}"
    respuesta = requests.get(url, headers=HEADERS)

    if respuesta.status_code == 200:
        datos = respuesta.json()
        fotos = datos.get("photos", [])

        if not os.path.exists(carpeta_destino):
            os.makedirs(carpeta_destino)

        for i, foto in enumerate(fotos):
            imagen_url = foto["src"]["original"]
            autor = foto["photographer"]
            licencia = "Licencia de Pexels"

            # Descargar contenido de la imagen
            img_respuesta = requests.get(imagen_url)
            if img_respuesta.status_code == 200:
                contenido = img_respuesta.content
                hash_imagen = obtener_hash_archivo(contenido)

                if hash_imagen not in hash_registro:
                    hash_registro.add(hash_imagen)
                    archivo_destino = os.path.join(carpeta_destino, f"{consulta}_{i+1}.jpg")

                    print(f"Descargando {archivo_destino} de {autor}...")
                    with open(archivo_destino, "wb") as archivo:
                        archivo.write(contenido)
                    print(f"Guardada: {archivo_destino}")

                    # Guardar metadatos en el archivo de texto
                    if archivo_metadatos:
                        with open(archivo_metadatos, "a", encoding="utf-8") as f:
                            f.write(f"Imagen: {archivo_destino}\n")
                            f.write(f"Palabra clave: {consulta}\n")
                            f.write(f"Autor: {autor}\n")
                            f.write(f"Copyright: {licencia}\n")
                            f.write("\n")
                else:
                    print(f"Imagen duplicada detectada, omitida: {imagen_url}")
    else:
        print(f"Error en la solicitud ({consulta}):", respuesta.status_code)

def descargar_imagenes_por_tema(palabras_clave_tema, carpeta_base="dataset_pexels", cantidad=150):
    """
    Descarga imágenes organizadas por tema y subtema, y extrae sus metadatos.

    :param palabras_clave_tema: Diccionario con temas y palabras clave.
    :param carpeta_base: Carpeta principal donde se guardarán las imágenes.
    :param cantidad: Número de imágenes a descargar por palabra clave.
    """
    archivo_metadatos = os.path.join(carpeta_base, "metadatos_imagenes.txt")
    hash_registro = set()

    # Crear carpeta base si no existe
    os.makedirs(carpeta_base, exist_ok=True)

    for tema, subtemas in palabras_clave_tema.items():
        for subtema, palabras_clave in subtemas.items():
            carpeta_destino = os.path.join(carpeta_base, tema, subtema)
            os.makedirs(carpeta_destino, exist_ok=True)

            for palabra_clave in palabras_clave:
                print(f"Descargando imágenes para: {palabra_clave}")
                try:
                    descargar_imagenes(
                        palabra_clave, carpeta_destino, cantidad=cantidad,
                        hash_registro=hash_registro, archivo_metadatos=archivo_metadatos
                    )
                except Exception as e:
                    print(f"Error descargando imágenes para {palabra_clave}: {e}")
                time.sleep(1)  # Pausa para evitar sobrecarga

if __name__ == "__main__":
    descargar_imagenes_por_tema(palabras_clave_por_tema, cantidad=150)
