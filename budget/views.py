"""Views"""
from django.shortcuts import render
from django.views.generic import CreateView, ListView, DetailView
from django.forms import inlineformset_factory
from django.http import HttpResponse
from transactions.models import Account, Transaction
from .models import Budget, BudgetPost
from .forms import BudgetPostForm
from transactions.scripts.tools import sum_cat, sum_account



NUMBER_OF_ACCOUNTS = Account.objects.count()

class BudgetCreateView(CreateView):
    """Lagar eit tomt budsjett"""
    model = Budget
    fields = ['name', 'start_date', 'end_date']


def create_budgetpost(request, **kwargs):
    """Fyller inn budsjettpostane"""
    budget = Budget.objects.get(pk=kwargs['pk'])
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


class BudgetListView(ListView):
    model = Budget

class BudgetDetailView(DetailView):
    model = Budget
    def get_context_data(self, *args, **kwargs):
        t = Transaction.objects.filter(date__range=(self.object.start_date, self.object.end_date))
        budgetpost_set = BudgetPost.objects.filter(budget=self.object)
        cat_dict = sum_account(t)
        data = super().get_context_data(**kwargs)
        data['transaction_set'] = t
        data['cat_dict'] = cat_dict
        data['budgetpost_set'] = budgetpost_set
        return data
