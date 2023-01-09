from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import ListView, DetailView
from .models import Contact, PhoneNumber
from django.forms.formsets import formset_factory
from django.shortcuts import  render
from .forms import PhoneForm, BasePhoneFormSet, ContactForm


class ContactListView(ListView):
    template_name = "main/contacts.html"
    model = Contact
    context_object_name = 'contacts'


class ContactDetailView(DetailView):
    template_name = "main/contact_details.html"
    queryset = Contact.objects.all()
    context_object_name = 'contact'


def create(request):

    # Create the formset, specifying the form and formset we want to use.
    PhoneFormSet = formset_factory(PhoneForm, formset=BasePhoneFormSet)

    if request.method == 'POST':
        contact_form = ContactForm(request.POST)
        phone_formset = PhoneFormSet(request.POST)

        if contact_form.is_valid() and phone_formset.is_valid():
            # Save contact info
            first_name = contact_form.cleaned_data['first_name']
            last_name = contact_form.cleaned_data['last_name']
            new_contact = Contact(first_name=first_name, last_name=last_name)
            new_contact.save()

            # Now save the data for each form in the formset
            new_phones = []

            for phone_form in phone_formset:
                phone = phone_form.cleaned_data.get('phone')

                if phone:
                    new_phones.append(PhoneNumber(contact=new_contact, number=phone))

            PhoneNumber.objects.bulk_create(new_phones)
            return redirect('contacts')

    else:
        contact_form = ContactForm()
        phone_formset = PhoneFormSet()

    context = {
        'contact_form': contact_form,
        'phone_formset': phone_formset,
    }

    return render(request, 'main/create.html', context)
