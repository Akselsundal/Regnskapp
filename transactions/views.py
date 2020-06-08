"""Handels views for transactions"""

from django.shortcuts import render
from django.views import View
from django.views.generic import DetailView, UpdateView, CreateView
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.core import exceptions
from .forms import TransactionForm
from .models import Transaction, Category, Account, Project
from .scripts.import_handler import importer
from .scripts.tools import sum_account

# Create your views here.

class TransactionView(View):
    "Generic view function for transactons"
    t = Transaction.objects.all()
    a = sum_account(t)
    template_name = "transactions/transaction_list.html"
    context = {
        "transaction_list" : t,
        "account_dict" : a
    }

    def get(self, request, *args, **kwargs):  # pylint: disable=unused-argument     
        """"Enkel get-funksjon som henter ut eventuelle datoer og lagar nytt queryset"""
        if kwargs:
            t = Transaction.objects.filter(date__range=(kwargs["start_date"], kwargs["end_date"]))
            self.context["transaction_list"] = t
            self.context["account_dict"] = sum_account(t)
        return render(request, self.template_name, self.context)



class TransactionDetailView(DetailView):
    """
    Viser detaljer for transaksjon og gir mulighet for
    endre, slette og bokføre
    """
    model = Transaction


class TransactionUpdate(UpdateView):
    """Oppdaterer og bokfører"""
    template_name_suffix = '_update_form'
    model = Transaction
    form_class = TransactionForm

class AccountCreateView(CreateView):
    """Oppretter ein konto"""
    model = Account
    template_name_suffix = '_create_form'
    fields = '__all__'

    def get_success_url(self):  # pylint: disable=unused-argument
        if 'pk' in self.kwargs:
            url = reverse_lazy('transactions:transaction-update', kwargs={'pk' : self.kwargs['pk']})
        else:
            try:
                url = self.object.get_absolute_url()
            except AttributeError:
                raise exceptions.ImproperlyConfigured(
                    "No URL to redirect to.  Either provide a url or define"
                    " a get_absolute_url method on the Model.")
        return url



class ProjectCreateView(CreateView):
    """Lager prosject"""
    model = Project
    template_name_suffix = '_create_form'
    fields = '__all__'

    def get_success_url(self):  # pylint: disable=unused-argument
        if 'pk' in self.kwargs:
            url = reverse_lazy('transactions:transaction-update', kwargs={'pk' : self.kwargs['pk']})

        else:
            try:
                url = self.object.get_absolute_url()
            except AttributeError:
                raise exceptions.ImproperlyConfigured(
                    "No URL to redirect to.  Either provide a url or define"
                    " a get_absolute_url method on the Model.")
        return url

class CategoryDetailView(DetailView):
    """Viser ein kategori"""
    model = Category

def data_import(request):
    """Importerer transaksjoner"""
    importer()
    #conflicting_transactions = Transaction.objects.filter(pk__in=pk_l)
    #Transaction.objects.all().delete()
    return HttpResponse("la inn objects")
