from django import template
from django.db.models import Sum
from transactions.models import Category, Account
from budget.models import BudgetPost
register = template.Library()

@register.filter(name='get_account_sum')
def get_account_sum(transaction_set, account):
    """Returnerer sum av transaksjoner for ein gitt konto"""
    return transaction_set.filter(account=account
                                 ).aggregate(Sum('amount')
                                 ).get('amount__sum')


@register.filter(name='total')
def totalt(category_dict, c_type):
    """Finne totalt utgift"""
    total = 0
    for key, value in category_dict.items():
        if key.category_type == c_type:
            continue
        total += value
    return total

@register.filter(name='get_budgeted_sum')
def get_budgeted_sum(budgetpost_set, category=None):
    """ Returnerer sum av budgetert verdi for kategori """
    if category:
        return budgetpost_set.filter(account__category__name=category
                                    ).aggregate(Sum('amount')).get('amount__sum')
    
    tot = 0
    for category in Category.objects.all():
        c_name = category.name
        tot += budgetpost_set.filter(account__category__name=c_name
                                ).aggregate(Sum('amount')).get('amount__sum') or 0
    return tot
