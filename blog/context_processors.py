from .models import Deposit
from django.core.exceptions import ObjectDoesNotExist


def deposit(request):
    if request.user.is_anonymous:
        return {"deposit": 0.00}
    try:
        return {"deposit": Deposit.objects.get(user=request.user)}
    except ObjectDoesNotExist:
        return {"deposit": 0.00}
