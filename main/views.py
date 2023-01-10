from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView
from .models import Contact, PhoneNumber
from django.forms.formsets import formset_factory
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
    context = dict()

    if request.method == 'POST':
        contact_form = ContactForm(request.POST)
        phone_formset = PhoneFormSet(request.POST)

        context = {
            'contact_form': contact_form,
            'phone_formset': phone_formset,
        }

        if contact_form.is_valid() and phone_formset.is_valid():
            first_name = contact_form.cleaned_data['first_name']
            last_name = contact_form.cleaned_data['last_name']
            new_contact = Contact(first_name=first_name, last_name=last_name)

            # check for no phones or phone duplicates
            new_phones = []

            for phone_form in phone_formset:
                phone = phone_form.cleaned_data.get('phone')

                if phone:
                    new_phones.append(phone)

            duplicate_numbers = PhoneNumber.objects.filter(number__in=new_phones)
            if not new_phones:
                # No phone numbers provided
                context['messages'] = ["You cannot create a contact without adding at least one phone number."]
            elif duplicate_numbers.count() > 0:
                # There exist duplicate phone numbers
                context['messages'] = [
                    "These numbers { " + " & ".join(str(phone) for phone in duplicate_numbers) + " } are already registered."
                ]
                return render(request, 'main/create.html', context)
            else:
                # valid ... save models to database
                new_contact.save()
                PhoneNumber.objects.bulk_create([PhoneNumber(contact=new_contact, number=phone) for phone in new_phones])
                return redirect('contacts')

    else:
        contact_form = ContactForm()
        phone_formset = PhoneFormSet()

    context['contact_form'] = contact_form
    context['phone_formset'] = phone_formset

    return render(request, 'main/create.html', context)
