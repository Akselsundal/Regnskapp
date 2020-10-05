"""Urls til budget"""
from django.urls import path
from .views import BudgetCreateView, create_budgetpost, BudgetListView, BudgetDetailView

app_name = 'budget'

urlpatterns = [
    path("create/", BudgetCreateView.as_view(), name="budget-create"),
    path("create/<int:pk>", create_budgetpost, name="budgetpost-create"),
    path("", BudgetListView.as_view(), name="budget-list"),
    path("<pk>/",BudgetDetailView.as_view(), name="budget-detail")
]
