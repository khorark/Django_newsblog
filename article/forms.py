from django.forms import ModelForm
from article.models import Comment


class CommentForm(ModelForm):

    class Meta:
        model = Comment
        fields = ('comments_author', 'comments_text')
