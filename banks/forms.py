from django import forms
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
        self.fields['name'].label = 'name'
        self.fields['transit_num'].label = 'inst_num'
        self.fields['address'].label = 'address'
        self.fields['email'].label = 'email'
        self.fields['capacity'].label = 'capacity'
