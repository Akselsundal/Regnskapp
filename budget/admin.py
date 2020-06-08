""" Register your models here."""

from django.contrib import admin
from .models import Budget, BudgetPost

admin.site.register(Budget)
admin.site.register(BudgetPost)

