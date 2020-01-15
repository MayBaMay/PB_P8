from django.urls import path
from django.conf.urls import url

from . import views # import views so we can use them in urls.

app_name = 'foodSearch'

urlpatterns = [
    path('', views.index, name='index'),
    url(r'^register/$', views.register, name='register'),
    url(r'^search/$', views.search, name='search'),
]
