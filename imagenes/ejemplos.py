"""
Este script permite descargar imáges desde google o bing.

Descargar imágenes desde GOOGLE:
- Instalación:
No usar: pip install google_images_download
Algunas imágenes no se pueden descargar.
Repositorio Actualizado: 
pip install git+https://github.com/Joeclinton1/google-images-download.git
Limitación: 100 imágenes

Descargar imágenes con BING:
- Instalación:
pip install bing-image-downloader

Limitación: Al parecer no hay limites.
"""
#####################################
# Google
#from google_images_download import google_images_download

#instantiate the class
#response = google_images_download.googleimagesdownload()
#arguments = {"keywords":"avion, bus escolar, motos deportivas",
 #            "limit":10,"print_urls":False}
#paths = response.download(arguments)

#print complete paths to the downloaded images
#print(paths)

#####################################
# Bing
from bing_image_downloader import downloader
downloader.download("monkey", limit=5,  output_dir='dataset', 
                    adult_filter_off=True, force_replace=False, timeout=60)

downloader.download("tiger", limit=5,  output_dir='dataset', 
                   adult_filter_off=True, force_replace=False, timeout=60)

"""

palabras_clave_por_tema = {
    "Fundamentos de IA": {
        "Tipos de Inteligencia Artificial": [
            "Clasificación de tipos de IA con ejemplos visuales",
            "Tipos de inteligencia artificial reactiva y autónoma diagramas",
            "Representación gráfica inteligencia artificial ejemplos",
        ],
        "Agentes o Sistemas Inteligentes": [
            "Estructura de agentes inteligentes ilustraciones",
            "Tipos de agentes inteligentes y aplicaciones gráficas",
            "Sistemas inteligentes ejemplos en la vida real",
        ],
        "Comparación de Algoritmos de Búsqueda": [
            "Diagramas comparativos de algoritmos búsqueda heurística",
            "Visualización de algoritmos A y búsqueda en profundidad",
            "Optimización en algoritmos de búsqueda ejemplos gráficos",
        ],
        "Algoritmos Basados en Instancias": [
            "Diagramas explicativos del algoritmo KNN",
            "Agrupamiento K-medias gráficos detallados",
            "Clasificación basada en distancias con ejemplos visuales",
        ],
    },
    "Matemáticas Discretas": {
        "Reglas de Inferencia": [
            "Diagramas gráficos de reglas de inferencia lógica",
            "Ejemplos visuales de proposiciones y conclusiones",
            "Explicaciones gráficas de demostraciones directas",
        ],
        "Teoría de Conjuntos": [
            "Operaciones entre conjuntos gráficas y ejemplos",
            "Diagramas de intersección, unión y diferencia",
            "Representación visual álgebra de conjuntos",
        ],
        "Grafos y Árboles": [
            "Grafos dirigidos y no dirigidos representaciones gráficas",
            "Visualización de árboles binarios y sus recorridos",
            "Ejemplos gráficos de caminos mínimos en grafos",
        ],
        "Relaciones de Orden y Relaciones de Equivalencia": [
            "Diagramas de relaciones reflexivas y transitivas",
            "Visualización gráfica de clases de equivalencia",
            "Ejemplos visuales de relaciones de orden antisimétricas",
        ],
    },
    "Fundamentos de Programación": {
        "Arquitectura Von Neumann": [
            "Esquema de arquitectura Von Neumann ejemplos",
            "Diagramas del modelo Von Neumann gráficos explicativos",
            "Visualización de datos en arquitectura computacional",
        ],
        "Lenguaje C": [
            "Ejemplos gráficos de código básico en lenguaje C",
            "Visualización de estructuras de programación en C",
            "Diagramas de funciones y sintaxis en C",
        ],
        "Manejo de Archivos en C": [
            "Gráficos para operaciones de lectura y escritura en C",
            "Diagramas de manejo de archivos binarios y secuenciales",
            "Visualización de procesos con archivos en lenguaje C",
        ],
        "Arquitecturas de Memoria": [
            "Diagramas detallados de memoria dinámica y estática",
            "Visualización de modelos de memoria Harvard y Von Neumann",
            "Ilustraciones de asignación y acceso a memoria en C",
        ],
    },
    "Introducción a la Ciencia de Datos": {
        "Historia de la Computación": [
            "Avances históricos en computación representaciones gráficas",
            "Evolución de generaciones de computadoras ejemplos gráficos",
            "Desarrollo de tecnologías computacionales visualizaciones",
        ],
        "Revoluciones Industriales": [
            "Gráficos de impacto de las revoluciones industriales",
            "Representación visual del cambio hacia industria 4.0",
            "Transformación digital con ejemplos visuales",
        ],
        "Campos de la Ciencia de Datos": [
            "Diagramas de aplicaciones de ciencia de datos en industrias",
            "Visualización de herramientas y áreas de ciencia de datos",
            "Ejemplos gráficos de ciencia de datos aplicada",
        ],
    },
}
"""