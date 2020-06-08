"""Views
from django.shortcuts import render
from django.views.generic.edit import CreateView
from django.forms import inlineformset_factory
from django.http import HttpResponse
from budget.models import Account
from .models import Budget, BudgetPost
from .forms import BudgetPostForm



NUMBER_OF_ACCOUNTS = Account.objects.count()

class BudgetCreateView(CreateView):
    "Lagar eit tomt budsjett""
    model = Budget
    fields = ['name', 'start_date', 'end_date']


def create_budgetpost(request, pk):
    "Fyller inn budsjettpostane""
    budget = Budget.objects.get(pk=pk)
    accounts = Account.objects.all()
    BudgetPostInlineFormSet = inlineformset_factory(Budget,
                                                    BudgetPost,
                                                    form=BudgetPostForm,
                                                    fields='__all__',
                                                    extra=NUMBER_OF_ACCOUNTS)
    if request.method == 'POST':
        formset = BudgetPostInlineFormSet(request.POST,
                                          instance=budget,
                                          initial=[{'account' : a.id} for a in accounts])
        if formset.is_valid():
            formset.save()
            return HttpResponse("la inn objects")
    else:
        formset = BudgetPostInlineFormSet(instance=budget,
                                          initial=[{'account' : a.id} for a in accounts])
    return render(request, 'budget/budgetpost_form.html', {'formset': formset})

"""