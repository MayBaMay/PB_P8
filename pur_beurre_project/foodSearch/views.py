from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.db import transaction

from .models import Category, Favorite, Product
from .forms import RegisterForm, ParagraphErrorList


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
    title = 'Mes aliments'
    context = {'title':title}
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
        answer = Product.objects.all()[:12]
    else:

        # get first category containing the query
        querycat = Category.objects.filter(reference__icontains=query)
        if querycat.exists(): # checks if it is a category (ex: query=soda)
            # get products form this category
            answer = Product.objects.filter(categories__reference=querycat[0].reference)

        else:   # query should be a product

            # checks first category of the first product containing the query
            found_product_name = Product.objects.filter(name__icontains=query)[0].name
            found_category_ref = Category.objects.filter(products__name=found_product_name)[0].reference
            # find products from same category
            answer = Product.objects.filter(categories__reference=found_category_ref)

        # in any case order by nutrition_grade
        answer = answer.order_by('nutrition_grade_fr')


        # prod = Category.objects.all()[:12]
            # if not prod.exists():
            #     prod = prod[:1]

    #     prod = Product.objects.filter(categorie__name__icontains=query)
    context = {
        'title':title,
        'answer': answer,
        'query':query,
    }
    return render(request, 'foodSearch/search.html', context)

def checkbox_products(request):
    product_on_watchlist = request.POST.get('checks')
