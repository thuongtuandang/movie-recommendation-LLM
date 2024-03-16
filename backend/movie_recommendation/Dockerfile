FROM python:3.10.11
ENV PYTHONUNBUFFERED=1
WORKDIR /backend

# Install pipenv and compilation dependencies
RUN pip install --no-cache-dir pipenv

# Install project dependencies
COPY Pipfile Pipfile.lock ./
RUN pipenv install --deploy --system

# Copy project files
COPY . /backend

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]