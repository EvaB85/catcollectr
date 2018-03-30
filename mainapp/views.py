from django.shortcuts import render
from .models import Cat
from .forms import CatForm, LoginForm, SignUpForm
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
# from django.http import HttpResponse

# Create your views here.

def index(request):
    cats = Cat.objects.all()
    form = CatForm()
    return render(request, 'index.html', {'cats': cats, 'form': form})


def show(request, cat_id):
    cat = Cat.objects.get(id=cat_id)
    return render(request, 'show.html', {'cat': cat})

def post_cat(request):
    form = CatForm(request.POST)
    if form.is_valid():
        cat = form.save(commit = False)
    cat.user = request.user
    cat.save()
    return HttpResponseRedirect('/')

def profile(request, username):
    user = User.objects.get(username=username)
    cats = Cat.objects.filter(user=user)
    return render(request, 'profile.html', {'username': username, 'cats': cats})

def login_view(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            u = form.cleaned_data['username']
            p = form.cleaned_data['password']
            user = authenticate(username = u, password = p)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect('/')
                else:
                    print("This account")
            else:
                print("The username and or password is incorrect")
    else:
        form = LoginForm()
        return render(request, 'login.html', {'form':form})

def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/')

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect ('/')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})
