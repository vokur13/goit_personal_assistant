from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView
from django.views.generic.edit import UpdateView, DeleteView, CreateView
from django.urls import reverse_lazy

from .models import Contact


class ContactListView(LoginRequiredMixin, ListView):
    model = Contact
    template_name = "contact_list.html"

    def get_queryset(self):
        return (
            super(ContactListView, self).get_queryset().filter(owner=self.request.user)
        )


class ContactDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Contact
    template_name = "contact_detail.html"

    def test_func(self):
        obj = self.get_object()
        return obj.owner == self.request.user


class ContactUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
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

    def test_func(self):
        obj = self.get_object()
        return obj.owner == self.request.user


class ContactDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Contact
    template_name = "contact_delete.html"
    success_url = reverse_lazy("contact_list")

    def test_func(self):
        obj = self.get_object()
        return obj.owner == self.request.user


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
