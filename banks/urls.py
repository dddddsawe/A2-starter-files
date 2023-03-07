from django.urls import path
from . import views

app_name = 'banks'

urlpatterns = [
    path('all/', views.BankListView.as_view(), name='bank_list'),  # checked
    path('add/', views.AddBankView.as_view(), name='add_bank'),  # checked
    path('<int:bank_id>/details/', views.BankDetailsView.as_view(), name='bank_detail'),  # checked
    path('<int:bank_id>/branches/add/', views.AddBranchView.as_view(), name='add_branch'),  # checked
    path('branch/<int:branch_id>/details/', views.BranchDetailsView.as_view(), name='branch_detail'),  # checked
    path('branch/<int:branch_id>/edit/', views.EditBranchView.as_view(), name='edit_branch'),  # checked
]
