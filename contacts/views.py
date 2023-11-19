from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Q
from django.shortcuts import render
from django.views import View
from django.views.generic import ListView, FormView
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.edit import UpdateView, DeleteView, CreateView
from django.urls import reverse_lazy, reverse

from .models import Contact
from .forms import (
    PhoneNumberForm,
    DOBIntervalForm,
    SearcListForm,
)


class ContactListView(LoginRequiredMixin, ListView):
    model = Contact
    template_name = "contact_list.html"

    def get_queryset(self, *args, **kwargs):
        qs = super(ContactListView, self).get_queryset().filter(owner=self.request.user)
        qs = qs.order_by("last_name")
        return qs


class DOBListView(LoginRequiredMixin, ListView, FormView):
    template_name = "dob_list.html"
    success_url = reverse_lazy("dob_list.html")

    Contact.objects.get_upcoming_birthdays()

    def get(self, request, *args, **kwargs):
        form = DOBIntervalForm()
        return render(request, self.template_name, {"form": form})

    def post(self, request, *args, **kwargs):
        form = DOBIntervalForm(request.POST)
        if form.is_valid():
            interval = form.cleaned_data["interval"]
            queryset = Contact.objects.get_upcoming_birthdays(days=interval)
            return render(
                request,
                self.template_name,
                {"form": form, "contact_list": queryset, "interval": interval},
            )
        return render(request, self.template_name, {"form": form})


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


class SearchListView(LoginRequiredMixin, ListView, FormView):
    template_name = "search_list.html"
    success_url = reverse_lazy("search_list.html")

    def get(self, request, *args, **kwargs):
        form = SearcListForm()
        return render(request, self.template_name, {"form": form, "contact_list": []})

    def post(self, request, *args, **kwargs):
        form = SearcListForm(request.POST)
        if form.is_valid():
            search_last_name = form.cleaned_data["search"]
            search_first_name = form.cleaned_data["search_name"]
            queryset = Contact.objects.filter(
                Q(owner=request.user) & Q(last_name__icontains=search_last_name) & Q(first_name__icontains=search_first_name)
            ).order_by("last_name", "first_name")  
            return render(
                request,
                self.template_name,
                {"form": form, "contact_list": queryset},
            )
        return render(request, self.template_name, {"form": form, "contact_list": []})
