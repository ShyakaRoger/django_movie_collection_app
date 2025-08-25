from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.views import LoginView
from django.contrib.auth import views as auth_views
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib import messages
from .models import Movie, Review, Watchlist
from .forms import ReviewForm, WatchlistForm, MovieForm

DEFAULT_WATCHLIST_TITLE = "My Watchlist"

# Define the home view function
class Home(LoginView):
    template_name = 'home.html'

# custom login made inside reviews
def custom_login(request):
    return redirect('home')

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
    movie = get_object_or_404(
        Movie.objects.prefetch_related('reviews__author'),
        id=movie_id
    )

    # Only query watchlists if authenticated
    if request.user.is_authenticated:
        # ensure the user has at least one watchlist so the select isn't empty
        wl_qs = Watchlist.objects.filter(user=request.user).order_by("title")
        if not wl_qs.exists():
            Watchlist.objects.create(user=request.user, title=DEFAULT_WATCHLIST_TITLE)
            wl_qs = Watchlist.objects.filter(user=request.user).order_by("title")
        user_watchlists = wl_qs
    else:
        user_watchlists = Watchlist.objects.none()

    # Provide the review form (you can still guard posting in the POST view)
    form = ReviewForm()

    return render(
        request,
        'movies/detail.html',
        {'movie': movie, 'form': form, 'watchlists': user_watchlists})


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

    if request.method == "POST":
        watchlist_id = request.POST.get("watchlist_id")
        
        if not watchlist_id:
            messages.error(request, "No watchlist selected.")
            return redirect('movie-detail', movie_id=movie_id)

        watchlist = get_object_or_404(Watchlist, id=watchlist_id, user=request.user)
        
        if movie in watchlist.movies.all():
            messages.info(request, f"'{movie.title}' is already in '{watchlist.title}'.")
        else:
            watchlist.movies.add(movie)
            messages.success(request, f"'{movie.title}' was added to '{watchlist.title}'.")

    return redirect('movie-detail', movie_id=movie_id)

@login_required
def remove_from_watchlist(request, watchlist_id, movie_id):
    watchlist = get_object_or_404(Watchlist, id=watchlist_id, user=request.user)
    movie = get_object_or_404(Movie, id=movie_id)

    if movie in watchlist.movies.all():
        watchlist.movies.remove(movie)
        messages.success(request, f"'{movie.title}' removed from '{watchlist.title}'.")
    else:
        messages.info(request, f"'{movie.title}' is not in '{watchlist.title}'.")

    return redirect('watchlist-detail', pk=watchlist_id)
    
class WatchlistCreate(LoginRequiredMixin, CreateView):
    model = Watchlist
    form_class = WatchlistForm
    template_name = 'main_app/watchlist_form.html'

    def form_valid(self, form):
        form.instance.user = self.request.user  # Set the user before saving
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('watchlist-detail', kwargs={'pk': self.object.pk})

class WatchlistUpdate(LoginRequiredMixin, UpdateView):
    model = Watchlist
    form_class = WatchlistForm
    template_name = 'main_app/watchlist_form.html'

    def get_queryset(self):
        return Watchlist.objects.filter(user=self.request.user)

    def get_success_url(self):
        return reverse_lazy('watchlist-detail', kwargs={'pk': self.object.pk})

class WatchlistDelete(LoginRequiredMixin, DeleteView):
    model = Watchlist
    success_url = '/watchlists/'

class MovieCreate(LoginRequiredMixin, CreateView):
    model = Movie
    form_class = MovieForm
    template_name = 'main_app/movie_form.html'

    def get_success_url(self):
        return reverse_lazy('movie-detail', kwargs={'movie_id': self.object.pk})


class MovieUpdate(LoginRequiredMixin, UpdateView):
    model = Movie
    form_class = MovieForm
    template_name = 'main_app/movie_form.html'
    success_url = '/movies/'

  


class MovieDelete(LoginRequiredMixin, DeleteView):
    model = Movie
    success_url = '/movies/'

