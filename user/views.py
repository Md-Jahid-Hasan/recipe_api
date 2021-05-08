from django.contrib.auth import login
from django.http import JsonResponse
from rest_framework import generics, authentication, permissions
from rest_framework.response import Response
import json
from user.serializers import UserSerializer, AuthTokenSerializer
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from rest_framework.views import APIView


class CreateUserView(generics.CreateAPIView):
    serializer_class = UserSerializer


class CreateTokenView(ObtainAuthToken):
    serializer_class = AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


class TestView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = AuthTokenSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        s = UserSerializer(user)

        return Response({"message": "Login Successful", "test": s.data})

    def get(self, request):
        serializer = AuthTokenSerializer()
        return Response(serializer.data)


class ManageUserView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    # authentication_classes = (authentication.BasicAuthentication,) #it require authentication thou you are login
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        return self.request.user
