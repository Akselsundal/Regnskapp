"""forms"""
from django import forms
from .models import Transaction, Account

class TransactionForm(forms.ModelForm):
    """Til å endre eller bokføre transaksjon"""
    account = forms.ModelChoiceField(
        queryset=Account.objects.all(),
        widget=forms.Select(attrs={'class' : 'form-control form-group col-md-2'}))
    amount = forms.DecimalField(
            max_digits=10,
            decimal_places=2,
            disabled=True
        )
    class Meta:
        model = Transaction    
        fields = (
            'transaction_type',
            'description',
            'amount',
            'account',
            'project'
        )  

        widgets = {
            'transaction_type' : forms.TextInput(
                attrs={'class' : 'form-control col-md-4', 'rows' : '4'}),
            'description' : forms.TextInput(attrs={
                'class' : 'form-control col-md-7', 'rows' : '4'}),
            'project' : forms.Select(attrs={'class' : 'form-control form-group col-md-2'}),
            'happy' : forms.Select(attrs={'class' : 'form-control form-group col-md-2'}),
        }
    

class CreateTransactionForm(forms.ModelForm):
    
    class Meta:
        model = Transaction
        fields = (
            'date',
            'transaction_type',
            'description',
            'amount',
            'project',
            'account'
        )
