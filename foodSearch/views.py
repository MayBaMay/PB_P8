from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.db import transaction
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.views.generic.edit import FormView
from django.urls import resolve
from django.http import HttpResponse, HttpResponseRedirect
from django.http import JsonResponse

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

def register_view(request):
    response_data = {}
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        try:
            user = User.objects.get(username=username)
            response_data = {'user':"already in DB"}
        except User.DoesNotExist:
            user = User.objects.create(username=username, email=email, password=password)
            user.save()
            log_user = authenticate(username=username, password=password)
            login(request, user)
            response_data = {'user':"success"}
    return HttpResponse(JsonResponse(response_data))

def login_view(request):
    response_data = {}
    if request.method == 'POST':

        username = request.POST['username']
        password = request.POST['password']
        try:
            get_user = User.objects.get(username=username)
            if get_user.check_password(password):
                user = authenticate(username=username, password=password)
                if user is not None:
                    login(request, user)
                    response_data = {'user':"success"}
                else:
                    response_data = {'user':"user unknown"}
            else:
                response_data = {'user':"password wrong"}
        except User.DoesNotExist:
            response_data = {'user':"user unknown"}
        return HttpResponse(JsonResponse(response_data))


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
    current_user = request.user
    parser = ResultsParser(product_id, current_user)
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
    try:
        current_user = request.user
        substitute = Product.objects.get(id=substitute_id)
        product = Product.objects.get(id=product_id)
        Favorite.objects.create(user=current_user, substitute=substitute, initial_search_product=product)
    except:
        pass
    return redirect('/results/{}/?page={}'.format(product_id, page))

def delete_favorite_from_result(request, substitute_id, product_id, page):
    try:
        current_user = request.user
        substitute = Product.objects.get(id=substitute_id)
        product = Product.objects.get(id=product_id)
        Favorite.objects.get(user=current_user, substitute=substitute).delete()
    except:
        pass
    return redirect('/results/{}/?page={}'.format(product_id, page))

def delete_favorite_from_watchlist(request, substitute_id, page):
    current_user = request.user
    substitute = Product.objects.get(id=substitute_id)
    Favorite.objects.get(user=current_user, substitute=substitute).delete()
    return redirect('/watchlist/?page={}'.format(page))
