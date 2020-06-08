"""Hjelpefunksjoner"""
from django.db.models import Sum
from transactions.models import Category

def sum_account(transaction_set):
    """
    Summerer opp transaksjoner for gitt kategori og
    gitte datoer. Returnerer ein dict med format
    {kategorinamn : sum}
    """
    sum_dict = {}
    for cat in Category.objects.all():
        sum_dict[cat.name] = round(transaction_set.filter(
            category=cat
            ).aggregate(Sum("amount")
            ).get("amount__sum") or 0, 2)

    return sum_dict
