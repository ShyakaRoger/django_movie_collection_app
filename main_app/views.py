from django.shortcuts import render, get_object_or_404
from .models import Movie

# Define the home view function
def home(request):
    return render(request, 'home.html')

# Define the about view function
def about(request):
    return render(request, 'about.html')



# create a Movie class and a list of movie instances to imulate a database of movies
# class Movie:
#     def __init__(self, title, genre, duration, release_year, rating, comments):
#         self.title = title
#         self.genre = genre
#         self.duration = duration
#         self.release_year = release_year
#         self.rating = rating
#         self.comments = comments

# # create a list of Movie instances
# movies = [
#     Movie('Finding Nemo', 'Family', 100, 2003, '5', 'these are comments'),
#     Movie('The Goonies', 'Adventure', 114, 1985, '5', 'these are more comments')
# ]

def movie_index(request):
    # render the movies/index.html template with the movies data
    movies = Movie.objects.all().order_by('title')
    return render(request, 'movies/index.html', {'movies': movies})


def movie_detail(request, pk):
    movie = get_object_or_404(Movie, pk=pk)
    return render(request, 'movies/detail.html', {'movie': movie})