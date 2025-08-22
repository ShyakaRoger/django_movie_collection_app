from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
# create genre choices and rating choices for the Movie model
# create movie model 
GENRE_CHOICES = (
    ('AC', 'Action'),
    ('AD', 'Adventure'),
    ('AN', 'Animation'),
    ('C',  'Comedy'),
    ('CR', 'Crime'),
    ('D',  'Documentary'),
    ('DR', 'Drama'),
    ('FM', 'Family'),
    ('F',  'Fantasy'),
    ('HF', 'Historical Fiction'),
    ('H',  'Horror'),
    ('M',  'Musical'),
    ('MS', 'Mystery'),
    ('N',  'Noir'),
    ('P',  'Psychological'),
    ('R',  'Romance'),
    ('SF', 'Science Fiction'),
    ('T',  'Thriller'),
    ('W',  'Western'),
    ('O',  'Other'),
)

RATING_CHOICES = (
    ('0', '0'),
    ('1', '1'),
    ('2', '2'),
    ('3', '3'),
    ('4', '4'),
    ('5', '5'),
)

class Movie(models.Model):
    title = models.CharField(max_length=100)
    genre = models.CharField(
        max_length=2,    # choices above are up to 2 chars.
        choices=GENRE_CHOICES,
        default='O', # storesthe code; and template shows label
    )
    duration = models.PositiveIntegerField(help_text='minutes')
    release_year = models.PositiveIntegerField()
    rating = models.CharField(
        max_length=1,
        choices=RATING_CHOICES,
        default='0',
    )
    comments = models.TextField(max_length=500, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self) -> str:
        return self.title
    
    def get_absolute_url(self):
        return reverse('movie-detail', kwargs={'movie_id': self.id})
    

# Added Model(new feature)
class Review(models.Model):
    movie = models.ForeignKey(
        Movie, on_delete=models.CASCADE, related_name='reviews'
    )
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='reviews'
    )
    rating = models.PositiveSmallIntegerField()  # 1–5 in the form
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f'{self.movie.title} — {self.author.username} ({self.rating}/5)'
    
class Watchlist(models.Model):

    title = models.CharField(max_length=100, default='My Watchlist')

    movies = models.ManyToManyField(Movie, related_name='watchlists')

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='watchlists'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.username}'s Watchlist"