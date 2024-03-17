import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

# Create views here.
class SendMessageView(APIView):

    def post(self, request):
        try:
            data = request.data  # You can use request.data instead of json.loads(request.body)
            text = data.get("text")

            # The FastAPI service is running on http://localhost:8001/send_text without using docker
            # and expects a JSON with a key 'text'
            # response = requests.post('http://localhost:8001/send_text', json={'text': text})

            # Using docker
            response = requests.post('http://host.docker.internal:8001/send_text', json={'text': text})

            # Check if the request to the FastAPI service was successful
            if response.status_code == 200:
                # Assuming FastAPI response is a JSON containing a 'results' field
                return Response(response.json())
            else:
                # FastAPI service did not return a 200 OK
                return Response({'error': 'FastAPI service error'}, status=response.status_code)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
