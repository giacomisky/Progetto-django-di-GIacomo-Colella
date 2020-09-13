from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, JsonResponse

from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from .models import UserProfile
from .forms import RegisterForm, LoginForm
from django.urls import reverse
from django.contrib import messages
from user.models import Post

def getIpAdd(request):
    try:
        x_forward = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forward:
            ip = x_forward.split(",")[0]
        else:
            ip = request.META.get("REMOTE_ADDR")
    except:
        ip = ""
    return ip

def log(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        print(form.is_valid())
        if form.is_valid():
            #Accesso utente
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            try:
                lastIp = UserProfile.objects.get(user=user)
                lastIp.ipAddress = getIpAdd(request)
                lastIp.save()
            except:
                pass
            finally:
                messages.success(request, 'Indirizzo IP aggiornato con successo')
            if user is not None:
                if user.is_superuser:
                    login(request, user)
                    return redirect('managing/')
                else:
                    login(request, user)
                    return redirect('home/')
    else:
        form = LoginForm()
        return render(request, 'login/login.html', {'form':form})

def registration(request):
    #Registrazione utente
    try:
        ip = getIpAdd(request)
    except:
        pass
    form = RegisterForm(request.POST)
    if form.is_valid():
        user = form.save()
        thisUser = UserProfile()
        thisUser.user = user
        thisUser.ipAddress = ip
        thisUser.save()
        return redirect('/home/')
    else:
        form = RegisterForm()
        return render(request, 'login/registration.html', {'form':form})

def detUser(request, pk):
    user = User.objects.filter(id=pk).values()
    return render(request, 'login/url_page.html', {'user':user})
