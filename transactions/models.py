
"""
Inneholder modeller for transaksjoner og
tilhøyrande konto og kategori
"""

from django.db import models
from django.urls import reverse
ACCOUNT_CHOICES = [
    ("expence", "expence"),
    ("deposit", "deposit")
]


class Project(models.Model):
    """
    Prosjekt: Dette er i prinsippet bare
    ein konto med tidsavgrensing
    """
    name = models.CharField(max_length=20)
    description = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        """Sender til detaljer"""
        return reverse('transactions:project-detail', kwargs={'pk': self.pk})



class Category(models.Model):
    "Kategori"""
    name = models.CharField(max_length=20)
    description = models.CharField(max_length=100)
    category_type = models.CharField(
        max_length=8,
        choices=ACCOUNT_CHOICES,
        blank=False,
        null=True,
        default="expence")

    def __str__(self):
        return self.name


class Account(models.Model):
    """Konto"""
    name = models.CharField(max_length=30)
    description = models.CharField(max_length=100)
    category = models.ForeignKey(Category,
                                 blank=False,
                                 on_delete=models.CASCADE)

    account_type = models.CharField(
        max_length=8,
        choices=ACCOUNT_CHOICES,
        blank=False,
        null=True,
        default="expence")

    def get_absolute_url(self):
        """Sender til detaljer"""
        return reverse('transactions:transaction-detail', kwargs={'pk': self.pk})

    def __str__(self):
        return "{}".format(self.name)

HAPPY_CHOICES = [
    ('1', 1),
    ('2', 2),
    ('3', 3),

]

'''
class RawTransaction(models.Model):
    This model is automatically inserted in the database from csv file
    date = models.DateField() # Date transaction happened
    transaction_type = models.CharField(max_length=30, null=True) # Expence or Income
    description = models.CharField(max_length=200) 
    amount = models.DecimalField(max_digits=10,
                                 decimal_places=2,
                                 default=0)
'''

class Transaction(models.Model): #Klasse som representerer ein transaksjon
    """
    The posted transaction as created by the user. 
    """

    date = models.DateField() # Date transaction happened
    transaction_type = models.CharField(max_length=30, null=True) # Expence or Income
    description = models.CharField(max_length=200) 
    amount = models.DecimalField(max_digits=10,
                                 decimal_places=2,
                                 default=0)
    happy = models.PositiveSmallIntegerField(choices=HAPPY_CHOICES, blank=True, null=True)
    account = models.ForeignKey(Account,
                                blank=True,
                                null=True,
                                on_delete=models.SET_NULL
                                )
    category = models.ForeignKey(Category,
                                 blank=True,
                                 null=True,
                                 on_delete=models.SET_NULL
                                 ) # unnecesary? 
    project = models.ForeignKey(Project,
                                blank=True,
                                null=True,
                                on_delete=models.SET_NULL
                                )
    

    def is_posted(self):
        """Sjekker om transaksjonen er bokført"""
        return bool(self.account)

    def set_category(self):
        """Setter kategorien til transaksjonen lik den til kontoen"""
        if self.is_posted():
            self.category = self.account.category

    def __str__(self):
        return '{} - {}, amount={}, account={} \n'.format(self.pk,
                                                          self.date,
                                                          self.amount,
                                                          self.account
                                                          )

    def get_absolute_url(self):
        """Sender til detaljer"""
        return reverse('transactions:transaction-detail', kwargs={'pk': self.pk})

    def save(self, *args, **kwargs): # pylint: disable=signature-differs
        """Setter kategori lik den som tilhøyrer kontoen"""
        print("kwargs: ", kwargs)
        if self.account is not None:
            self.category = self.account.category
        return super(Transaction, self).save(*args, **kwargs)


