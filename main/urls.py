from django.urls import path
from .views import ContactListView, ContactDetailView, create

urlpatterns = [
    path('', ContactListView.as_view(), name="contacts"),
    path('contacts/', ContactListView.as_view(), name="contacts"),
    path('contacts/create/', create),
    path('contacts/<pk>/', ContactDetailView.as_view()),
]