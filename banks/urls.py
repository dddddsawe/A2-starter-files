from django.urls import path

from banks.views import (
    BankListView,
    BankDetailView,
    BankCreateView,
    BranchCreateView,
    BranchUpdateView,
    BankBranchListView,
    BranchDetailsView,
    BankAllView,
    BankAddView,
)

app_name = 'banks'

urlpatterns = [
    path('banks/', BankListView.as_view(), name='bank_list'),
    path('banks/<int:pk>/', BankDetailView.as_view(), name='bank_detail'),
    path('banks/create/', BankCreateView.as_view(), name='bank_create'),
    path('banks/add/', BankAddView.as_view(), name='bank_add'),
    path('banks/<int:bank_id>/branches/create/', BranchCreateView.as_view(), name='branch_create'),
    path('branches/<int:pk>/update/', BranchUpdateView.as_view(), name='branch_update'),
    path('banks/<int:bank_id>/branches/', BankBranchListView.as_view(), name='bank_branch_list'),
    path('branches/<int:branch_id>/', BranchDetailsView.as_view(), name='branch_detail'),
    path('all/json/', BankAllView.as_view(), name='bank_all'),
    path('banks/add/', BankCreateView.as_view(), name='bank_create'),
]
