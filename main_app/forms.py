from django import forms
from .models import Review, Watchlist, Movie

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 4}),
        }

class WatchlistForm(forms.ModelForm):
    movies = forms.ModelMultipleChoiceField(
        queryset=Movie.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    class Meta:
        model = Watchlist
        fields = ['title', 'movies'] 


class MovieForm(forms.ModelForm):
    class Meta:
        model = Movie
        fields = ['title', 'genre', 'duration', 'release_year', 'poster_url']
      
        
        
