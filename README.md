# movie-recommendation-LLM

The data for the project is available in Kaggle: https://www.kaggle.com/datasets/rounakbanik/the-movies-dataset with more than 45.000 movies and their metadata.

The project aims to solve this problem: given databases with metadata fields (can be text/images), build a chatbot that can interact with users based on their inputs, and return results in related databases.

It is a full-stack project with 

- Qdrant vector database

- fastAPI for model service (here my choices are Flan-T5 or MiniChat-3B self-hosted) 

- Django for backend 

- React for frontend

The docker images are available at the branch 'docker-setup', and the project is more or less ready for production. We can easily scale, for example, by using any database to save (user's input, bot's response) pairs with ratings for fine-tuning process if needed.

Note that building (vector) databases alone is not enough to solve this problem. For example, with user's input 'recommend to me movies that make me cry', exact keyword matching can't solve it and we need an LLM to give relevant information (for example, overviews and genres) to perform vector search. Here is how I handle the problem

- Step 0. Build vector databases with Qdrant. We can use sentence transformer to transform the neccessary fields to vectors. It is done relatively fast. The movie dataset has more than 45.000 rows, and without GPUs, it can be done within 10 minutes.

- Step 1. Determine all intentions related to each database (for example: movie recommendation for movie database, helps for FAQ database)

- Step 2. For each intention, choose a key query and use sentence transformer to transform this to vector. In our case, the key query is "movie recommendation"

- Step 3. For each user's input, we use sentence transformer to transform this to vector and compute the similarity of the input with each key query

- Step 4. Use an LLM to give more relevant information about user's input with suitable prompt based on task filter. For example, if user's input is "recommend to me a movie similar to Harry Potter", we cannot perform any search, we need more information, for example, about the themes and genres of the movie

- Step 5. Perform vector search with relevant information from the LLM

- Step 6 (optional). Make a prompt with user's input and LLM's response and feed it to the LLM to generate coherent results

- Step 7. Return the results

# Project structure

Here are important files/folders within the project:

- Take a look on 'docs.txt' if you wish to run the project

- 'prepare-databases' folder contains a notebook movie_metadata. Before running it, you would need build docker image for Qdrant and then run this notebook file to create a vector database (this takes around 10-20 mins)

- 'fine-tune' folder contains several notebooks for the set up and results of the three LLMs: Flan-T5, MiniChat-3B and Mistral-7B. You can also fine-tune those models with dataset from huggingface, which I also prepared with a complete process

- 'data' folder contains the movie dataset and some question-answer pairs for fine-tuning

- 'model_service' folder contains source codes for fastAPI server

- 'backend' folder contains sources codes for backend with django

- 'frontend' folder contains source codes for react with django

- 'images' folder contains the results of the project when we glued everything together

# Results

The results are quite good for MiniChat-3B because it can gives relevant information well enough.There are several ways to enhance: 

- Consider fine-tuning MiniChat with relevant datasets

- Use a better LLM, for example, Mistral-7B or LLama-7B

- If the tasks are complex and require reasoning/explaining, consider to use larger LLMs, for example, LLama2-70B or Mistral-8x-7B

- If the domain of knowledge is not sensitive and/or the tasks are complex with limited resources, we can use OpenAI api for reasoning purposes to further improve the relevant information

- Use higher dimension vectors to save vectors, because with 384 dimensions, sentence transformer may not capture well the similarities in vector search and task classifications 

There are several places you can look at before choosing the model:
 
 - In 'fine-tune' folder, I prepared a dataset and the complete fine-tuning process, but because of limited resources, I can only perform this on a very small portion of the dataset

 - You can also see in 'fine-tune' folder the notebooks and results for three models: Flan-T5, MiniChat-3B and Mistral-7B

 - In the 'images' folder, you will see how everything is glued together with MiniChat-3B model