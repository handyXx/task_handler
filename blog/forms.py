from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Category, Deposit, Task


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False, help_text="Optional.")
    last_name = forms.CharField(max_length=30, required=False, help_text="Optional.")
    email = forms.EmailField(
        max_length=254, help_text="Required. Inform a valid email address."
    )

    class Meta:
        model = User
        fields = (
            "username",
            "first_name",
            "last_name",
            "email",
            "password1",
            "password2",
        )


class DepositForm(forms.ModelForm):
    class Meta:
        model = Deposit
        fields = ("amount",)


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ("name",)


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ("name", "description", "price", "category")

    def __init__(self, *args, **kwargs):
        self._user = kwargs.pop("user", None)
        self._prev_url = kwargs.pop("prev_url", None)
        super().__init__(*args, **kwargs)
        if self._prev_url and "category" in self._prev_url:
            category_slug = self._prev_url.split("/")[-2]
            self.fields["category"].initial = Category.objects.get(slug=category_slug)
            self.fields["category"].queryset = None
        else:
            if self._user:
                # print(dir(self.fields["category"]))
                self.fields["category"].queryset = Category.objects.filter(
                    user=self._user
                )
                self.fields["category"].initial = Category.objects.filter(
                    user=self._user
                )[0]
