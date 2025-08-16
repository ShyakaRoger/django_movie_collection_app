from django.urls import path
from . import views # Import views to connect routes to view functions

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('movies/', views.movie_index, name='movie-index'),

    path('movies/<int:movie_id>/', views.movie_detail, name='movie-detail')

    
]