from django.db import models

# create genre choices and rating choices for the Movie model
# create movie model 
GENRE_CHOICES = (
    ('AC', 'Action'),
    ('AD', 'Adventure'),
    ('AN', 'Animation'),
    ('C', 'Comedy'),
    ('CR', 'Crime'),
    ('D', 'Documentary'),
    ('DR', 'Drama'),
    ('FM', 'Family'),
    ('F', 'Fantasy'),
    ('HF', 'Historical Fiction'),
    ('H', 'Horror'),
    ('M', 'Musical'),
    ('MS', 'Mystery'),
    ('N', 'Noir'),
    ('P', 'Psychological'),
    ('R', 'Romance'),
    ('SF', 'Science Fiction'),
    ('T', 'Thriller'),
    ('W', 'Western'),
    ('O', 'Other')
)

RATING_CHOICES = (
    ('0', '0'),
    ('1', '1'),
    ('2', '2'),
    ('3', '3'),
    ('4', '4'),
    ('5', '5')
)

class Movie(models.Model):
    title = models.CharField(max_length=100)
    genre = models.CharField(
        max_length=1,
        choices=GENRE_CHOICES,
        default="Other"
    )
    duration = models.IntegerField()
    release_year = models.IntegerField()
    rating = models.CharField(
        max_length=1,
        choices=RATING_CHOICES,
        default=[0][0]
    )
    comments = models.TextField(max_length=500)

    def __str__(self):
        return self.title
