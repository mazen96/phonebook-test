from django.urls import path
from .views import ContactListView, ContactDetailView, create

urlpatterns = [
    path('', ContactListView.as_view(), name="contacts"),
    path('create/', create),
    path('<pk>/', ContactDetailView.as_view()),
]