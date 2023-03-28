

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