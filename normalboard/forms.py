from django import forms
from .models import Post

class PostForm(forms.ModelForm):
    title = forms.CharField(
        label='글 제목',
        widget=forms.TextInput(
            attrs = {
                'placeholder':'글 제목을 입력하세요.',
            }
        )
    )
    content = forms.CharField(
        label='내용',
        widget=forms.Textarea(
            attrs = {
                'placeholder':'글 내용을 입력하세요.',
            }
        )
    )
    password = forms.CharField(
        label='글 비밀번호',
        widget=forms.PasswordInput()
    )
    class Meta:
        model = Post
        fields = ['title', 'content', 'password']