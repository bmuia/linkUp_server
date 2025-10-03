from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
import logging
from server.settings import MONGO_DB

logger = logging.getLogger(__name__)

# Create your views here.

"""
ChatHistory class is a blueprint for receiving messages from mongodb

- check to see if user is authenticated
- check to see if its the right user
- fetch all the messages from mongodb for the current authenticated user
- return a 200 response if a success
"""

class ChatHistoryView(APIView):

    def get(self, request):

        try:
            user = request.user

            if not user.is_authenticated:

                return Response({
                    'error': 'user is unathorized to access this page.'
                }, status=403)

            
            messages = list(MONGO_DB["messages"].find({}, {"_id": 0}))

            if len(messages) > 0:

                return Response(messages, status=200)

            elif len(messages) == 0:
                return Response({'message': 'This group has not posted any messages'}, status=200)
            
            else:
                return Response({'error': "This request couldn't be completed at the time"})

        
        except Exception as e:
            logger.error("error: {e}")










