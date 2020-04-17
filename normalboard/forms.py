from django import forms
from .models import Post
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
    # content = forms.CharField(
    #     label='내용',
    #     label_suffix='',
    #     widget=forms.Textarea(
    #         attrs = {
    #             'placeholder':'글 내용을 입력하세요.',
    #             'class': 'form',
    #         }
    #     )
    # )
    content = MartorFormField()
    password = forms.CharField(
        label='글 비밀번호',
        label_suffix='',
        widget=forms.PasswordInput(
            attrs = {
                'class': 'form',
            }
        )
    )
    class Meta:
        model = Post
        fields = ['title', 'content', 'password']

