from django import forms
from .models import Review, Watchlist

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 4}),
        }
class WatchlistForm(forms.ModelForm):
    class Meta:
        model = Watchlist
        fields = ['title', 'movies']  # Allow users to select movies
        widgets = {
            'movies': forms.CheckboxSelectMultiple(),  # Display movies as checkboxes
        }
