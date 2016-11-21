from django.db import models

# Create your models here.


class Article(models.Model):
    """docstring for Article"""
    class Meta():
        db_table = "article"
    article_title = models.CharField(max_length=200)
    article_text = models.TextField()
    article_date = models.DateTimeField()
    article_likes = models.IntegerField(default=0)


class Comment(models.Model):

    class Meta():
        db_table = "comments"

    comments_text = models.TextField(verbose_name='Текст комментария')
    comments_author = models.CharField(
        max_length=100, default='anonymous', verbose_name='Автор')
    comments_article = models.ForeignKey(Article)
