# app/database/vector_store.py
import chromadb
from chromadb.utils import embedding_functions

from app.config import config

class VectorDB:
    def __init__(self, db_path=config.CHROMA_DB_PATH):
        self.client = chromadb.PersistentClient(path=db_path)
        self.embedding_fn = embedding_functions.SentenceTransformerEmbeddingFunction(
            model_name=config.EMBEDDING_MODEL_NAME
        )
        self.collection = self.client.get_or_create_collection(
            name="ecommerce_catalog", 
            embedding_function=self.embedding_fn
        )
        self._seed_initial_catalog()

    def _seed_initial_catalog(self):
        if self.collection.count() == 0:
            # Seed containing cross-lingual reference indicators
            products = [
                {"id": "p1", "name": "Eco-Friendly Wireless Mouse", "price": 25.00, "desc": "Sleek 2.4GHz wireless mouse constructed from 100% ocean recycled plastics. इको-फ्रेंडली वायरलेस माउस कंप्यूटर"},
                {"id": "p2", "name": "Minimalist Leather Journal", "price": 18.50, "desc": "Genuine top-grain leather blank sketchbook containing 200 pages. चमड़े की डायरी नोटबुक जर्नल"},
                {"id": "p3", "name": "Stainless Steel Water Bottle", "price": 30.00, "desc": "Double-walled vacuum insulated thermal flask water bottle. पानी की बोतल स्टील थर्मल"},
                {"id": "p4", "name": "Ergonomic Wool Desk Mat", "price": 22.00, "desc": "Soft felt anti-slip protective covering optimized for office layouts. टेबल मैट डेस्क पैड ऊनी"},
            ]
            self.collection.add(
                documents=[f"{p['name']}: {p['desc']}" for p in products],
                metadatas=[{"name": p["name"], "price": p["price"], "id": p["id"]} for p in products],
                ids=[p["id"] for p in products]
            )

    def search_products(self, query: str, limit: int = 2):
        results = self.collection.query(query_texts=[query], n_results=limit)
        matched_items = []
        if results and 'metadatas' in results and len(results['metadatas']) > 0 and results['metadatas'][0]:
            for metadata in results['metadatas'][0]:
                matched_items.append({
                    "id": metadata["id"],
                    "name": metadata["name"],
                    "price": metadata["price"]
                })
        return matched_items
