from django.http import HttpResponseForbidden, HttpResponseRedirect, Http404, HttpResponseNotFound, HttpResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy, reverse, resolve
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, DetailView, UpdateView, FormView
from .forms import AddBankForm, AddBranchForm, EditBranchForm
from .models import Bank, Branch
from django.http import JsonResponse
from django.views import View


# checked!!!
class BankDetailsView(DetailView):
    model = Bank
    template_name = 'banks/detail.html'
    context_object_name = 'bank'

    def get_object(self):
        bank_id = self.kwargs['bank_id']
        return get_object_or_404(Bank, id=bank_id)


# Not Working now! fuck!
@method_decorator(csrf_exempt, name='dispatch')
class BranchDetailsView(DetailView):
    def get(self, request, branch_id, *args, **kwargs):
        try:
            branch = Branch.objects.get(id=kwargs['branch_id'], bank__id=kwargs['bank_id'])
        except Branch.DoesNotExist:
            raise Http404("Branch does not exist")
        data = {
            "id": branch.id,
            "name": branch.name,
            "transit_num": branch.transit_num,
            "address": branch.address,
            "email": branch.email,
            "capacity": branch.capacity,
            "last_modified": branch.last_modified.isoformat(),
        }
        return JsonResponse(data)


# checked!!!
class AddBankView(LoginRequiredMixin, FormView):
    template_name = 'banks/create.html'
    form_class = AddBankForm
    success_url = reverse_lazy('banks:bank_detail')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.object = None
        self.add_branch_view = None  # add this attribute


    def form_valid(self, form):
        bank = form.save(commit=False)
        bank.owner = self.request.user
        bank.save()
        self.object = bank  # set the object attribute
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('banks:bank_detail', kwargs={'bank_id': self.object.id})  # use the object attribute

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if 'bank_id' in self.kwargs:
            context['bank_id'] = self.kwargs['bank_id']
        elif self.request.POST.get('bank_id'):
            context['bank_id'] = self.request.POST.get('bank_id')
        else:
            context['bank_id'] = None
        return context

    def get_object(self):
        return self.object


# checked!!!
class AddBranchView(LoginRequiredMixin, FormView):
    template_name = 'banks/branch_create.html'
    form_class = AddBranchForm

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.branch = None
        self.add_bank_view = None

    def get_success_url(self):
        add_bank_view = resolve(self.request.resolver_match.url_name).func.view_class
        add_bank_view_object = add_bank_view.get_object(self.request.resolver_match.kwargs.get('pk'))
        return reverse_lazy('banks:branch_detail', kwargs={'branch_id': add_bank_view_object.id})

    def dispatch(self, request, *args, **kwargs):
        bank = get_object_or_404(Bank, id=self.kwargs.get('bank_id'))

        # Check if the current user owns this bank
        if bank.owner != request.user:
            return HttpResponseForbidden()

        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        bank = get_object_or_404(Bank, id=self.kwargs.get('bank_id'))

        # Create a new branch
        self.branch = form.save(commit=False)
        self.branch.bank = bank
        self.branch.save()

        return super().form_valid(form)


# checked!!!
class BankListView(ListView):
    template_name = 'banks/list.html'
    queryset = Bank.objects.all()
    context_object_name = 'bank_list'


class BankBranchesView(View):
    def get(self, request, bank_id, *args, **kwargs):
        bank = get_object_or_404(Bank, pk=bank_id)

        # Check if the current user owns this bank
        if bank.owner != request.user:
            return HttpResponseForbidden()

        branches = Branch.objects.filter(bank=bank)
        data = []
        for branch in branches:
            data.append({
                'id': branch.pk,
                'name': branch.name,
                'transit_num': branch.transit_num,
                'address': branch.address,
                'email': branch.email,
                'capacity': branch.capacity,
            })
        return JsonResponse(data, safe=False)


class EditBranchView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Branch
    form_class = EditBranchForm
    template_name = 'banks/edit_branch.html'
    context_object_name = 'branch'

    def test_func(self):
        """
        Check if the current user owns this branch.
        """
        branch = self.get_object()
        return branch.bank.owner == self.request.user

    def get_success_url(self):
        branch = Branch.objects.get(id=self.kwargs['branch_id'], bank__id=self.kwargs['bank_id'])
        return reverse_lazy('banks:branch_detail', kwargs={'branch_id': branch.id})

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponse(status=401)

        return super().dispatch(request, *args, **kwargs)

    def get_object(self, queryset=None):
        branch_id = self.kwargs.get('branch_id')
        branch = get_object_or_404(Branch, id=branch_id)

        # Check if the current user owns this branch's bank
        if branch.bank.owner != self.request.user:
            raise HttpResponseForbidden()

        return branch

