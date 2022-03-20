from django.shortcuts import render, redirect


# Create your views here.
def home(request):
    return render(request, 'mad_libs/home.html', {'nbar': 'home'})

