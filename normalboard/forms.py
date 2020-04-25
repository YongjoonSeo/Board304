from django import forms
from .models import Post, Comment
from martor.fields import MartorFormField

class PostForm(forms.ModelForm):
    title = forms.CharField(
        label='글 제목',
        label_suffix='',
        widget=forms.TextInput(
            attrs = {
                'placeholder':'글 제목을 입력하세요.',
                'class': 'form',
            }
        )
    )
    content = MartorFormField()
    password = forms.CharField(
        label='글 비밀번호 설정',
        label_suffix='',
        widget=forms.PasswordInput(
            attrs = {
                'class': 'form password-form',
            }
        )
    )
    class Meta:
        model = Post
        fields = ['title', 'content', 'password']

class CommentForm(forms.ModelForm):
    content = forms.CharField(
        label='',
        label_suffix='',
        widget=forms.TextInput(
            attrs = {
                'placeholder': '댓글을 입력하세요.',
            }
        )
    )
    class Meta:
        model = Comment
        fields = ['content']