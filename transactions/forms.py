"""forms"""
from django import forms
from .models import Transaction, Account

class TransactionForm(forms.ModelForm):
    """Til å endre eller bokføre transaksjon"""
    description = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={
            'class' : 'form-control col-md-7', 'rows' : '4'})
        )
    account = forms.ModelChoiceField(
        queryset=Account.objects.all(),
        widget=forms.Select(attrs={'class' : 'form-control form-group col-md-2'}))

    class Meta:
        model = Transaction
        fields = (
            'transaction_type',
            'description',
            'project',
            'happy'
        )
