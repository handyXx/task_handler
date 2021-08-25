from .models import Deposit


def deposit(request):
    if request.user.is_anonymous:
        return {"deposit": 0.00}
    return {"deposit": Deposit.objects.get(user=request.user)}
