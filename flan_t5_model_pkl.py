"""
create_model_pkl.py
-------------------
Loads a Hugging Face Flan-T5 model and saves it as a .pkl file.
Run this file ONCE.
"""

import pickle
from transformers import pipeline

def create_model_pickle():
    print("Loading Flan-T5 model...")
    model_pipeline = pipeline(
        task="text2text-generation",
        model="google/flan-t5-base",
        max_length=512
    )

    print("Saving model to flan_t5_model.pkl...")
    with open("flan_t5_model.pkl", "wb") as f:
        pickle.dump(model_pipeline, f)

    print("Model saved successfully.")

if __name__ == "__main__":
    create_model_pickle()
