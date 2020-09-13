from django.shortcuts import render
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse

from django.contrib.auth.models import User
from datetime import timedelta
from django.utils import timezone
from django.urls import reverse
import math
from .models import Post


def homePage(request):
    if request.method == 'POST':
        
        messaggio = request.POST
        if 'hack' in messaggio['msg'] or 'Hack' in messaggio['msg']:
            return HttpResponse('<h1>Errore di inserimento. Riprova.</h1>')
        else:
            new_post = Post(user=request.user, content=messaggio['msg'])
            new_post.setDate()
            new_post.save()
            response = []
            posts = Post.objects.filter().order_by('-published_date')
            for post in posts:
                response.append({
                    'content': post.content,
                    'author': f"{post.user}",
                    'published_date': post.published_date
                })

            return render(request, 'user/home_page.html', {'post':response})
    else:
        response = []
        posts = Post.objects.filter().order_by('-published_date')
        for post in posts:
            response.append({
                'content': post.content,
                'author': f"{post.user}",
                'published_date': post.published_date
            })

        return render(request, 'user/home_page.html', {'post':response})


def lastPosts(request):
    lasPosts = {}
    now = timezone.now()
    posts = Post.objects.filter().order_by('-published_date')
    for post in posts:
        diff = now - post.published_date
        if diff.days == 0 and diff.seconds >= 60 and diff.seconds < 3600:
            minutes = math.floor(diff.seconds/60)
            lasPosts[post.txId] = {
                'author': f"{post.user}",
                'content': post.content,
                'published_date': post.published_date,
                'minutesAgo': minutes
            }
        else:
            continue
    return JsonResponse(lasPosts)



def checkWord(request):
    word = request.GET.get('q', '')
    posts = Post.objects.filter().order_by('-published_date')
    cont = 0
    w = word.replace('<','')
    w = w.replace('>', '')
    for post in posts:
        if w in post.content:
            cont += 1
    return HttpResponse(f'La parola {w} è apparsa {cont} volte nei post')
