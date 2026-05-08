from drf_spectacular.utils import extend_schema
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from .serializers import CreateUserSerializer, DetailAuthorizedUserSerializer


class RegisterAPIView(APIView):
    """Provides endpoint for user registration."""
    @extend_schema(
        summary='Create user',
        request=CreateUserSerializer,
        responses=DetailAuthorizedUserSerializer
    )
    def post(self, request, *args, **kwargs):
        serializer = CreateUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(data=DetailAuthorizedUserSerializer(user).data, status=status.HTTP_201_CREATED)


class DetailAuthorizedUserAPIView(APIView):
    """Returns details of the currently authenticated user."""
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary='Show current user details',
        responses=DetailAuthorizedUserSerializer
    )
    def get(self, request, *args, **kwargs):
        serializer = DetailAuthorizedUserSerializer(request.user)
        return Response(data=serializer.data, status=status.HTTP_200_OK)