from bing_image_downloader import downloader
from PIL import Image
from PIL.ExifTags import TAGS
import os
import time

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
            "Visualization of A and depth-first search algorithms",
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


def extraer_metadatos(imagen_path, palabra_clave, archivo_txt):
    try:
        with Image.open(imagen_path) as img:
            ancho, alto = img.size
            espacio_color = img.mode

            exif_data = img._getexif()
            autor = "Desconocido"
            copyright = "Desconocido"

            if exif_data:
                for tag_id, value in exif_data.items():
                    tag = TAGS.get(tag_id, tag_id)
                    if tag == "Artist":
                        autor = value
                    if tag == "Copyright":
                        copyright = value

            with open(archivo_txt, "a", encoding="utf-8") as f:
                f.write(f"Imagen: {imagen_path}\n")
                f.write(f"Palabra clave: {palabra_clave}\n")
                f.write(f"Resolución: {ancho}x{alto}\n")
                f.write(f"Espacio de color: {espacio_color}\n")
                f.write(f"Autor: {autor}\n")
                f.write(f"Copyright: {copyright}\n")
                f.write("\n")
    except Exception as e:
        print(f"No se pudieron extraer metadatos de {imagen_path}: {e}")


def descargar_imagenes_por_tema(palabras_clave_tema, carpeta_base="dataseteng", cantidad=60):
    archivo_metadatos = os.path.join(carpeta_base, "metadatos_imagenes.txt")
    os.makedirs(carpeta_base, exist_ok=True)

    for tema, subtemas in palabras_clave_tema.items():
        for subtema, palabras_clave in subtemas.items():
            carpeta_destino = os.path.join(carpeta_base, tema, subtema)
            os.makedirs(carpeta_destino, exist_ok=True)

            for palabra_clave in palabras_clave:
                print(f"Descargando imágenes para: {palabra_clave}")
                try:
                    downloader.download(
                        palabra_clave,
                        limit=cantidad,
                        output_dir=carpeta_destino,
                        adult_filter_off=True,
                        force_replace=False,
                        timeout=60,
                    )

                    carpeta_imagenes = os.path.join(carpeta_destino, palabra_clave)
                    if os.path.exists(carpeta_imagenes):
                        for i, imagen in enumerate(os.listdir(carpeta_imagenes)):
                            imagen_path = os.path.join(carpeta_imagenes, imagen)
                            nuevo_nombre = f"{subtema.replace(' ', '_')}_{i + 1}.jpg"
                            nuevo_path = os.path.join(carpeta_destino, nuevo_nombre)

                            os.rename(imagen_path, nuevo_path)
                            extraer_metadatos(nuevo_path, palabra_clave, archivo_metadatos)

                        os.rmdir(carpeta_imagenes)

                except Exception as e:
                    print(f"Error descargando imágenes para {palabra_clave}: {e}")
                time.sleep(1)


if __name__ == "__main__":
    descargar_imagenes_por_tema(palabras_clave_por_tema, cantidad=60)
