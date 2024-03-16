from fastapi import FastAPI
import bitsandbytes as bnb
import torch
import torch.nn as nn
import transformers
from huggingface_hub import notebook_login
from peft import LoraConfig, PeftConfig, PeftModel, get_peft_model, prepare_model_for_kbit_training
from transformers import AutoConfig, AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig
import sentencepiece
from sentence_transformers import SentenceTransformer
from qdrant_client import models, QdrantClient
from qdrant_client.http.models import CollectionDescription, VectorParams
from utilities import get_vector, bot_response, database_search, answer_with_query
from torch.nn.functional import cosine_similarity
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Load the model with bits and bytes config
model = "GeneZC/MiniChat-3B"

MODEL_NAME = model

bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_use_double_quant=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_compute_dtype=torch.bfloat16
)

model = AutoModelForCausalLM.from_pretrained(
    MODEL_NAME,
    device_map="auto",
    # device_map="cpu",
    trust_remote_code=True,
    quantization_config=bnb_config
)

# PEFT wrapper the model for training / fine-tuning
model = prepare_model_for_kbit_training(model)

# Define tokenizer
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME, use_fast=False)
tokenizer.pad_token = tokenizer.eos_token

filter_model = SentenceTransformer('all-MiniLM-L6-v2')

# Connect to the Qdrant database
client = QdrantClient(host='localhost', port=6333)

# Vectorization of "movie recommendation"
valid_query = "movie recommendation"
valid_vector = get_vector(valid_query, filter_model)
valid_vector.shape

intentions = [
    "Can you recommend to me a movie similar to Harry Potter?"
]

app = FastAPI()

@app.get("/")
async def read_root():
    logger.info("Handling request to the root endpoint")

    for intention in intentions:
        intention_vector = get_vector(intention, filter_model)
        similarity = cosine_similarity(intention_vector.unsqueeze(0), valid_vector.unsqueeze(0))
        logger.debug(f"Question: {intention}")
        if similarity < 0.5:
            prompt = f"Answer the following question:\n{intention}"
            logger.debug(bot_response(prompt, model, tokenizer))
        if similarity >= 0.5:
            prompt = f"For the information mentioned, describe its genres and any notable themes:\n{intention}"
            bot_answer = bot_response(prompt, model, tokenizer)
            logger.debug(f"First answer:\n{bot_answer}")
            results = database_search(bot_answer, client, filter_model)
            evidence_list = answer_with_query(results)
            logger.debug(f"Database search results:\n{evidence_list}")
        logger.info("============================================================")


# @app.get("/")

# async def read_root():
#     return {"Hello": "World"}
    # for intention in intentions:
    #     intention_vector = get_vector(intention, filter_model)
    #     similarity = cosine_similarity(intention_vector.unsqueeze(0), valid_vector.unsqueeze(0))
    #     print(f"Question: {intention}")
    #     if similarity < 0.5:
    #         prompt = f"Answer the following question:\n{intention}"
    #         print(bot_response(prompt, model, tokenizer))
    #     if similarity >= 0.5:
    #         prompt = f"For the information mentioned, describe its genres and any notable themes:\n{intention}"
    #         bot_answer = bot_response(prompt, model, tokenizer)
    #         print(f"First answer:\n{bot_answer}")
    #         results = database_search(bot_answer, client, filter_model)
    #         evidence_list = answer_with_query(results)
    #         print(f"Databse search results:\n{evidence_list}")
    #     print("============================================================")
        