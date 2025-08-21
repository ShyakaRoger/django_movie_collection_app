from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.views import LoginView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Movie, Review
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
    # render the movies/index.html template with the movies data
    movies = Movie.objects.all().order_by('title')
    return render(request, 'movies/index.html', {'movies': movies})

@login_required
def movie_detail(request, movie_id):

    #I changed pk back to movie_id. I was getting an error that it wasnt matching up to the url when navigating to a movie detail
    movie = get_object_or_404(Movie, id=movie_id)
    return render(request, 'movies/detail.html', {'movie': movie})


# Add review feature
@login_required
def add_review(request, movie_id):
    movie=get_object_or_404(Movie, id=movie_id)

    if request.method =='POST':
        form=ReviewForm(request.POST)
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
    reviews = Review.objects.all().order_by('-created_at')
    return render(request, 'reviews/all_reviews.html', {'reviews': reviews})   
 
# Adding review delete funtionality
@login_required
def delete_review(request, review_id):
    review = get_object_or_404(Review, id=review_id)
    movie_id = review.movie.id
    review.delete()
    return redirect('movie-detail', movie_id=movie_id)



class MovieCreate(LoginRequiredMixin, CreateView):
    model = Movie
    fields = '__all__'

class MovieUpdate(LoginRequiredMixin, UpdateView):
    model = Movie
    fields = '__all__'

class MovieDelete(LoginRequiredMixin, DeleteView):
    model = Movie
    success_url = '/movies/'


