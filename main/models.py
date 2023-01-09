from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


class Contact(models.Model):
    first_name = models.CharField(max_length=50, null=False)
    last_name = models.CharField(max_length=50, null=False)

    def __str__(self):
        return self.first_name + " " + self.last_name


class PhoneNumber(models.Model):
    contact = models.ForeignKey(Contact, on_delete=models.CASCADE)
    number = PhoneNumberField(null=False, blank=False, unique=True)

    def __str__(self):
        return str(self.number)

