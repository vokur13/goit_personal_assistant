from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView
from django.views.generic.edit import UpdateView, DeleteView, CreateView
from django.urls import reverse_lazy

from .models import Contact


class ContactListView(LoginRequiredMixin, ListView):
    model = Contact
    template_name = "contact_list.html"


class ContactDetailView(LoginRequiredMixin, DetailView):
    model = Contact
    template_name = "contact_detail.html"


class ContactUpdateView(LoginRequiredMixin, UpdateView):
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


class ContactDeleteView(LoginRequiredMixin, DeleteView):
    model = Contact
    template_name = "contact_delete.html"
    success_url = reverse_lazy("contact_list")


class ContactCreateView(LoginRequiredMixin, CreateView):
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

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)
