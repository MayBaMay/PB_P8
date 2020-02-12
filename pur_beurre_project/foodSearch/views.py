from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.db import transaction
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from googletrans import Translator

from .models import Category, Favorite, Product
from .forms import RegisterForm, ParagraphErrorList
from .query_parser import QueryParser
from .results_parser import ResultsParser
from .favorite import SaveFavorite


def index(request):
    return render(request, 'foodSearch/index.html')

def userpage(request):
    title = 'Mon compte'
    context = {'title':title}
    if request.user.is_authenticated:
        username = request.user.username
        email = request.user.email
        context['username'] = username
        context['email'] = email
    return render(request, 'foodSearch/userpage.html', context)

def watchlist(request):
    current_user = request.user
    title = 'Mes aliments'
    user_watchlist = Favorite.objects.filter(user=current_user)
    context = {
        'title':title,
        'user_watchlist':user_watchlist
    }
    return render(request, 'foodSearch/watchlist.html', context)


def register(request):
    title = 'Créer un compte'
    if request.method == 'POST':
        form = RegisterForm(request.POST, error_class=ParagraphErrorList)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('foodSearch:index')
    else:
        form = RegisterForm()

    context = {
        'title':title,
        'form':form
        }
    return render(request, 'registration/register.html', context)

def search(request):
    query = request.GET.get('query')
    title = 'Aliment cherché'

    if query=="":
        found_products = []
    else:
        parser = QueryParser(query)

    context = {
        'found_products': parser.product_list[0:12],
    }
    return render(request, 'foodSearch/search.html', context)

def results(request, product_id):

    parser = ResultsParser(product_id)

    if parser.paginate:
        paginator = Paginator(parser.results_infos, 6)
        page = request.GET.get('page')
        page_results = paginator.get_page(page)

    context = {
        'product':parser.product,
        'result': page_results,
        "paginate":parser.paginate
    }
    return render(request, 'foodSearch/results.html', context)

def detail(request, product_id):
    product = Product.objects.get(id=product_id)
    found_categories = Category.objects.filter(products__name=product.name)
    context = {
        'product':product,
        'found_categories':found_categories
    }
    return render(request, 'foodSearch/detail.html', context)

def save_favorite(request, substitute_id, product_id):
    current_user = request.user
    substitute = Product.objects.get(id=substitute_id)
    product = Product.objects.get(id=product_id)
    favorite = SaveFavorite(current_user, substitute, product)
    favorite.find_favorite()
    page = request.GET.get('page')
    context = {
        'product':product,
        'page':page
    }
    return render(request, 'foodSearch/results.html', context)
