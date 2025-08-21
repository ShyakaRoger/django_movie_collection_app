from django.urls import path
from . import views # Import views to connect routes to view functions

urlpatterns = [
    path('accounts/signup/', views.signup, name='signup'),

    path('', views.Home.as_view(), name='home'),
    path('about/', views.about, name='about'),
    path('movies/', views.movie_index, name='movie-index'),
    path('movies/<int:movie_id>/', views.movie_detail, name='movie-detail'),
    path('movies/create/', views.MovieCreate.as_view(), name='movie-create'),
    path('movies/<int:pk>/update/', views.MovieUpdate.as_view(), name='movie-update'),
    path('movies/<int:pk>/delete/', views.MovieDelete.as_view(), name='movie-delete'),

    # adding a review
    path('movies/<int:movie_id>/reviews/add/', views.add_review, name='review-add'),
    
    #all reviews 
    path('reviews/', views.all_reviews, name='all-reviews'),

    #deleting a review
    path('reviews/<int:review_id>/delete/', views.delete_review, name='review-delete'),
]