"""Db models"""
from django.urls import reverse
from django.db import models
from transactions.models import Account

class Budget(models.Model):
    """Objekt for å oppbevare eit budsjett"""

    name = models.CharField(max_length=30)
    start_date = models.DateField()
    end_date = models.DateField()
    timestamp = models.DateField(auto_now_add=True)
    edited = models.DateField(auto_now=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        """Sender til utfylling av budsjett"""
        return reverse('budget:budgetpost-create', kwargs={'pk' : self.pk})



class BudgetPost(models.Model):
    """Representerer ein post i budsjettet"""
    account = models.ForeignKey(Account,
                                null=True,
                                blank=False,
                                on_delete=models.CASCADE)
    budget = models.ForeignKey(Budget,
                               null=False,
                               blank=False,
                               on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10,
                                 decimal_places=2,
                                 default=0)
    comment = models.CharField(max_length=30,
                               null=True,
                               blank=True)

    def __str__(self):
        return "{} in {}: {}".format(self.account.name, self.budget.name, self.amount)
