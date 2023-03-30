from django.shortcuts import redirect, render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from minted.decorators import staff_prohibited
from minted.forms import *
from minted.models import *
from minted.views.general_user_views.login_view_functions import *
from minted.views.expenditure_views.expenditure_receipt_functions import handle_uploaded_receipt_file, delete_file
from django.shortcuts import get_object_or_404
from django.http import Http404

class CategoryExpenditureListView(LoginRequiredMixin, ListView):
    """View that displays a user's expenditure in a specific category"""

    model = Expenditure
    template_name = 'expenditures/expenditure_list.html'
    context_object_name = 'expenditures'
    http_method_names = ['get']
    paginate_by = settings.EXPENDITURES_PER_PAGE

    def get(self, request, *args, **kwargs):
        """Handle get request and redirect if category_name is invalid"""

        try:
            return super().get(request, *args, **kwargs)
        except Http404:
            return redirect('category_list')

    def get_queryset(self):
        """Return the user's expenditures in a given category"""

        current_user = self.request.user
        self.category = get_object_or_404(Category, user = current_user, name = self.kwargs['category_name'])
        expenditures = Expenditure.objects.filter(category = self.category).order_by('-date')
        return expenditures

    def get_context_data(self, *args, **kwargs):
        """Generate content to be displayed in the template"""

        context = super().get_context_data(*args, **kwargs)
        context['category'] = self.category
        return context

@staff_prohibited
def delete_expenditure(request, expenditure_id):
    if request.method == 'POST':
        expenditure = Expenditure.objects.get(pk=expenditure_id)
        category = expenditure.category
        if request.user == category.user:
            if expenditure.receipt:
                delete_file(expenditure.receipt)
            expenditure.delete()
        return redirect('category_expenditures', category_name=category.name)
    return redirect('category_list')

@staff_prohibited
def edit_expenditure(request, category_name, expenditure_id):
    expenditure_exists = Expenditure.objects.filter(id=expenditure_id).count() != 0
    if not expenditure_exists:
        return redirect('category_list')
    
    expenditure = Expenditure.objects.get(id=expenditure_id)
    if request.user != expenditure.category.user:
        return redirect('category_list')

    form = ExpenditureForm(instance=expenditure)
    if request.method == 'POST':
        form = ExpenditureForm(request.POST, instance=expenditure)
        if form.is_valid():
            expenditure = form.save(commit=False)
            new_file = request.FILES.get('receipt')
            current_receipt = expenditure.receipt
            update_file = new_file and current_receipt

            if update_file:
                delete_file(current_receipt)

            if new_file:
                receipt_path = handle_uploaded_receipt_file(new_file)
                expenditure.receipt = receipt_path

            expenditure.save()

            return redirect('category_expenditures', category_name=category_name)
    return render(request, 'expenditures/edit_expenditures.html', { 'form': form, 'expenditure': expenditure })


@staff_prohibited
def add_expenditure(request, category_name):
    if Category.objects.filter(user=request.user, name=category_name).exists() == False:
        return redirect('create_category')
    if request.method == 'POST':
        category = Category.objects.get(user=request.user, name=category_name)
        form = ExpenditureForm(request.POST)
        if request.POST.get("addExpenditure"):
            if form.is_valid():
                expenditure = form.save(commit=False)
                file = request.FILES.get('receipt')
                expenditure.category = category

                if file:
                    receipt_path = handle_uploaded_receipt_file(file)
                    expenditure.receipt = receipt_path
                
                expenditure.save()

                return redirect('category_expenditures', category_name=category_name)
        elif request.POST.get("cancelAddition"):
            return redirect('category_expenditures', category_name=category_name)
    form = ExpenditureForm()
    return render(request, 'expenditures/add_expenditure.html', { 'form': form, 'category': category_name })
