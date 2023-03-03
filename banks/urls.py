from django.urls import path

from banks.views import (
    BankListView,
    BankDetailView,
    BranchCreateView,
    BranchUpdateView,
    bank_branch_details,
    bank_branch_list,
    bank_all,
)

urlpatterns = [
    path('all/', BankListView.as_view(), name='bank_list'),
    path('int:pk/details/', BankDetailView.as_view(), name='bank_detail'),
    path('add/', BankCreateView.as_view(), name='bank_add'),
    path('int:bank_id/branches/add/', BranchCreateView.as_view(), name='bank_branch_add'),
    path('branch/int:pk/edit/', BranchUpdateView.as_view(), name='bank_branch_edit'),
    path('int:bank_id/branches/all/', bank_branch_list, name='bank_branch_list'),
    path('branch/int:pk/details/', bank_branch_details, name='bank_branch_detail'),
    path('all/json/', bank_all, name='bank_all'),
]