import uuid

import xlwt
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import FormView, ListView, TemplateView, View

from blog.models import *

from .forms import CategoryForm, DepositForm, TaskForm


class ExportExcel(View):
    model = Task

    def get(self, request, *args, **kwargs):
        return self.extract_excel()

    def get_queryset(self):
        prev_url = self.request.META.get("HTTP_REFERER")
        if "category" in prev_url:
            category_slug = prev_url.split("/")[-2]
            return self.model.objects.filter(
                category__in=[Category.objects.get(slug=category_slug)]
            )
        return self.model.objects.filter(user=self.request.user)

    def extract_excel(self):
        response = HttpResponse(content_type="application/ms-excel")
        response["Content-Disposition"] = f"attachment; filename={uuid.uuid4()}.xls"

        wb = xlwt.Workbook(encoding="utf-8")
        ws = wb.add_sheet("django-try")

        row_num = 0
        font_style = xlwt.XFStyle()
        font_style.font.FAMILY_MODERN = True
        qs = self.get_queryset()

        columns = [
            "task_id",
            "user_id",
            "task_name",
            "description",
            "price",
            "category",
            "purchased_at",
        ]
        for col_num in range(len(columns)):
            ws.write(row_num, col_num, columns[col_num], font_style)

        rows = list(
            qs.values_list(
                "id", "user", "name", "description", "price", "category", "created_at"
            )
        )
        for row in rows:
            row_num += 1
            for col_num in range(len(row)):
                ws.write(row_num, col_num, str(row[col_num]), font_style)

        wb.save(response)
        return response


class IndexView(LoginRequiredMixin, TemplateView):
    template_name = "blog/home.html"
    model = Task

    def get(self, request, *args, **kwargs):
        self.check_deposit(request)
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        try:
            context["deposit"] = Deposit.objects.get(user=self.request.user)
            context["elements"] = Task.objects.filter(user=self.request.user)
            context["categories"] = Category.objects.filter(user=self.request.user)
        except ObjectDoesNotExist as e:
            context["deposit"] = Deposit.objects.create(
                amount=0.00, user=self.request.user
            )

            context["elements"] = None
            context["categories"] = None
        return context

    def check_deposit(self, request):
        user_elements = self.model.objects.filter(user=request.user)
        user_deposit = Deposit.objects.filter(user=request.user)

        if user_deposit.exists():
            user_deposit = user_deposit[0]
            for element in user_elements:
                if not element.price_added:
                    user_deposit.amount = float(user_deposit.amount) - float(
                        element.price
                    )
                    element.price_added = True
                    element.save()
                    user_deposit.save()


class DepositView(LoginRequiredMixin, FormView):
    form_class = DepositForm
    template_name = "blog/deposit.html"

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        form.save()
        return redirect("blog:home")

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["instance"] = Deposit.objects.get(user=self.request.user)
        return kwargs


class CategoryElementsListView(LoginRequiredMixin, ListView):
    model = Task
    template_name = "blog/home.html"
    context_object_name = "elements"

    def get_queryset(self):
        return self.model.objects.filter(
            category__in=[Category.objects.get(slug=self.kwargs["category_slug"])]
        )


class CategoryCreationView(LoginRequiredMixin, FormView):
    form_class = CategoryForm
    template_name = "blog/category.html"

    def form_valid(self, form):
        category = form.save(commit=False)
        category.user = self.request.user
        category.save()
        return redirect("blog:home")


class TaskCreationView(LoginRequiredMixin, FormView):
    form_class = TaskForm
    template_name = "blog/element.html"

    def form_valid(self, form):
        task = form.save(commit=False)
        task.user = self.request.user
        task.save()
        return redirect("blog:home")

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        kwargs["request"] = self.request
        return kwargs


class TaskEditView(LoginRequiredMixin, FormView):
    form_class = TaskForm
    template_name = "blog/element.html"
    model = Task
    success_url = reverse_lazy("blog:home")

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["instance"] = self.model.objects.get(id=self.kwargs["id"])
        kwargs["user"] = self.request.user
        return kwargs

    def form_valid(self, form):
        # check if the user changed the price of the element and subtract from the deposit
        deposit = Deposit.objects.get(user=self.request.user)
        task_obj = self.model.objects.get(id=self.kwargs["id"])
        if float(task_obj.price) != float(form.cleaned_data["price"]):
            deposit.amount = (float(deposit.amount) + float(task_obj.price)) - float(
                form.cleaned_data["price"]
            )
            deposit.save()

        # save task instance
        form.save()
        return HttpResponseRedirect(self.success_url)
