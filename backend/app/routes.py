# backend/app/routes.py
from flask import Blueprint, request, jsonify, render_template
from sentence_transformers import SentenceTransformer
import pandas as pd
import chromadb
from chromadb.config import Settings
from openai import OpenAI
import os

main_bp = Blueprint('main', __name__)

# Cargar modelo y datos una vez
model = SentenceTransformer('all-MiniLM-L6-v2')
data = pd.read_csv("./Data/corpus_preprocesado.csv")
documents = data['Entrevista'].tolist()
ids = data['ID'].tolist()
metadatas = data[['Candidato', 'Temas', 'Descripción']].to_dict(orient='records')
embeddings = model.encode(documents).tolist()

# ChromaDB
client = chromadb.PersistentClient(path="./chroma_db")
collection = client.get_or_create_collection("prueba_collection")
if len(collection.get()) == 0:
    collection.add(documents=documents, metadatas=metadatas, ids=ids, embeddings=embeddings)

# OpenAI client
cliente = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@main_bp.route('/')
def index():
    return render_template('index.html')

@main_bp.route('/query', methods=['POST'])
def query_system():
    try:
        user_query = request.json.get('query')
        if not user_query:
            return jsonify({"error": "No se proporcionó ninguna consulta."}), 400

        query_embedding = model.encode([user_query]).tolist()
        results = collection.query(query_embeddings=query_embedding, n_results=3)
        context = "\n".join(results['documents'][0]) if results['documents'] else "No se encontraron documentos relevantes."

        response = cliente.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Eres un experto en recuperación de información que proporciona respuestas breves y concisas."},
                {"role": "user", "content": f"Usando el siguiente contexto, responde de manera breve y concisa a la pregunta: '{user_query}'\n\nContexto:\n{context}\n\nRespuesta:"}
            ]
        )
        generated_response = response.choices[0].message.content
        return jsonify({"query": user_query, "response": generated_response, "context": context})

    except Exception as e:
        return jsonify({"error": str(e)}), 500