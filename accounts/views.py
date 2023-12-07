import hashlib

from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View

from accounts.forms import CustomUserCreationForm


# class SignUpView(CreateView):
#     form_class = CustomUserCreationForm
#     success_url = reverse_lazy("login")
#     template_name = "registration/signup.html"


class SignUpView(View):
    template_name = "registration/signup.html"
    success_url = reverse_lazy("login")

    def get(self, request):
        form = CustomUserCreationForm()
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.avatar = self.get_gravatar_url(user.email)
            user.save()
            return redirect("login")
        return render(request, self.template_name, {"form": form})

    @staticmethod
    def get_gravatar_url(email):
        """
        Generate and return a gravatar URL.
        :param email: User's email address.
        :return: Gravatar based on the user's email address.
        """
        return (
            f"https://www.gravatar.com/avatar/{hashlib.md5(email.lower().encode()).hexdigest()}?d"
            f"=wavatar&s=150"
        )
