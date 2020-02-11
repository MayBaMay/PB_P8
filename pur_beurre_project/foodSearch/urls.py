from django.urls import path, re_path

from . import views # import views so we can use them in urls.

app_name = 'foodSearch'

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('search/', views.search, name='search'),
    path('results/<int:product_id>/', views.results, name='results'),
    path('detail/<int:product_id>/', views.detail, name='detail'),
    path('userpage/', views.userpage, name='userpage'),
    path('save_favorite/<int:substitute_id>/<int:product_id>/', views.save_favorite, name='save_favorite'),
    path('watchlist/', views.watchlist, name='watchlist'),
    # path('get_initial_search_product_in_wachlist/', views.get_initial_search_product_in_wachlist, name='get_initial_search_product_in_wachlist')
]
