from django.views.generic.edit import FormView, UpdateView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse, Http404, HttpResponseBadRequest
from django.shortcuts import get_object_or_404, render
from banks.models import Bank, Branch
from banks.forms import BankForm, BranchForm
import json
from django.core import serializers
from django.core.exceptions import PermissionDenied


class BankListView(ListView):
    model = Bank
    template_name = 'banks/bank_list.html'
    context_object_name = 'bank_list'

class BankDetailView(DetailView):
    model = Bank
    template_name = 'banks/bank_detail.html'
    context_object_name = 'bank'

class BranchUpdateView(LoginRequiredMixin, UpdateView):
    model = Branch
    form_class = BranchForm
    template_name = 'banks/edit_branch.html'

    def dispatch(self, request, *args, **kwargs):
        if self.get_object().bank.owner != self.request.user:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('bank_branch_detail', args=(self.object.pk,))

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['initial'] = {
            'name': self.object.name,
            'transit_num': self.object.transit_num,
            'address': self.object.address,
            'email': self.object.email,
            'capacity': self.object.capacity,
        }
        return kwargs


class BankCreateView(LoginRequiredMixin, FormView):
    template_name = 'banks/add_bank.html'
    form_class = BankForm
    success_url = reverse_lazy('bank_detail')

    def form_valid(self, form):
        bank = form.save(commit=False)
        bank.owner = self.request.user
        bank.save()
        return super().form_valid(form)

class BranchCreateView(LoginRequiredMixin, FormView):
    template_name = 'banks/add_branch.html'
    form_class = BranchForm

    def dispatch(self, request, *args, **kwargs):
        bank_id = kwargs.get('bank_id')
        self.bank = get_object_or_404(Bank, pk=bank_id)
        if self.bank.owner != self.request.user:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        branch = form.save(commit=False)
        branch.bank = self.bank
        branch.save()
        return super().form_valid(form)

class BranchDetailsView(View):
    def get(self, request, *args, **kwargs):
        try:
            branch = Branch.objects.get(pk=kwargs['branch_id'], bank__pk=kwargs['bank_id'])
        except Branch.DoesNotExist:
            raise Http404('Branch does not exist')

        data = {
            'id': branch.pk,
            'name': branch.name,
            'transit_num': branch.transit_num,
            'address': branch.address,
            'email': branch.email,
            'capacity': branch.capacity,
            'last_modified': branch.last_modified.isoformat()
        }
        return JsonResponse(data)

class BankBranchListView(View):
    def get(self, request, *args, **kwargs):
        try:
            bank = Bank.objects.get(pk=kwargs['bank_id'])
        except Bank.DoesNotExist:
            raise Http404('Bank does not exist')
        branches = bank.branches.all()
        data = [{
            'id': branch.pk,
            'name': branch.name,
            'transit_num': branch.transit_num,
            'address': branch.address,
            'email': branch.email,
            'capacity': branch.capacity,
            'last_modified': branch.last_modified.isoformat()
        } for branch in branches]
        return JsonResponse(data, safe=False)
