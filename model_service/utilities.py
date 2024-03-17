
import torch

# Get vector from an input text by Sentence Transformer
def get_vector(text, filter_model):
    text_vector = filter_model.encode(text)
    return torch.tensor(text_vector)

# Generate response based on a suitable prompt
def bot_response(prompt, model, tokenizer):
    inputs = tokenizer(prompt, return_tensors="pt", padding=True, truncation=True).to(model.device)

    # Generate answer
    output_sequences = model.generate(
        **inputs,
        max_length=1000,
        num_return_sequences=1,
        # temperature=0.1,  # Adjust for creativity
        # top_p=0.1,  # Nucleus sampling
        top_k=50,  # Top-k sampling
        no_repeat_ngram_size=2  # Prevent repeating n-grams
    )
    
    # Process the output to remove the input question from the response if it gets included
    answer = tokenizer.decode(output_sequences[0], skip_special_tokens=True).replace(prompt, "").strip()
    return answer

# Perform vector database search
def database_search(input_text, client, filter_model):
    results = []
    hits = client.search(
        collection_name='movies',
        query_vector=filter_model.encode(input_text).tolist(),
        limit = 2
    )
    for idx, hit in enumerate(hits):
        result = {}
        result['original_title'] = hit.payload['original_title']
        result['genres'] = hit.payload['genres']
        result['overview'] = hit.payload['overview']
        results.append(result)
    return results

def answer_with_query(results):
    # Constructing a detailed prompt that structures the results as individual pieces of evidence
    evidence_list = "\n".join([f"Title: {result['original_title']}\nGenres: {result['genres']}\nOverview: {result['overview']}" for result in results])
    return evidence_list