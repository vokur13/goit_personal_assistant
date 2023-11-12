from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views import View
from django.views.generic import ListView, DetailView, FormView
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.edit import UpdateView, DeleteView, CreateView
from django.urls import reverse_lazy, reverse

from .models import Contact
from .forms import PhoneNumberForm


class ContactListView(LoginRequiredMixin, ListView):
    model = Contact
    template_name = "contact_list.html"

    def get_queryset(self):
        return (
            super(ContactListView, self).get_queryset().filter(owner=self.request.user)
        )


class PhoneNumberGet(DeleteView):
    model = Contact
    template_name = "contact_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = PhoneNumberForm
        return context


class PhoneNumberPost(SingleObjectMixin, FormView):
    model = Contact
    form_class = PhoneNumberForm
    template_name = "contact_detail.html"
    object = {}

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        phonenumber = form.save(commit=False)
        phonenumber.contact = self.object
        phonenumber.owner = self.request.user
        phonenumber.save()
        return super().form_valid(form)

    def get_success_url(self):
        contact = self.object
        return reverse("contact_detail", kwargs={"pk": contact.pk})


class ContactDetailView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        view = PhoneNumberGet.as_view()
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        view = PhoneNumberPost.as_view()
        return view(request, *args, **kwargs)


# class ContactDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
#     model = Contact
#     template_name = "contact_detail.html"
#
#     def test_func(self):
#         obj = self.get_object()
#         return obj.owner == self.request.user
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context["form"] = PhoneNumberForm()
#         return context


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
