from django import forms
from phonenumber_field.formfields import PhoneNumberField
from django.forms.formsets import BaseFormSet


class ContactForm(forms.Form):
    first_name = forms.CharField(max_length=50, required=True)
    last_name = forms.CharField(max_length=50, required=True)


class PhoneForm(forms.Form):
    """
    Form for individual contact phone
    """
    phone = PhoneNumberField()


class BasePhoneFormSet(BaseFormSet):
    def clean(self):
        if any(self.errors):
            return

        phones = []
        duplicates = False

        for form in self.forms:
            if form.cleaned_data:
                phone = form.cleaned_data['phone']

                # Check that contact has no duplicate numbers
                if phone:
                    if phone in phones:
                        duplicates = True
                    phones.append(phone)

                if duplicates:
                    raise forms.ValidationError(
                        'Phone numbers duplicates are not allowed',
                        code='duplicate_phones'
                    )
