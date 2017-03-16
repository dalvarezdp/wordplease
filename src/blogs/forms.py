from django import forms

from blogs.models import Post, Category


class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ["title", "subtitle", "description", "image", "categories", "date_public"]
        widgets = {
            'title': forms.TextInput(attrs={'class': "form-control", 'placeholder': 'Title'}),
            'subtitle': forms.TextInput(attrs={'class': "form-control", 'placeholder': 'Subtitle'}),
            'description': forms.Textarea(attrs={'class': "form-control", 'placeholder': 'Description'}),
            'categories': forms.SelectMultiple(attrs={'class': "form-control"}),
            'date_public': forms.DateTimeInput(format='%Y-%m-%d %H:%M:%S', attrs={'class': "form-control", 'placeholder': 'YYYY-MM-DD HH-MM-SS'})
        }
