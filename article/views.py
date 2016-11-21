from django.shortcuts import render_to_response, redirect
from django.http.response import HttpResponse, Http404
from django.template.loader import get_template
from django.template import Context
from article.models import Article, Comment
from django.core.exceptions import ObjectDoesNotExist
from article.forms import CommentForm
from django.template.context_processors import csrf
from django.contrib import auth
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


# Create your views here.


def basic_one(request):
    view = "basic_one"
    html = "<html><body><p>This is {} func</p></body></html>".format(view)
    return HttpResponse(html)


def template_two(request):
    view = "template_two"
    t = get_template('my_view.html')
    html = t.render(Context({'name': view}))
    return HttpResponse(html)


def template_three(request):
    name = 'Simle template'
    return render_to_response('my_view.html', {'name': name})


def articles(request):
    all_articles = Article.objects.all().order_by('-article_date')
    paginator = Paginator(all_articles, 3)
    page = request.GET.get('page')
    try:
        contacts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        contacts = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        contacts = paginator.page(paginator.num_pages)
    return render_to_response('articles.html', {'articles': contacts, 'username': auth.get_user(request).username})


# def article(request, article_id=1):
# return render_to_response('article.html', {'article':
# Article.objects.get(id=article_id), 'comments':
# Comment.objects.filter(comments_article_id=article_id)})

def article(request, article_id=1):
    comment_form = CommentForm
    args = {}
    args.update(csrf(request))
    args['article'] = Article.objects.get(id=article_id)
    all_comments = Comment.objects.filter(comments_article_id=article_id)
    paginator = Paginator(all_comments, 3)
    page = request.GET.get('page')
    try:
        args['comments'] = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        args['comments'] = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        args['comments'] = paginator.page(paginator.num_pages)
    args['form'] = comment_form
    args['username'] = auth.get_user(request).username
    return render_to_response('article.html', args)


def addlike(request, article_id):
    try:
        if article_id not in request.COOKIES:
            article = Article.objects.get(id=article_id)
            article.article_likes += 1
            article.save()
            response = redirect(request.META.get('HTTP_REFERER'))
            response.set_cookie(article_id, "like_add")
            return response
    except ObjectDoesNoExist:
        raise Http404
    return redirect(request.META.get('HTTP_REFERER'))


def addcomment(request, article_id):
    if request.POST and ('pause' not in request.session):
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            # comment.comments_article = Article.objects.get(id=article_id)
            comment.comments_article_id = article_id
            form.save()
            # сессия существует в течении 60 сек
            request.session.set_expiry(60)
            request.session['pause'] = True
    return redirect('/articles/get/%s/' % article_id)
