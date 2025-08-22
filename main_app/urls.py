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

    #view user watchlists
    path('watchlists/', views.watchlist_index, name='user-watchlists'),

    # create multiple watchlists
    path('watchlists/create/', views.WatchlistCreate.as_view(), name = 'watchlist-create'),

    path('watchlists/<int:pk>/', views.watchlist_detail, name='watchlist-detail'),

    path('watchlists/<int:pk>/update/', views.WatchlistUpdate.as_view(), name='watchlist-update'),


    #add movie to watchlist
    path('movie/<int:movie_id>/add_to_watchlist', views.add_to_watchlist, name='add_to_watchlist'),

    #remove movie from watchlist
    path('movie/<int:movie_id>/remove_from_watchlist', views.remove_from_watchlist, name='remove_from_watchlist'),
]