from django.shortcuts import render, get_object_or_404
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Movie

# Define the home view function
def home(request):
    return render(request, 'home.html')

# Define the about view function
def about(request):
    return render(request, 'about.html')

def movie_index(request):
    # render the movies/index.html template with the movies data
    movies = Movie.objects.all().order_by('title')
    return render(request, 'movies/index.html', {'movies': movies})

def movie_detail(request, movie_id):

    #I changed pk back to movie_id. I was getting an error that it wasnt matching up to the url when navigating to a movie detail
    movie = get_object_or_404(Movie, id=movie_id)
    return render(request, 'movies/detail.html', {'movie': movie})

class MovieCreate(CreateView):
    model = Movie
    fields = '__all__'

class MovieUpdate(UpdateView):
    model = Movie
    fields = '__all__'

class MovieDelete(DeleteView):
    model = Movie
    success_url = '/movies/'
   