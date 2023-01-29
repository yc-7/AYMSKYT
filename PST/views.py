from django.shortcuts import render
from PST.forms import SpendingLimitForm
from PST.models import SpendingLimit, Category
# Create your views here.

def home(request):
    return render(request, 'home.html')

def test_category(request):
    categories = Category.objects.all()
    return render(request, 'test_category.html', {'categories': categories})

def test_spending(request, category_id):
    try:
        category = Category.objects.get(id=category_id)
    except ObjectDoesNotExist:
        return redirect('category')
    else:
        if request.method == 'POST':
            form = SpendingLimitForm(request.POST)
            if form.is_valid():
                category.budget = form.save()
                category.save()
        else:
            form = SpendingLimitForm()
    return render(request, 'test_spending.html', {'form': form, 'category_id': category_id})