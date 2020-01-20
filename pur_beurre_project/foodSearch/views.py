from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.db import transaction
from django.db.models import Q

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

    if query=="":
        answer = Product.objects.all()[:12]
    else:

        # get first category containing the query
        querycat = Category.objects.filter(reference__icontains=query)

        # checks first category of the first product containing the query
        found_product = Product.objects.filter(name__icontains=query)

        if found_product.exists():
            found_product_name = found_product[0].name
            found_categories = Category.objects.filter(products__name=found_product_name)#[0].reference

            reference_prod_loaded = []
            results = []

            for nb in range(0,found_categories.count()): #pour chaque category liée au produit recherché$
                for prod in Product.objects.filter(categories__reference=found_categories[nb].reference):
                    if prod.reference in reference_prod_loaded:
                        pass
                    else:
                        # print(prod.name, found_categories[nb].reference)
                        count_same_cat=0 #count nb of categories in common
                        cats = [] #name of those categories
                        for cat in Category.objects.filter(products__name=prod.name):
                            if cat in found_categories:# cat à la fois du produit de base et du produit comparé
                                if cat not in cats:
                                    cats.append(cat)
                                    count_same_cat += 1
                                    # complète la liste par un dictionnaire comprenant les informations
                        results.append({'name':prod.name, 'reference':prod.reference, 'nb':count_same_cat, 'cats_list':cats})
                        reference_prod_loaded.append(prod.reference)

            results = sorted(results, key=fctSortDict, reverse=True)

        # in any case order by nutrition_grade
            answer = Product.objects.filter(Q(reference=results[0]['reference'])|
                                            Q(reference=results[1]['reference'])|
                                            Q(reference=results[2]['reference'])|
                                            Q(reference=results[3]['reference'])|
                                            Q(reference=results[4]['reference'])|
                                            Q(reference=results[5]['reference'])|
                                            Q(reference=results[6]['reference'])|
                                            Q(reference=results[7]['reference'])|
                                            Q(reference=results[8]['reference'])|
                                            Q(reference=results[9]['reference'])|
                                            Q(reference=results[10]['reference'])|
                                            Q(reference=results[11]['reference'])|
                                            Q(reference=results[12]['reference'])|
                                            Q(reference=results[13]['reference'])|
                                            Q(reference=results[14]['reference'])|
                                            Q(reference=results[15]['reference'])|
                                            Q(reference=results[16]['reference'])|
                                            Q(reference=results[17]['reference'])|
                                            Q(reference=results[18]['reference'])|
                                            Q(reference=results[19]['reference'])|
                                            Q(reference=results[19]['reference']))
            answer = answer.order_by('nutrition_grade_fr')

        else :
            answer = []

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
