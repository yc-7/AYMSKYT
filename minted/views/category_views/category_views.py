from django.shortcuts import redirect, render
from minted.decorators import staff_prohibited
from minted.forms import *
from minted.models import *
from minted.views.general_user_views.login_view_functions import *
from django.contrib import messages
from django.shortcuts import redirect, render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from minted.decorators import staff_prohibited
from minted.models import Category, SpendingLimit
from minted.forms import CategoryForm, SpendingLimitForm
from minted.mixins import AdminProhibitedMixin
from minted.views.category_views.category_view_functions import *
from django.core.paginator import Paginator


class CategoryListView(LoginRequiredMixin, AdminProhibitedMixin, ListView):
    """View that displays a user's categories"""

    model = Category
    template_name = 'categories/category_list.html'
    context_object_name = 'categories'
    paginate_by = settings.CATEGORIES_PER_PAGE


    def get_queryset(self):
        current_user = self.request.user
        user_category_list = current_user.get_categories()
        return user_category_list

    def get_context_data(self, *args, **kwargs):
        """Generate content to be displayed in the template"""

        context = super().get_context_data(*args, **kwargs)
        current_user = self.request.user
        context['user'] = current_user
        paginator = Paginator(self.object_list, self.paginate_by)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context['page_obj'] = page_obj
        return context

@staff_prohibited
def create_category(request):
    category_form = CategoryForm(user=request.user)
    spending_form = SpendingLimitForm()

    if request.method == 'POST':
        category_form = CategoryForm(request.POST, user=request.user)
        spending_form = SpendingLimitForm(request.POST)

        valid_forms = category_form.is_valid() and spending_form.is_valid()
        if valid_forms:
            create_category_from_forms(request.user, category_form, spending_form, request.POST.get('colour_value', ""))

            return redirect('category_list')           
    return render(request, 'categories/create_category.html', {'category_form': category_form, 'spending_form': spending_form})

@staff_prohibited
def delete_category(request, category_id):
    if request.method == 'POST':
        if Category.objects.filter(id=category_id).count() == 0:
            messages.add_message(request, messages.ERROR, "Category does not exist")
            return redirect('create_category')
        category = Category.objects.get(id=category_id)
        category.budget.delete()
        messages.add_message(request, messages.SUCCESS, "Category deleted successfully")
    return redirect('category_list')

@staff_prohibited
def edit_category(request, category_id):
    
    category_exists = len(Category.objects.filter(id=category_id)) != 0
    
    if not category_exists:
        messages.add_message(request, messages.ERROR, "Category does not exist")
        return redirect('create_category')

    category = Category.objects.get(id=category_id)
    spending_limit = SpendingLimit.objects.get(category=category)

    if request.user != category.user and not request.user.is_superuser:
        return redirect('category_list')

    category_form = CategoryForm(instance=category)
    spending_form = SpendingLimitForm(instance=spending_limit)
    category_colour = ""
    category = Category.objects.get(pk=category_id)
    if category.colour:
        category_colour = category.colour

    if request.method == 'POST':
        category_form = CategoryForm(instance=category, data=request.POST)
        spending_form = SpendingLimitForm(request.POST)
        valid_forms = category_form.is_valid() and spending_form.is_valid()
        if valid_forms:
            if category_already_exists_for_edit(category_form, category, request.user):
                category_form.add_error('name', 'You already have a category with this name')
                return render(request, 'categories/edit_category.html', {'category_form': category_form, 'spending_form': spending_form, 'category_id': category.id})
            
            messages.add_message(request, messages.SUCCESS, "Category updated!")
            edit_category_from_forms(category_form, spending_form, spending_limit, request.POST.get('colour_value', ""))
            return redirect('category_list')
    
    context = {'category_form': category_form, 'spending_form': spending_form, 'category_id': category.id, 'category_colour': category_colour}
    return render(request, 'categories/edit_category.html', context)
