from django.conf.urls import url
from article import views

urlpatterns = [
    url(r'^1/', views.basic_one),
    url(r'^2/', views.template_two),
    url(r'^3/', views.template_three),
    #url(r'^articles/all/$', views.articles),
    url(r'^articles/get/(?P<article_id>\d)+/$', views.article),
    url(r'^articles/addlike/(?P<article_id>\d)+/$', views.addlike),
    url(r'^articles/addcomment/(?P<article_id>\d)+/$', views.addcomment),
    #url(r'^page/\d+/$', views.articles),
    url(r'^', views.articles),

]
