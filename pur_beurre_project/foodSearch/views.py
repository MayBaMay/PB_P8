from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout


def index(request):
    return render(request, 'foodSearch/index.html')

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            redirect('index')
    else:
        form = UserCreationForm()

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
