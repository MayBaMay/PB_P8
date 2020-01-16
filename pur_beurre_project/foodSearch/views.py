from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

from .models import Category, Favorite, Product
from .forms import RegisterForm, ParagraphErrorList


def index(request):
    return render(request, 'foodSearch/index.html')

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST, error_class=ParagraphErrorList)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('foodSearch:index')
    else:
        form = RegisterForm()

    context = {'form' : form}
    return render(request, 'registration/register.html', context)

def search(request):
    query = request.GET.get('query')
    # if not query:
    #     products = Product.objects.all()
    # else:
    #     products = Product.objects.filter(name__icontains=query)
    # if not products.exists():
    #     products = Product.objects.filter(categorie__name__icontains=query)
    # title = "Résultats pour la requête %s"%query
    context = {
        'query': query,
    }
    return render(request, 'foodSearch/index.html', context)
