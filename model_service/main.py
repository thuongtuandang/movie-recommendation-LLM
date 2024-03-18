from fastapi import FastAPI
from transformers import AutoModelForSeq2SeqLM, AutoModelForCausalLM, AutoTokenizer
from sentence_transformers import SentenceTransformer
import sentencepiece
from qdrant_client import QdrantClient
from utilities import get_vector, bot_response, database_search, answer_with_query
from torch.nn.functional import cosine_similarity
import logging
from pydantic import BaseModel
import torch

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# # Load the Flan-t5-small if your resources are limited
# MODEL_NAME = 'google/flan-t5-small'

# model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_NAME)

# # Define tokenizer
# tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME, use_fast=False)
# tokenizer.pad_token = tokenizer.eos_token

# Load the MiniChat model
MODEL_NAME = "GeneZC/MiniChat-3B"

model = AutoModelForCausalLM.from_pretrained(
    MODEL_NAME,
    device_map="auto",
    # device_map="cpu",
    trust_remote_code=True,
)
# device = "mps" if torch.backends.mps.is_available() else "cpu"
# model = model.to(device)

# device = "cuda" if torch.cuda.is_available() else "cpu"
# model = model.to(device)

# Define tokenizer
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME, use_fast=False)
tokenizer.pad_token = tokenizer.eos_token

filter_model = SentenceTransformer('all-MiniLM-L6-v2')


# Connect to the Qdrant database
# Use this for docker
# client = QdrantClient(host='host.docker.internal', port=6333)

# Use this to run locally
client = QdrantClient(host='localhost', port=6333)

# Vectorization of "movie recommendation"
valid_query = "movie recommendation"
valid_vector = get_vector(valid_query, filter_model)
valid_vector.shape

app = FastAPI()

# Define TextItem class with Pydantic
# This expects a JSON object with a text field

class TextItem(BaseModel):
    text: str

@app.post("/send_text")
async def send_text(item: TextItem):
    # Vectorize and compute the similarity to movie recommendation
    intention = item.text
    intention_vector = get_vector(intention, filter_model)
    similarity = cosine_similarity(intention_vector.unsqueeze(0), valid_vector.unsqueeze(0))

    if similarity < 0.5:
        prompt = f"Answer the following question:\n{intention}"
        response = bot_response(prompt, model, tokenizer)
        response = response.replace("<pad>", "").strip()
        return {"category": "0", "response": response}
    if similarity >= 0.5:
        prompt = f"For the information mentioned, describe its genres and any notable themes:\n{intention}"
        bot_answer = bot_response(prompt, model, tokenizer)
        bot_answer = bot_answer.replace("<pad>", "").strip()
        results = database_search(bot_answer, client, filter_model)
        evidence_list = answer_with_query(results)
        return {"category": "1", "response": bot_answer, "results": evidence_list}
        