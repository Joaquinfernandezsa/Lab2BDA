from pymongo import MongoClient
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# Conexión a MongoDB
cliente = MongoClient("mongodb://localhost:27017/?replicaSet=rs0")
db = cliente["Política"]
coleccion = db["Discursos"]

# Modelo de embeddings
modelo = SentenceTransformer('all-MiniLM-L6-v2')

# Ingresar la consulta
consulta = input("🔍 Ingresa tu consulta: ")

# Vectorizar la consulta
embedding_consulta = modelo.encode([consulta])

# Obtener todos los documentos con embeddings
documentos = list(coleccion.find({}, {"_id": 1, "texto": 1, "embedding": 1}))

# Crear una matriz con todos los embeddings
embeddings = np.array([doc["embedding"] for doc in documentos])

# Calcular similitud coseno
similitudes = cosine_similarity(embedding_consulta, embeddings)[0]

# Asociar puntajes a los documentos
resultados = []
for i, doc in enumerate(documentos):
    resultados.append({
        "id": doc["_id"],
        "texto": doc["texto"][:200] + "...",  # solo muestra un extracto
        "similitud": round(similitudes[i], 4)
    })

# Ordenar por mayor similitud
top_resultados = sorted(resultados, key=lambda x: x["similitud"], reverse=True)[:5]

# Mostrar resultados
print("\n📄 Resultados más similares:")
for res in top_resultados:
    print(f"\n🆔 ID: {res['id']}")
    print(f"🔗 Similitud: {res['similitud']}")
    print(f"📝 Fragmento: {res['texto']}")
