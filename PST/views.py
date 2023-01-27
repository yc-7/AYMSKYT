from django.shortcuts import render
# Create your views here.

def home(request):
    return render(request, 'homepage.html')

def view_expenditures(request):
    pass