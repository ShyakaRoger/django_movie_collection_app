from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.views import LoginView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from .models import Movie, Review, Watchlist
from .forms import ReviewForm


# Define the home view function
class Home(LoginView):
    template_name = 'home.html'

def signup(request):
    error_message = ''
    if request.method == 'POST':
        # create a user form object 
        form = UserCreationForm(request.POST)
        if form.is_valid():
            # add user to the database
            user = form.save()
            # log the user in
            login(request, user)
            return redirect('movie-index')
        else:
            error_message = 'Invalid sign up - try again'
    form = UserCreationForm()
    context = {'form': form, 'error_message': error_message}
    return render(request, 'signup.html', context)

# Define the about view function

def about(request):
    return render(request, 'about.html')

def movie_index(request):
    # visible to everyone
    movies = Movie.objects.all().order_by('title')
    return render(request, 'movies/index.html', {'movies': movies})

def movie_detail(request, movie_id):

    # visible to everyone
    # use select/prefetch so reviews/users load efficiently
    movie = get_object_or_404(
        Movie.objects.prefetch_related('reviews__author'),
        id=movie_id
    )
    # always provide a form so logged-in users can post without error
    form = ReviewForm()
    return render(request, 'movies/detail.html', {'movie': movie, 'form': form})


# ---- WRITE (login required) ----


# Add review feature

@login_required
def add_review(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            Review.objects.create(
                movie=movie,
                author=request.user,
                rating=form.cleaned_data['rating'],
                comment=form.cleaned_data['comment']
            )
            return redirect('movie-detail', movie_id=movie.id)
    else:
        form = ReviewForm()
    return render(request, 'movies/detail.html', {'movie': movie, 'form': form, 'mode': 'Add'})


#All reviews
@login_required
def all_reviews(request):
    # visible to everyone
    reviews = Review.objects.select_related('movie', 'author').order_by('-created_at')
    return render(request, 'reviews/all_reviews.html', {'reviews': reviews})   

@login_required
def delete_review(request, review_id):
    review = get_object_or_404(Review, id=review_id)
    movie_id = review.movie.id
    review.delete()
    return redirect('movie-detail', movie_id=movie_id)

@login_required
def watchlist_index(request):
        user_watchlists = Watchlist.objects.filter(user=request.user)
        return render(request, 'watchlists/watchlist.html', {'watchlists': user_watchlists})

@login_required
def watchlist_detail(request, pk):
    watchlist = get_object_or_404(Watchlist, id=pk, user=request.user)
    return render(request, 'watchlists/detail.html', {
        'watchlist': watchlist
    })

@login_required
def add_to_watchlist(request, movie_id):
    movie = get_object_or_404(Movie, pk=movie_id)
    user_watchlist, created = Watchlist.objects.get_or_create(user=request.user) 

    if movie in user_watchlist.movies.all():
        messages.error(request, f"{movie.title} is already in your watchlist.") 
    else:
        user_watchlist.movies.add(movie) 
        messages.success(request, f"{movie.title} added to your watchlist.") 
    # Redirect back to the movie detail page 
    return redirect('movie-detail', movie_id=movie_id)

@login_required
def remove_from_watchlist(request, watchlist_movie_id, watchlist_id):
    Watchlist.objects.get(id=watchlist_id).movies.remove(watchlist_movie_id)
    return render(request, 'watchlists/watchlist.html')
    
class WatchlistCreate(LoginRequiredMixin, CreateView):
    model = Watchlist
    fields = '__all__'


class WatchlistUpdate(LoginRequiredMixin, UpdateView):
    model = Watchlist
    fields = '__all__'

class MovieCreate(LoginRequiredMixin, CreateView):
    model = Movie
    fields = '__all__'

class MovieUpdate(LoginRequiredMixin, UpdateView):
    model = Movie
    fields = ['title', 'genre', 'duration', 'release_year', 'rating', 'comments']

class MovieDelete(LoginRequiredMixin, DeleteView):
    model = Movie
    success_url = '/movies/'
