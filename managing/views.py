from django.shortcuts import render
from django.http import HttpResponseRedirect, JsonResponse
from django.contrib.auth.models import User
from user.models import Post


def managing(request):
    userList = User.objects.filter(is_superuser=False)
    elePost = {}
    for user in userList:
        cont = 0
        try:
            posts = Post.objects.filter(user=user).values()
            for post in posts:
                cont += 1
        except:
            continue
        elePost[user.username] = cont
    
    return render(request, 'managing/managing.html', {'elePost': elePost})

