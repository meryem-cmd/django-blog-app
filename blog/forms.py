from django import forms
from .models import Blog

class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ["title", "content", "is_published", "visibility"]
        widgets = {
            "is_published": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "visibility": forms.RadioSelect(),
        }
        labels = {
            "is_published": "Publish now (uncheck to save as draft)",
            "visibility": "Who can read this post?",
        }