from fastapi import FastAPI
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer, BitsAndBytesConfig
from sentence_transformers import SentenceTransformer
import sentencepiece
from qdrant_client import QdrantClient
from utilities import get_vector, bot_response, database_search, answer_with_query
from torch.nn.functional import cosine_similarity
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Load the model with bits and bytes config
MODEL_NAME = 'google/flan-t5-small'

model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_NAME)

# Define tokenizer
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME, use_fast=False)
tokenizer.pad_token = tokenizer.eos_token

filter_model = SentenceTransformer('all-MiniLM-L6-v2')

# Connect to the Qdrant database
client = QdrantClient(host='host.docker.internal', port=6333)

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
        return {"Hello": "World"}
        