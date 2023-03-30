from minted.models import Category

def category_already_exists_for_edit(category_form, category, user):
    """Returns whether a user already has a category with the name provided in form"""
    user_categories = Category.objects.filter(user = user)
    new_category_name = category_form.cleaned_data.get('name')
    categories_with_new_category_name = user_categories.filter(name=new_category_name)

    # Filter out existing category
    categories_with_new_category_name = [new_category for new_category in categories_with_new_category_name if new_category!=category]
    category_that_already_exists = categories_with_new_category_name[0] if len(categories_with_new_category_name) > 0 else None

    if category_that_already_exists and category_that_already_exists.name == category.name:
        return True
    return False


def create_category_from_forms(user, category_form, spending_form, colour):
    spending = spending_form.save()
    category = category_form.save(commit=False)
    category.user = user
    category.budget = spending
    category.colour = colour
    category.save()
    return category

def edit_category_from_forms(category_form, spending_form, old_spending_limit, colour):
    new_spending = spending_form.save()
    category = category_form.save(commit=False)
    category.budget = new_spending
    colour_value = colour
    category.colour = colour_value
    category.save()
    old_spending_limit.delete()
