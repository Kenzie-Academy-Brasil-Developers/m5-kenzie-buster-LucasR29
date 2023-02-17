from django.db import models
from users.models import User


class MovieRating(models.TextChoices):
    G = "G"
    PG = "PG"
    PG_13 = "PG-13"
    R = "R"
    NC_17 = "NC-17"


class Movie(models.Model):
    title = models.CharField(max_length=127)
    duration = models.CharField(max_length=10, null=True, default=None)
    rating = models.CharField(
        max_length=20,
        choices=MovieRating.choices,
        default=MovieRating.G,
        null=True,
    )
    synopsis = models.TextField(null=True, default=None)

    user = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        related_name="movies",
    )

    orders = models.ManyToManyField(
        "users.User", through="movies.MovieOrder", related_name="movies_ordered"
    )

    def __repr__(self) -> str:
        return f"<Book [{self.id}] - {self.title}>"


class MovieOrder(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="movie_user_orders"
    )
    movie = models.ForeignKey(
        Movie, on_delete=models.CASCADE, related_name="user_movie_orders"
    )
    buyed_at = models.DateTimeField(auto_now=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)
