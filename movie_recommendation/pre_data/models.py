from django.db import models

# Create your models here.

class MovieData(models.Model):
    movie_id = models.IntegerField()
    title = models.CharField(max_length = 100, null=True)
    star = models.FloatField(null=True)
    movie_rating = models.CharField(max_length = 100, null=True)
    genre = models.CharField(max_length = 100, null=True)
    director = models.CharField(max_length = 100, null=True)
    actors = models.CharField(max_length = 400, null=True)
    summary =  models.TextField(null=True)
