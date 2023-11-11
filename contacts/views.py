from django.views.generic import ListView, DetailView
from django.views.generic.edit import UpdateView, DeleteView, CreateView
from django.urls import reverse_lazy

from .models import Contact


class ContactListView(ListView):
    model = Contact
    template_name = "contact_list.html"


class ContactDetailView(DetailView):
    model = Contact
    template_name = "contact_detail.html"


class ContactUpdateView(UpdateView):
    model = Contact
    fields = (
        "first_name",
        "last_name",
        "avatar",
        "email",
        "dob",
        "notes",
    )
    template_name = "contact_edit.html"


class ContactDeleteView(DeleteView):
    model = Contact
    template_name = "contact_delete.html"
    success_url = reverse_lazy("contact_list")


class ContactCreateView(CreateView):
    model = Contact
    template_name = "contact_new.html"
    fields = (
        "first_name",
        "last_name",
        "avatar",
        "email",
        "dob",
        "notes",
    )
