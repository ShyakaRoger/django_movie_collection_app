from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Movie, Review
from .forms import ReviewForm


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


# Add review feature
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
def all_reviews(request):
    reviews = Review.objects.all().order_by('-created_at')
    return render(request, 'reviews/all_reviews.html', {'reviews': reviews})   
 
# Adding review delete funtionality
def delete_review(request, review_id):
    review = get_object_or_404(Review, id=review_id)
    movie_id = review.movie.id
    review.delete()
    return redirect('movie-detail', movie_id=movie_id)



class MovieCreate(CreateView):
    model = Movie
    fields = '__all__'

class MovieUpdate(UpdateView):
    model = Movie
    fields = '__all__'

class MovieDelete(DeleteView):
    model = Movie
    success_url = '/movies/'


