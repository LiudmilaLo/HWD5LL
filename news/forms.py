from django.forms import ModelForm
from .models import *


class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ('author', 'categoryType', 'title', 'text')


class AuthorForm(ModelForm):
    class Meta:
        model = Author
        fields = '__all__'
