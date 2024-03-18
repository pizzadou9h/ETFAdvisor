# file: st_app/st_recommender.py
import json
import os
import numpy as np
from vertexai.language_models import TextEmbeddingModel


class ETFRecommender:
    def __init__(self):
        # Set the path to your service account key file
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "google_key.json"
        self.data = None

    def load_data(self, file_path):
        # Load the JSON data with embeddings from file
        with open(file_path, "r") as file:
            self.data = json.load(file)

    def get_embedding(self, text):
        model = TextEmbeddingModel.from_pretrained("textembedding-gecko@003")
        embeddings = model.get_embeddings([text])
        return embeddings[0].values

    def cosine_similarity(self, a, b):
        return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

    def recommend_etfs(self, user_input):
        # Load ETF data
        self.load_data("etf_data_short.json")

        # Generate embedding for user input
        user_input_embedding = self.get_embedding(user_input)

        # Calculate cosine similarity between user input and each ETF
        for etf in self.data:
            etf["similarity"] = self.cosine_similarity(
                user_input_embedding, etf["embedding"]
            )

        # Sort ETFs based on similarity score
        self.data.sort(key=lambda x: x["similarity"], reverse=True)

        # Return top 5 ETF recommendations
        return self.data[:5]
