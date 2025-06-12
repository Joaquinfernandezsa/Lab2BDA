import os
import hashlib
from pymongo import MongoClient
from sentence_transformers import SentenceTransformer
import json

# Conexión a MongoDB (ajusta el puerto si usas mongo2 o mongo3)
cliente = MongoClient("mongodb://localhost:27017/?replicaSet=rs0")
db = cliente["Política"]
coleccion = db["Discursos"]

# Modelo de embeddings
modelo = SentenceTransformer('all-MiniLM-L6-v2')

# Ruta al directorio con los .txt
ruta_discursos = "./DiscursosOriginales"

# Procesamiento de cada archivo
for archivo in os.listdir(ruta_discursos):
    if archivo.endswith(".txt"):
        with open(os.path.join(ruta_discursos, archivo), "r", encoding="utf-8") as f:
            texto = f.read()

        # Calcular SHA-256 del texto
        hash_id = hashlib.sha256(texto.encode("utf-8")).hexdigest()

        # Generar embedding
        embedding = modelo.encode(texto).tolist()

        # Crear documento
        documento = {
            "_id": hash_id,
            "texto": texto,
            "embedding": embedding
        }

        # Insertar en MongoDB (ignora duplicados)
        try:
            coleccion.insert_one(documento)
            print(f"Insertado: {archivo}")
        except:
            print(f"Ya existe: {archivo}")
