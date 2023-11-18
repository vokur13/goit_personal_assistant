from django.urls import path

from .views import (
    ContactListView,
    ContactDetailView,
    ContactUpdateView,
    ContactDeleteView,
    ContactCreateView,
    DOBListView,
    SearchListView,
)

urlpatterns = [
    path("<int:pk>/", ContactDetailView.as_view(), name="contact_detail"),
    path("<int:pk>/edit", ContactUpdateView.as_view(), name="contact_edit"),
    path("<int:pk>/delete", ContactDeleteView.as_view(), name="contact_delete"),
    path("new/", ContactCreateView.as_view(), name="contact_new"),
    path("dob_list/", DOBListView.as_view(), name="dob_list"),
    path("search_list/", SearchListView.as_view(), name="search_list"),
    path("", ContactListView.as_view(), name="contact_list"),
]
