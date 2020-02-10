from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.db import transaction
from django.db.models import Q
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from googletrans import Translator

from .models import Category, Favorite, Product
from .forms import RegisterForm, ParagraphErrorList
from .query_parser import QueryParser


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

def fctSortDict(value):
    # permet de trier la liste contenat les dictionnaire en fonction du nombre trouvé
    return value['nb']

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
    #get product we want to substitute
    product = Product.objects.get(id=product_id)
    paginate = False

    # found categories linked to this product
    found_categories = Category.objects.filter(products__id=product_id)
    # get reference of product loaded in results
    reference_prod_loaded = []
    results = []

    #for each category of the product asked
    for category in found_categories:
        # for product in this category
        for prod in Product.objects.filter(categories__reference=category.reference):
            if prod.reference in reference_prod_loaded:
                pass
            else:
                if prod.nutrition_grade_fr < product.nutrition_grade_fr:
                    count_same_cat = 0 #count nb of categories in common
                    cats = [] #name of those categories
                    for cat in Category.objects.filter(products__name=prod.name):
                        if cat in found_categories:
                            if cat not in cats:
                                cats.append(cat)
                                count_same_cat += 1
                    # get informations in dictionnary contained in the list results
                    results.append({'name':prod.name, 'reference':prod.reference, 'nb':count_same_cat, 'cats_list':cats})
                    reference_prod_loaded.append(prod.reference)

    # get the 24 firsts most relevant products in an ordered queryset
    results = sorted(results, key=fctSortDict, reverse=True)
    results20 = results[0:24]
    q_objects = Q()
    for item in results20:
        q_objects.add(Q(reference=item['reference']), Q.OR)
    result_list = Product.objects.filter(q_objects).order_by('nutrition_grade_fr')

    if result_list.count() != 0:
        paginate = True

    if paginate:
        paginator = Paginator(result_list, 6)
        page = request.GET.get('page')
        result = paginator.get_page(page)

    context = {
        'product':product,
        'result': result,
        "paginate":paginate
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

def save_favorite(request, product_id, substitute_id):
    product = Product.objects.get(id=product_id)
    substitute = Product.objects.get(id=substitute_id)
    
    return redirect('foodSearch:watchlist')
