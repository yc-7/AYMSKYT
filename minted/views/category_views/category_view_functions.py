from minted.models import Category

def category_already_exists_for_create(category_form, user):
    """Returns whether a user already has a category with the name provided in form"""
    user_categories = Category.objects.filter(user = user)
    new_category_name = category_form.cleaned_data.get('name')
    category_with_same_name_exists = user_categories.filter(name=new_category_name).count() > 0
    if category_with_same_name_exists:
        return True
    return False

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