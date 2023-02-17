from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.views import APIView, Request, Response, status
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.pagination import PageNumberPagination
from .permission import IsAdminOrReadOnly, IsOwnerOrAdmin
from django.shortcuts import get_object_or_404
from .serializers import UserSerializer
from .models import User


class CustomTokenObtainPairSerializer(
    TokenObtainPairView,
):
    @classmethod
    def get_token(cls, user: User):
        token = super().get_token(user)

        token["email"] = user.email
        token["is_superuser"] = user.is_superuser
        token["user_id"] = user.id

        return token


class UserView(APIView):
    def post(self, request: Request) -> Response:
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status.HTTP_201_CREATED)


class UserDetailView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsOwnerOrAdmin]

    def get(self, request: Request, user_id: int) -> Response:
        user = get_object_or_404(User, id=user_id)

        self.check_object_permissions(request, user)

        serializer = UserSerializer(user)

        return Response(serializer.data, status.HTTP_200_OK)

    def patch(self, request: Request, user_id: int) -> Response:
        user = get_object_or_404(User, id=user_id)

        self.check_object_permissions(request, user)

        serializer = UserSerializer(user, request.data, partial=True)

        serializer.is_valid()

        serializer.save()

        return Response(serializer.data, status.HTTP_200_OK)
