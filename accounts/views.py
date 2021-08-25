from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import FormView

from blog.forms import SignUpForm
from blog.models import Deposit


class SignUpView(FormView):
    form_class = SignUpForm
    template_name = "account/signup.html"

    def form_valid(self, form):
        # save the sign up form
        form.save()

        # authenticate the signed up user and log him in
        username = form.cleaned_data.get("username")
        raw_password = form.cleaned_data.get("password1")
        user = authenticate(username=username, password=raw_password)
        login(self.request, user)

        # initiate the deposit of the user
        Deposit.objects.create(user=user)

        return redirect("blog:home")


class LogInView(FormView):
    form_class = AuthenticationForm
    template_name = "account/login.html"
    success_url = reverse_lazy("blog:deposit")

    def dispatch(self, request, *args, **kwargs):
        try:
            if request.user.is_authenticated():
                return HttpResponseRedirect("blog:home")
        except TypeError as e:
            pass
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        user = authenticate(username=username, password=password)

        if user is not None:
            login(self.request, user)
            return redirect("/")

        return super(LogInView, self).form_valid(form)
