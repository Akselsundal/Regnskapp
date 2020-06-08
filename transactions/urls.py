"""Urls til transactions"""
from django.urls import path
from . import views
from .views import (TransactionDetailView,
                    TransactionUpdate,
                    TransactionView,
                    AccountCreateView,
                    ProjectCreateView
                    )

app_name = 'transactions'

urlpatterns = [
    path("", TransactionView.as_view(), name="transactions_list"),
    path("<start_date>/<end_date>/", TransactionView.as_view(), name="transactions_result"),
    path("<int:pk>/", TransactionDetailView.as_view(), name="transaction-detail"),
    path("<int:pk>/edit", TransactionUpdate.as_view(), name="transaction-update"),
    path("account/create", AccountCreateView.as_view(), name="account-create"),
    path("account/create/redirect/<int:pk>", AccountCreateView.as_view(), name="account-create-redirect"),
    path("project/create", ProjectCreateView.as_view(), name="project-create"),
    path("project/create/redirect/<int:pk>/", ProjectCreateView.as_view(), name="project-create-redirect"),
    path("import/", views.data_import, name="data_import")
]
