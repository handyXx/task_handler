from django.contrib import admin

from .models import Category, Deposit, Task

admin.site.register(Category)
admin.site.register(Deposit)
admin.site.register(Task)
