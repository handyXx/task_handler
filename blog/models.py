from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.template.defaultfilters import default, slugify
from django.utils.translation import gettext_lazy as _

from helpers.random_name_generator import RandomFileName


class TaskCustomManger(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(price_added=True)


class Category(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=70, null=False, unique=True)
    slug = models.SlugField(
        verbose_name=_("Category safe URL"), max_length=255, unique=True
    )

    objects = models.Manager

    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")
        ordering = ["-name"]

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    description = models.TextField(null=True)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True)
    price = models.DecimalField(max_length=6, max_digits=4, decimal_places=2)
    price_added = models.BooleanField(default=False)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    picture = models.ImageField(upload_to=RandomFileName("items_blog"), default=None)

    objects = TaskCustomManger()

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.name


class Deposit(models.Model):
    amount = models.DecimalField(
        default=0.00, null=False, decimal_places=2, max_digits=6
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    assigned_at = models.DateField(auto_now=Task)

    objects = models.Manager()

    def __str__(self):
        return f"{self.user.username} has {self.amount}$"
