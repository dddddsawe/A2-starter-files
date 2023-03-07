from django import forms
from django.http import Http404
from django.shortcuts import render

from .models import Bank, Branch


# checked!!!
class AddBranchForm(forms.ModelForm):
    class Meta:
        model = Branch
        fields = ['name', 'transit_num', 'address', 'email', 'capacity']

    email = forms.EmailField(required=True, initial='admin@utoronto.ca')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not email.endswith('@utoronto.ca'):
            raise forms.ValidationError('The email address must end with @utoronto.ca')
        return email


# checked
class AddBankForm(forms.ModelForm):
    class Meta:
        model = Bank
        fields = ['name', 'description', 'inst_num', 'swift_code']
        labels = {
            'name': 'Bank Name',
            'description': 'Description',
            'inst_num': 'Institution Number',
            'swift_code': 'Swift Code',
        }
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        for field in ['name', 'description', 'inst_num', 'swift_code']:
            if not cleaned_data.get(field):
                self.add_error(field, 'This field is required')
        return cleaned_data

    def save(self, commit=True):
        bank = super().save(commit=False)
        bank.owner = self.user
        if commit:
            bank.save()
        return bank


# checked
class EditBranchForm(forms.ModelForm):
    class Meta:
        model = Branch
        fields = ['name', 'transit_num', 'address', 'email', 'capacity']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Customize form labels
        self.fields['name'].label = 'Name'
        self.fields['transit_num'].label = 'Transit Number'
        self.fields['address'].label = 'Address'
        self.fields['email'].label = 'Email'
        self.fields['capacity'].label = 'Capacity'


class BranchCreateForm(forms.ModelForm):
    class Meta:
        model = Branch
        fields = ['name', 'transit_num', 'address', 'email', 'capacity']

    def __init__(self, *args, **kwargs):
        bank_id = kwargs.pop('bank_id')
        super().__init__(*args, **kwargs)
        self.fields['bank_id'] = forms.IntegerField(widget=forms.HiddenInput(), initial=bank_id)


class CreateBranchForm(forms.ModelForm):
    template_name = 'banks/branch.html'
    form_class = BranchCreateForm
    success_url = '/banks/{bank_id}/details/'

    class Meta:
        model = Branch
        fields = ['name', 'transit_num', 'address', 'email', 'capacity']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'class': 'form-control'})
        self.fields['transit_num'].widget.attrs.update({'class': 'form-control'})
        self.fields['address'].widget.attrs.update({'class': 'form-control'})
        self.fields['email'].widget.attrs.update({'class': 'form-control'})
        self.fields['capacity'].widget.attrs.update({'class': 'form-control'})

    def clean(self):
        cleaned_data = super().clean()
        name = cleaned_data.get('name')
        transit_num = cleaned_data.get('transit_num')
        address = cleaned_data.get('address')
        email = cleaned_data.get('email')
        capacity = cleaned_data.get('capacity')
        if not name:
            self.add_error('name', 'This field is required')
        if not transit_num:
            self.add_error('transit_num', 'This field is required')
        if not address:
            self.add_error('address', 'This field is required')
        if not email:
            self.add_error('email', 'This field is required')
        if not capacity:
            self.add_error('capacity', 'This field is required')
        elif capacity < 0:
            self.add_error('capacity', 'Capacity cannot be negative')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['bank_id'] = self.kwargs.get('bank_id')
        return kwargs

    def form_valid(self, form):
        branch = form.save(commit=False)
        branch.bank_id = self.kwargs.get('bank_id')
        branch.save()
        return super().form_valid(form)


class BankInfoForm(forms.ModelForm):
    class Meta:
        model = Bank
        fields = ['name', 'inst_num', 'swift_code', 'description']
        # 设置每个字段的widget为readonly，以便在template中只展示而不能修改
        widgets = {
            'name': forms.TextInput(attrs={'readonly': True}),
            'inst_num': forms.TextInput(attrs={'readonly': True}),
            'swift_code': forms.TextInput(attrs={'readonly': True}),
            'description': forms.Textarea(attrs={'readonly': True}),
        }


def bank_info(request, bank_id):
    try:
        bank = Bank.objects.get(pk=bank_id)
    except Bank.DoesNotExist:
        raise Http404

    form = BankInfoForm(instance=bank)

    return render(request, 'banks/detail.html', {'form': form})
