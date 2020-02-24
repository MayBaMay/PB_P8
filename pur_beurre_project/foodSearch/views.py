from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.db import transaction
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from .models import Category, Favorite, Product
from .forms import RegisterForm, ParagraphErrorList
from .query_parser import QueryParser
from .results_parser import ResultsParser


def index(request):
    return render(request, 'foodSearch/index.html')

def legals(request):
    context = {
        'title':'Mentions légales'
    }
    return render(request, 'foodSearch/legals.html', context)

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

def login_request(request):
    page = request.META.get('HTTP_REFERER')
    if request.method == 'POST':
        form = AuthenticationForm(request,request.POST)
        if form.is_valid():
            username = form.cleaned_data('email')
            password = form.cleaned_data('password')
            user = authenticate(username, password)
            if user is not None:
                login(request, user)
    form = AuthenticationForm()
    context = {
        'form':form
    }
    return render(request, page, context)

def logout_request(request):
    page = request.META.get('HTTP_REFERER')
    logout(request)
    return render(request, page)


def userpage(request):
    title = request.user
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
    page = request.GET.get('page')
    user_watchlist = Favorite.objects.filter(user=current_user)

    if user_watchlist.count() > 6 :
        paginate = True
    else :
        paginate = False

    if paginate:
        paginator = Paginator(user_watchlist, 6)
        watchlist = paginator.get_page(page)
    else:
        watchlist = user_watchlist

    if page == None:
        page = 1

    context = {
        'page':page,
        'title':title,
        'watchlist':watchlist,
        'paginate':paginate
    }
    return render(request, 'foodSearch/watchlist.html', context)

def search(request):
    query = request.GET.get('query')
    title = query

    if query=="":
        found_products = []
    else:
        parser = QueryParser(query)

    context = {
        'title' : title,
        'found_products': parser.product_list[0:12],
    }
    return render(request, 'foodSearch/search.html', context)

def results(request, product_id):
    title = Product.objects.get(id=product_id).name
    page = request.GET.get('page')
    parser = ResultsParser(product_id)
    if page == None:
        page = 1
    context = {
        'title':title,
        'product':parser.product,
        'result': parser.paginator(page),
        'page':page,
        "paginate": True
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

def save_favorite(request, substitute_id, product_id, page):
    current_user = request.user
    substitute = Product.objects.get(id=substitute_id)
    product = Product.objects.get(id=product_id)
    Favorite.objects.create(user=current_user, substitute=substitute, initial_search_product=product)
    return redirect('/results/{}/?query=&page={}'.format(product_id, page))

def delete_favorite_from_result(request, substitute_id, product_id, page):
    current_user = request.user
    substitute = Product.objects.get(id=substitute_id)
    product = Product.objects.get(id=product_id)
    Favorite.objects.get(substitute=substitute).delete()
    return redirect('/results/{}/?query=&page={}'.format(product_id, page))

def delete_favorite_from_watchlist(request, substitute_id, page):
    current_user = request.user
    substitute = Product.objects.get(id=substitute_id)
    Favorite.objects.get(substitute=substitute).delete()
    return redirect('/watchlist/?page={}'.format(page))
