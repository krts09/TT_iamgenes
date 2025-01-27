import os
import requests
import json
from datetime import datetime

def is_valid_url(url):
    try:
        response = requests.head(url, timeout=5)
        return response.status_code == 200
    except requests.exceptions.RequestException:
        return False

def search_and_download_images(query, num_images=100, save_folder="datasetazureingles"):
    # Configuración de la API de Bing
    api_key = "8f2c531dae5c4f07b9d0573b7f6853db"  # Reemplaza con tu clave de API
    search_url = "https://api.bing.microsoft.com/v7.0/images/search"

    headers = {"Ocp-Apim-Subscription-Key": api_key}
    params = {"q": query, "count": num_images, "imageType": "photo"}

    try:
        response = requests.get(search_url, headers=headers, params=params)
        response.raise_for_status()
        results = response.json()

        if not os.path.exists(save_folder):
            os.makedirs(save_folder)

        metadata = []

        for i, img in enumerate(results.get("value", [])):
            image_url = img["contentUrl"]
            image_format = img.get("encodingFormat", "jpg")  # Valor por defecto 'jpg' si no se encuentra el campo
            file_name = f"{query.replace(' ', '_')}_{i}.{image_format}"
            file_path = os.path.join(save_folder, file_name)

            # Verificar si la URL es válida
            if not is_valid_url(image_url):
                print(f"URL no válida: {image_url}")
                continue  # Pasar a la siguiente imagen

            # Descargar y guardar la imagen
            img_data = requests.get(image_url).content
            with open(file_path, "wb") as f:
                f.write(img_data)

            # Guardar metadatos
            metadata.append({
                "file_name": file_name,
                "image_url": image_url,
                "source": img.get("hostPageUrl"),
                "format": image_format,
                "downloaded_at": datetime.now().isoformat()
            })

        # Guardar metadatos en un archivo JSON
        metadata_file = os.path.join(save_folder, f"{query.replace(' ', '_')}_metadata.json")
        with open(metadata_file, "w") as f:
            json.dump(metadata, f, indent=4)

        print(f"Descarga completada. Imágenes y metadatos guardados en '{save_folder}'")

    except Exception as e:
        print(f"Error durante la búsqueda o descarga: {e}")

def descargar_imagenes_por_tema(palabras_clave_por_tema, save_folder="datasetazure"):
    for tema, subtemas in palabras_clave_por_tema.items():
        for subtema, consultas in subtemas.items():
            subfolder_path = os.path.join(save_folder, tema, subtema)
            os.makedirs(subfolder_path, exist_ok=True)

            for consulta in consultas:
                print(f"Descargando imágenes para la consulta: {consulta}")
                search_and_download_images(consulta, num_images=100, save_folder=subfolder_path)

if __name__ == "__main__":
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


    descargar_imagenes_por_tema(palabras_clave_por_tema)
