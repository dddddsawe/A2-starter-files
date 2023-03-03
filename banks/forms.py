from django import forms
from django.core.exceptions import ValidationError
from banks.models import Bank, Branch


class BankForm(forms.ModelForm):
    class Meta:
        model = Bank
        fields = ['name', 'description', 'inst_num', 'swift_code']

    def clean(self):
        cleaned_data = super().clean()
        for field in ['name', 'description', 'inst_num', 'swift_code']:
            if not cleaned_data.get(field):
                self.add_error(field, 'This field is required')


class BranchForm(forms.ModelForm):
    class Meta:
        model = Branch
        fields = ['name', 'transit_num', 'address', 'email', 'capacity']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not email:
            raise ValidationError('This field is required')
        return email

    def clean(self):
        cleaned_data = super().clean()
        for field in ['name', 'transit_num', 'address']:
            if not cleaned_data.get(field):
                self.add_error(field, 'This field is required')