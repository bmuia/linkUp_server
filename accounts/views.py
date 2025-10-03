from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.exceptions import ValidationError
from django.db import IntegrityError, DatabaseError
from .serializers import RegistrationSerializer, UserSerializer


class RegistrationView(APIView):
    """
    POST /accounts/v1/register/  →  Create a new user and return JWT tokens.

    What this endpoint does:
      1) Accepts user input (e.g., email, username, password) in request.data
      2) Validates the input using RegistrationSerializer
      3) Creates the user in the database if valid
      4) Generates a JWT refresh token and an access token for that user
      5) Returns tokens with HTTP 201 on success
      6) Returns helpful error messages on validation/DB errors
    """
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
            user = serializer.save()

            refresh = RefreshToken.for_user(user)
            return Response({
                'access': str(refresh.access_token),
                'refresh': str(refresh),
            }, status=status.HTTP_201_CREATED)

        except ValidationError as e:
            return Response(e.detail, status=status.HTTP_400_BAD_REQUEST)

        except IntegrityError:
            return Response({
                'error': 'A user with this email/username already exists.'
            }, status=status.HTTP_400_BAD_REQUEST)

        except DatabaseError:
            return Response({
                'error': 'A database error occurred. Please try again later.'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        except Exception:
            return Response({
                'error': 'An unexpected error occurred.'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

class GetCurrentProfile(APIView):
    """
    GET /accounts/v1/whoami → Get the currently authenticated user
    
    What this endpoint does:
      1) No request body is required
      2) Checks which user is making the request
      3) If the provided token is valid, that user’s info is returned
      4) Returns all user info with HTTP 200 on success
      5) Handles errors properly to show where the issue is
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            user = request.user

            if not user.is_authenticated:
                return Response({
                    'error': 'User is not authenticated'
                }, status=status.HTTP_403_FORBIDDEN)
            
            serializer = UserSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response({
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        
class LogoutView(APIView):
    """
    POST /accounts/v1/logout/ → Invalidate the user’s refresh token

    What this endpoint does:
      1) Expects the refresh token in the request body
      2) Blacklists that refresh token so it cannot be used again
      3) Returns a success message if logout succeeds
      4) Returns an error message if something goes wrong
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        refresh = request.data.get('refresh')

        if not refresh:
            return Response(
                {'error': 'Refresh token is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            token = RefreshToken(refresh)
            token.blacklist()

            return Response(
                {'success': 'Logout successful'},
                status=status.HTTP_200_OK
            )
        
        except Exception:
            return Response(
                {'error': 'Invalid or expired refresh token'},
                status=status.HTTP_400_BAD_REQUEST
            )
        

class UpdateUserProfileView(APIView):

    permission_classes = [IsAuthenticated]

    """
    PUT accounts/v1/user/update/ -> Updates user profile

    what this endpoint does:
    1. Expects the data to be updated i.e email, username etc
    2. UPdates user info afer validating it is okay using the serializer
    3. Returns all user info(updated) and a success message
    4. Returns and error message if something goes wrong
    """


    def put(self, request):
        try:
            user = request.user
            serializer = UserSerializer(user, data=request.data, partial=True)

            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response({'message: User profile updated'}, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
    
