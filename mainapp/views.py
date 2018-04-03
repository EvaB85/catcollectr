from django.shortcuts import render, redirect, get_object_or_404
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

def like_cat(request):
    cat_id = request.GET.get('cat_id', None)
    likes = 0
    if (cat_id):
        cat = Cat.objects.get(id=int(cat_id))
        if cat is not None:
            likes = cat.likes + 1
            cat.likes = likes
            cat.save()
    return HttpResponse(likes)

def edit_cat(request, cat_id):
    instance = get_object_or_404(Cat, id=cat_id)
    form = CatForm(request.POST or None, instance=instance)
    if form.is_valid():
        form.save()
        return redirect('show', cat_id)
    return render(request, 'edit_cat.html', {'cat': instance, 'form': form})

def delete_cat(request, cat_id):
    if request.method == 'POST':
        instance = Cat.objects.get(pk=cat_id)
        instance.delete()
        return redirect('index')
