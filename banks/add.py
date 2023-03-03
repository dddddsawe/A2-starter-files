from django.urls import reverse_lazy
from django.views.generic.edit import FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from banks.models import Bank
from banks.forms import BankForm


class BankAddView(LoginRequiredMixin, FormView):
    template_name = 'banks/bank_form.html'
    form_class = BankForm

    def form_valid(self, form):
        # Infer owner from current user
        form.instance.owner = self.request.user
        # Save bank and get its ID
        bank = form.save()
        bank_id = bank.id
        # Redirect to bank details
        return super().form_valid(form)

    def get_success_url(self):
        bank_id = self.object.id
        return reverse_lazy('bank-details', kwargs={'pk': bank_id})

    def dispatch(self, request, *args, **kwargs):
        # Check if user is the owner of the corresponding bank
        bank_id = self.kwargs.get('pk')
        try:
            bank = Bank.objects.get(id=bank_id, owner=request.user)
        except Bank.DoesNotExist:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)
