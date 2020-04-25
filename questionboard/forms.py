from django import forms
from .models import QPost, QComment
from martor.fields import MartorFormField

class QPostForm(forms.ModelForm):
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
        model = QPost
        fields = ['title', 'content', 'password']

class QCommentForm(forms.ModelForm):
    content = forms.CharField(
        label='',
        label_suffix='',
        widget=forms.TextInput(
            attrs = {
                'placeholder': '댓글을 입력하세요.',
                'class': 'commentinput input-responsive',
            }
        )
    )
    class Meta:
        model = QComment
        fields = ['content']