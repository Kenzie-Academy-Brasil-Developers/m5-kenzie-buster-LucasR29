from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.views import APIView, Request, Response, status
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .serializers import MovieSerializer, MovieOrderSerializer
from rest_framework.pagination import PageNumberPagination
from users.permission import IsAdminOrReadOnly
from django.shortcuts import get_object_or_404
from .models import Movie, MovieOrder
from users.models import User


class MovieView(APIView, PageNumberPagination):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminOrReadOnly]

    def post(self, request: Request) -> Response:
        serializer = MovieSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        serializer.save(user=request.user)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get(self, request: Request) -> Response:
        movies_obj = Movie.objects.all()

        result_page = self.paginate_queryset(movies_obj, request)

        movies = MovieSerializer(result_page, many=True)

        return self.get_paginated_response(movies.data)


class MovieDetailView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminOrReadOnly]

    def delete(self, request: Request, movie_id: int) -> Response:
        movie = get_object_or_404(Movie, id=movie_id)

        movie.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)

    def get(self, request: Request, movie_id: int) -> Response:
        movie = get_object_or_404(Movie, id=movie_id)

        return Response(MovieSerializer(movie).data, status=status.HTTP_200_OK)


class MovieOrderView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]

    def post(self, request: Request, movie_id: int) -> Response:
        movie = get_object_or_404(Movie, id=movie_id)

        movie_order = MovieOrderSerializer(data=request.data)

        movie_order.is_valid(raise_exception=True)

        movie_order.save(user=request.user, movie=movie)

        return Response(movie_order.data, status=status.HTTP_201_CREATED)
