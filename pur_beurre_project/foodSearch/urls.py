from django.urls import path, re_path

from . import views # import views so we can use them in urls.

app_name = 'foodSearch'

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('search/', views.search, name='search'),
    path('userpage/', views.userpage, name='userpage'),
    path('watchlist/', views.watchlist, name='watchlist'),
    path('checkbox_products', views.checkbox_products, name='checkbox_products'),
]
