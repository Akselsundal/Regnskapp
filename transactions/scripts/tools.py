"""Hjelpefunksjoner"""
from django.db.models import Sum
from transactions.models import Category, Account


def totalt(transaction_set, model='__all__'):
    sum_dict = {}
    for entry in model:
        sum_dict[entry] = round(
            transaction_set.filter(
                account=entry
                ).filter(category=model)
        )

def sum_account(transaction_set):
    """
    Summerer opp transaksjoner for gitte datoer.
    Returnerer ein dict med format {kategorinamn : sum}
    """
    sum_dict = {}
    for cat in Category.objects.all():
        sum_dict[cat] = round(transaction_set.filter(
            category=cat
            ).aggregate(Sum("amount")
            ).get("amount__sum") or 0, 2)

    return sum_dict

def sum_cat(transaction_set, category):
    """
    Summerer opp transaksjoner for gitt konto og
    gitte datoer. Returnerer ein dict med format
    {kontonamn : sum}
    """
    account_set = Account.objects.filter(category=category)
    sum_dict = {}
    for account in account_set:
        sum_dict[account] = round(
            transaction_set.filter(account=account
            ).aggregate(Sum("amount")
            ).get("amount__sum") or 0, 2)

    return sum_dict