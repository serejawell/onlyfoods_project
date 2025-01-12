from django import forms

from posts.models import Post


class StyleFormMixin:

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

class PostCreateForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content','image','is_premium']

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'image']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Название вашего поста'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Описание'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
        }