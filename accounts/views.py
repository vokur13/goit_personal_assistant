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
            # You can set the Gravatar URL based on the user's email
            user.avatar = (
                f"https://www.gravatar.com/avatar/{hashlib.md5(user.email.lower().encode()).hexdigest()}?d"
                f"=wavatar&s=150"
            )
            user.save()
            return redirect("login")  # Redirect to your login view
        return render(request, self.template_name, {"form": form})
