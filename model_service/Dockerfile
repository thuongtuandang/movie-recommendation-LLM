# model_service/Dockerfile
FROM python:3.10.11

# Install pipenv
RUN pip install --no-cache-dir pipenv
# RUN pip install pipenv

COPY . /model_service
WORKDIR /model_service

# Install dependencies from Pipfile.lock
RUN pipenv install --deploy --ignore-pipfile

RUN pip install fastapi uvicorn

# Run the FastAPI app using uvicorn
CMD ["pipenv", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8001"]
