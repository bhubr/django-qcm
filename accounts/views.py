from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password

# Create your views here.
def register(request):
    if request.method == 'POST':
        User.objects.create(
            username=request.POST['username'],
            email=request.POST['email'],
            password=make_password(request.POST['password']),
        )
        return redirect('/libraries/' + request.POST['username'] + '/')

    return render(request, 'registration/register.html')