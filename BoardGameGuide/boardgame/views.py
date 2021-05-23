from django.db.models import Q
from django.shortcuts import redirect, render, get_object_or_404
from .models import *

# Create your views here.

def main(request):
    gameList = Game.objects.all()
    return render(request, 'main.html', {'gameList': gameList})

def search(request):
    if 'search_value' in request.POST:
        word = request.POST['search_value']
        gameList = Game.objects.all().filter(name__icontains=word).distinct()
    return render(request, 'search.html', {'word' : word, 'gameList': gameList})

def login(request):
    return render(request, 'login.html')

def signup(request):
    return render(request, 'signup.html')

def mypage(request):
    return render(request, 'mypage.html')

def game(request):
    return render(request, 'game.html')