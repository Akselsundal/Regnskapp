"""Skjemaer knytta til budsjett"""
from django import forms
from django.forms import ModelForm
from transactions.models import Account
from .models import BudgetPost

class BudgetPostForm(ModelForm):
    """Eit skjema for å fylle inn ein budsjettpost"""
    account = forms.ModelChoiceField(Account.objects.all(),
                                     required=True,
                                     disabled=True,
                                     #widget=forms.HiddenInput
                                     )

    class Meta():
        model = BudgetPost
        fields = ['amount', 'comment', 'budget']
