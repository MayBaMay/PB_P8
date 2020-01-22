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
    paginate = False

    if query=="":
        result = []
    else:
        # checks first category of the first product containing the query
        # categories references are in english and using app language french => translation
        translator = Translator()
        try:
            query_translated = translator.translate(query).text
            found_category = Category.objects.filter(reference__icontains=query_translated)
        except:
            found_category = Category.objects.filter(reference__icontains=query)

        # or find products with the user query
        if found_category.exists():
            # get all products with a category containing the query
            q_objects = Q()
            for category in found_category:
                q_objects.add(Q(categories__reference=category.reference), Q.OR)
            result_list = Product.objects.filter(q_objects).distinct().order_by('nutrition_grade_fr')[0:24]
            if result_list.count() != 0:
                paginate = True

        elif Product.objects.filter(name__icontains=query).exists():
            found_product = Product.objects.filter(name__icontains=query)
            found_product_name = found_product[0].name
            found_categories = Category.objects.filter(products__name=found_product_name)#[0].reference

            reference_prod_loaded = []
            results = []

            for nb in range(0,found_categories.count()): #pour chaque category liée au produit recherché$
                for prod in Product.objects.filter(categories__reference=found_categories[nb].reference):
                    if prod.reference in reference_prod_loaded:
                        pass
                    else:
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

            # get the 20 firsts most relevant products in an ordered queryset
            results = sorted(results, key=fctSortDict, reverse=True)
            results20 = results[0:24]
            q_objects = Q()
            for item in results20:
                q_objects.add(Q(reference=item['reference']), Q.OR)
            result_list = Product.objects.filter(q_objects).order_by('nutrition_grade_fr')

            if result_list.count() != 0:
                paginate = True


        else :
            result = []

    if paginate:
        paginator = Paginator(result_list, 6)
        page = request.GET.get('page')
        result = paginator.get_page(page)

    context = {
        'title':title,
        'result': result,
        'query':query,
        "paginate":paginate
    }
    return render(request, 'foodSearch/search.html', context)

def checkbox_products(request):
    product_on_watchlist = request.POST.get('checks')
