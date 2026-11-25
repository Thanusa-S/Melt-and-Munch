
from django.db.models import Sum
from .models import *


def cart_count(request):
    if request.user.is_authenticated:
        count = CartLine.objects.filter(
            cart__user=request.user
        ).aggregate(total=Sum("quantity"))["total"] or 0

    else:
        cart = request.session.get("cart", {})
        count = sum(int(quantity) for quantity in cart.values())

    return {
        "nav_cart_count": count
    }
