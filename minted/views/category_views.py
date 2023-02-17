from django.shortcuts import redirect, render, get_object_or_404
from ..forms import *
from ..models import *
from .views_functions.login_view_functions import *
from django.contrib import messages
from django.views.generic.edit import UpdateView
from .mixins import *
from django.conf import settings
from django.urls import reverse

def create_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            category = form.save(commit=False)
            category.user = request.user
            category.save()
            return redirect('dashboard')           
    else:
        form = CategoryForm(initial={'user': request.user})
    return render(request, 'create_category.html', {'form': form})


def delete_category(request, category_id):
    if request.method == 'POST':
        if not(Category.objects.filter(id=category_id).exists):
            messages.add_message(request, messages.ERROR, "Category does not exist")
            return redirect('create_category') 
        Category.objects.get(id=category_id).delete()
        messages.add_message(request, messages.SUCCESS, "Category deleted successfully")
    return redirect('category_list')


def category_list_view(request):
    current_user = request.user
    my_categories = Category.objects.filter(user = current_user)
    context = {'user': current_user,'category': my_categories}
    return render(request, 'category_list.html', context)

# LoginProhibitedMixin,
# class edit_category(UpdateView):
#     #model = Category
#     model = CategoryForm
#     template_name = "edit_category.html"
#     form_class = CategoryForm
#     #pk_url_kwarg = 'category_id'
    

#     def get_object(self):
        
#         category_id = self.kwargs.get("category_id")
#         return get_object_or_404(Category, id=category_id)
        
#     #fields = ['user', 'name', 'budget']
#     #template_name_suffix = 

#     def get_success_url(self):
#         """Return redirect URL after successful update."""
#         messages.add_message(self.request, messages.SUCCESS, "Category updated!")
#         return reverse('category_list')

#     def form_valid(self, form):
#         print(form.cleaned_data)
#         return super().form_valid(form)

def edit_category(request, category_id):
# Redirect if the requested user_id is not a valid user.
    if not category_id:
        return redirect('category_list')

    # Check if there exists a user with user_id
    if not Category.objects.filter(id=category_id).exists:
        return redirect('create_category')

    category = Category.objects.get(id=category_id)

    # Redirect if the current user is attempting to change the profile of another user.
    # if not request.user.is_superuser and request.user != user:
    #     return redirect_with_queries('/profile/', user_id=request.user.id)

    # redirect if the current user is attempting to change a category of another user
    if request.user != category.user and not request.user.is_superuser:
        return redirect('category_list')

    if request.method == 'POST':
        form = CategoryForm(instance=category, data=request.POST)
        if form.is_valid():
            messages.add_message(request, messages.SUCCESS, "Category updated!")
            form.save()
            print("here1")
            return redirect('dashboard')
    else:
        form = CategoryForm(instance=category)
    return render(request, 'edit_category.html', {'form': form, 'category_id': category.id})