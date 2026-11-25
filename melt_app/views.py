from decimal import Decimal
from .models import *
from .forms import *


from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
# from django.contrib.auth.views import LoginView, LogoutView
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST
from django.views.generic import FormView, View
from django.urls import reverse
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.utils import timezone
from django.db.models import Sum
from django.contrib.auth import get_user_model
from django.contrib.admin.views.decorators import staff_member_required

from django.views.generic import FormView, View





def _cart_rows(request):
    rows = []

    if request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user).first()

        if cart:
            lines = cart.lines.select_related(
                "product", "icecream"
            )

            for line in lines:
                item = line.item

                if item and item.is_available:
                    item_type = (
                        "icecream" if line.icecream_id else "product"
                    )
                    rows.append((
                        item,
                        line.quantity,
                        line.scoops,
                        item_type
                    ))

        return rows

    cart = request.session.get("cart", {})
    scoop_data = request.session.get("cart_scoops", {})

    for key, quantity in cart.items():
        try:
            item_type, item_id = key.split("_")
            item_id = int(item_id)
            quantity = int(quantity)
        except (ValueError, TypeError):
            continue

        if quantity <= 0:
            continue

        if item_type == "icecream":
            item = IceCream.objects.filter(
                pk=item_id, is_available=True
            ).first()
        elif item_type == "product":
            item = Product.objects.filter(
                pk=item_id, is_available=True
            ).first()
        else:
            item = None

        if item:
            scoops = int(scoop_data.get(key, 1))
            rows.append((item, quantity, max(1, scoops), item_type))

    return rows


def _add_to_cart(request, item, quantity, scoops=1):
    quantity = max(1, min(int(quantity), 99))
    scoops = max(1, min(int(scoops), 10))

    if request.user.is_authenticated:
        cart, _ = Cart.objects.get_or_create(user=request.user)

        if isinstance(item, IceCream):
            lookup = {"icecream": item}
        else:
            lookup = {"product": item}

        line, created = CartLine.objects.get_or_create(
            cart=cart,
            **lookup,
            defaults={
                "quantity": quantity,
                "scoops": scoops
            }
        )

        if not created:
            line.quantity = min(99, line.quantity + quantity)
            line.scoops = scoops
            line.save(update_fields=["quantity", "scoops"])

    else:
        cart = request.session.get("cart", {})
        scoop_data = request.session.get("cart_scoops", {})

        if isinstance(item, IceCream):
            key = f"icecream_{item.id}"
        else:
            key = f"product_{item.id}"

        cart[key] = min(99, int(cart.get(key, 0)) + quantity)
        scoop_data[key] = scoops

        request.session["cart"] = cart
        request.session["cart_scoops"] = scoop_data
        request.session.modified = True


def _set_quantity(request, item_type, item_id, quantity, scoops):
    quantity = max(0, min(int(quantity), 99))
    scoops = max(1, min(int(scoops), 10))

    if request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user).first()

        if cart:
            lookup = (
                {"icecream_id": item_id}
                if item_type == "icecream"
                else {"product_id": item_id}
            )

            line = CartLine.objects.filter(
                cart=cart, **lookup
            ).first()

            if line:
                if quantity == 0:
                    line.delete()
                else:
                    line.quantity = quantity
                    line.scoops = scoops
                    line.save(update_fields=["quantity", "scoops"])

    else:
        cart = request.session.get("cart", {})
        scoop_data = request.session.get("cart_scoops", {})
        key = f"{item_type}_{item_id}"

        if quantity == 0:
            cart.pop(key, None)
            scoop_data.pop(key, None)
        else:
            cart[key] = quantity
            scoop_data[key] = scoops

        request.session["cart"] = cart
        request.session["cart_scoops"] = scoop_data
        request.session.modified = True



@require_POST
def add_to_cart(request, item_type, item_id):

    if item_type == "icecream":
        item = get_object_or_404(
            IceCream,
            pk=item_id,
            is_available=True
        )

    elif item_type == "product":
        item = get_object_or_404(
            Product,
            pk=item_id,
            is_available=True
        )

    else:
        return redirect("ice_creams")

    try:
        quantity = int(request.POST.get("quantity", 1))
        scoops = int(request.POST.get("scoops", 1))
    except (TypeError, ValueError):
        quantity = 1
        scoops = 1

    _add_to_cart(request, item, quantity, scoops)

    action = request.POST.get("action", "cart")

    # Buy Now
    if action == "buy_now":
        messages.success(
            request,
            f"{item.name} is ready for checkout!"
        )
        return redirect("checkout")

    # Add to Cart
    messages.success(
        request,
        f"{item.name} added to your cart!"
    )

    return redirect("cart")



# def _set_quantity(request, item_type, item_id, quantity):

#     if request.user.is_authenticated:

#         cart = Cart.objects.filter(
#             user=request.user
#         ).first()

#         if cart:

#             lookup = (
#                 {"icecream_id": item_id}
#                 if item_type == "icecream"
#                 else {"product_id": item_id}
#             )

#             line = CartLine.objects.filter(
#                 cart=cart,
#                 **lookup
#             ).first()

#             if line:
#                 if quantity <= 0:
#                     line.delete()
#                 else:
#                     line.quantity = min(quantity, 99)
#                     line.save(update_fields=["quantity"])

#     else:
#         cart = request.session.get("cart", {})
#         key = f"{item_type}_{item_id}"

#         if quantity <= 0:
#             cart.pop(key, None)
#         else:
#             if item_type == "icecream":
#                 exists = IceCream.objects.filter(
#                     pk=item_id,
#                     is_available=True
#                 ).exists()
#             else:
#                 exists = Product.objects.filter(
#                     pk=item_id,
#                     is_available=True
#                 ).exists()

#             if exists:
#                 cart[key] = min(quantity, 99)

#         request.session["cart"] = cart
#         request.session.modified = True




def cart_view(request):
    rows = _cart_rows(request)

    total = sum(
        (
            item.price * quantity * scoops
            for item, quantity, scoops, item_type in rows
        ),
        Decimal("0.00")
    )

    return render(request, "shop/cart.html", {
        "rows": rows,
        "total": total,
        "nav_cart_count": sum(
            quantity for item, quantity, scoops, item_type in rows
        )
    })


@require_POST
def update_cart(request, item_type, item_id):
    try:
        quantity = int(request.POST.get("quantity", 1))
        scoops = int(request.POST.get("scoops", 1))
    except (TypeError, ValueError):
        messages.error(request, "Please enter valid quantities.")
        return redirect("cart")

    if item_type not in ["icecream", "product"]:
        return redirect("cart")

    _set_quantity(
        request,
        item_type,
        item_id,
        quantity,
        scoops
    )

    messages.success(request, "Your cart has been updated!")
    return redirect("cart")


def home(request):
    featured = Product.objects.filter(
        is_available=True,
        is_featured=True,
    ).select_related("category")[:8]

    if not featured:
        featured = Product.objects.filter(
            is_available=True,
        ).select_related("category")[:8]

    return render(request, "shop/home.html", {
        "featured": featured,
    })


def product_list(request):
    products = Product.objects.filter(
        is_available=True,
    ).select_related("category")

    category = request.GET.get("category", "")
    search = request.GET.get("q", "").strip()

    if category:
        products = products.filter(category__slug=category)

    if search:
        products = products.filter(name__icontains=search)

    return render(request, "shop/products.html", {
        "products": products,
        "categories": Category.objects.all(),
        "selected_category": category,
        "search_query": search,
    })


def product_detail(request, slug):
    product = get_object_or_404(
        Product,
        slug=slug,
        is_available=True,
    )

    return render(request, "shop/product_detail.html", {
        "product": product,
    })



@login_required
@transaction.atomic
def checkout(request):

    rows = _cart_rows(request)

    if not rows:
        messages.info(request, "Your cart is empty.")
        return redirect("ice_creams")

    total = sum(
        (
            item.price * quantity * scoops
            for item, quantity, scoops, item_type in rows
        ),
        Decimal("0.00")
    )

    if request.method == "POST":

        form = CheckoutForm(request.POST)

        order_type = request.POST.get("order_type", "delivery")
        payment_method = request.POST.get("payment_method", "cod")

        if order_type not in ["delivery", "takeaway"]:
            form.add_error(None, "Please select a valid order type.")

        if payment_method not in ["cod", "upi", "card"]:
            form.add_error(None, "Please select a valid payment method.")

        if order_type == "delivery" and form.is_valid():
            for field in ["address", "city", "postal_code"]:
                if not form.cleaned_data.get(field):
                    form.add_error(field, "This field is required for delivery.")

        if form.is_valid():

            if order_type not in ["delivery", "takeaway"]:
                pass
            elif payment_method not in ["cod", "upi", "card"]:
                pass
            elif order_type == "delivery" and any(
                not form.cleaned_data.get(field)
                for field in ["address", "city", "postal_code"]
            ):
                pass
            else:
                order = form.save(commit=False)

                order.user = request.user
                order.total_price = total
                order.order_type = order_type
                order.payment_method = payment_method

                if order_type == "takeaway":
                    order.address = ""
                    order.city = ""
                    order.postal_code = ""

                order.save()

                for item, quantity, scoops, item_type in rows:

                    OrderLine.objects.create(
                        order=order,
                        product_name=item.name,
                        unit_price=item.price,
                        quantity=quantity,
                        scoops=scoops
                    )

                Cart.objects.filter(user=request.user).delete()

                request.session["cart"] = {}
                request.session["cart_scoops"] = {}
                request.session.modified = True

                return render(
                    request,
                    "shop/order_success.html",
                    {"order": order}
                )

    else:
        form = CheckoutForm(initial={
            "full_name": request.user.get_full_name(),
            "email": request.user.email,
        })

    return render(request, "shop/checkout.html", {
        "form": form,
        "rows": rows,
        "total": total,
        "nav_cart_count": sum(
            quantity for item, quantity, scoops, item_type in rows
        )
    })


def register(request):
    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":
        form = RegisterForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Welcome to Melt & Munch!")
            return redirect("home")
    else:
        form = RegisterForm()

    return render(request, "shop/register.html", {
        "form": form,
    })


def _merge_guest_cart(request, user):
    guest_cart = request.session.get("cart", {})
    guest_scoops = request.session.get("cart_scoops", {})

    for key, quantity in guest_cart.items():
        try:
            item_type, item_id = key.split("_")
            quantity = int(quantity)
            item_id = int(item_id)
        except (ValueError, TypeError):
            continue

        if quantity <= 0:
            continue

        if item_type == "icecream":
            item = IceCream.objects.filter(
                pk=item_id,
                is_available=True
            ).first()

        elif item_type == "product":
            item = Product.objects.filter(
                pk=item_id,
                is_available=True
            ).first()

        else:
            item = None

        if item:
            scoops = int(guest_scoops.get(key, 1))

            _add_to_cart(
                request,
                item,
                quantity,
                scoops
            )

    request.session["cart"] = {}
    request.session["cart_scoops"] = {}
    request.session.modified = True


class StoreLoginView(FormView):
    template_name = "shop/login.html"
    form_class = LoginForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["request"] = self.request
        return kwargs

    def form_valid(self, form):
        user = form.get_user()

        if user.is_staff or user.is_superuser:
            messages.error(
                self.request,
                "Please use the admin login page."
            )
            return redirect("login")

        # IMPORTANT: Authenticate the customer with Django
        login(self.request, user)

        # Merge previously added guest cart items
        _merge_guest_cart(self.request, user)

        # Store customer information
        self.request.session["store_customer_id"] = user.id
        self.request.session["store_customer_name"] = user.username

        messages.success(
            self.request,
            f"Welcome back, {user.username}!"
        )

        next_url = (
            self.request.POST.get(REDIRECT_FIELD_NAME)
            or self.request.GET.get(REDIRECT_FIELD_NAME)
        )

        from django.utils.http import url_has_allowed_host_and_scheme

        if next_url and url_has_allowed_host_and_scheme(
            next_url,
            allowed_hosts={self.request.get_host()},
            require_https=self.request.is_secure()
        ):
            return redirect(next_url)

        return redirect("home")


class StoreLogoutView(View):

    def get(self, request, *args, **kwargs):
        return self.logout_user(request)

    def post(self, request, *args, **kwargs):
        return self.logout_user(request)

    def logout_user(self, request):

        logout(request)

        messages.success(
            request,
            "You have logged out successfully!"
        )

        return redirect("home")


def about(request):
    return render(request, "shop/about.html")


def contact(request):
    if request.method == "POST":
        form = ContactForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(
                request,
                "Thanks! Your message has been received.",
            )
            return redirect("contact")
    else:
        form = ContactForm()

    return render(request, "shop/contact.html", {
        "form": form,
    })

def ice_creams(request):

    ice_creams_list = IceCream.objects.filter(
        is_available=True
    )

    form = IceCreamSearchForm(request.GET)

    if form.is_valid():

        search = form.cleaned_data.get('search')
        category = form.cleaned_data.get('category')
        sort = form.cleaned_data.get('sort')

        if search:
            ice_creams_list = ice_creams_list.filter(
                name__icontains=search
            ) | ice_creams_list.filter(
                description__icontains=search
            )

        if category:
            ice_creams_list = ice_creams_list.filter(
                category=category
            )

        if sort == 'price_low':
            ice_creams_list = ice_creams_list.order_by('price')

        elif sort == 'price_high':
            ice_creams_list = ice_creams_list.order_by('-price')

        elif sort == 'name':
            ice_creams_list = ice_creams_list.order_by('name')

    context = {
        'ice_creams': ice_creams_list,
        'form': form,
        'total_ice_creams': ice_creams_list.count(),
    }

    return render(
        request,
        'shop/ice_creams.html',
        context
    )


# DASHBOARD ICE CREAM PAGE

@staff_member_required(login_url='/admin/login/')
def dashboard_icecreams(request):

    icecreams = IceCream.objects.all().order_by('-created_at')

    search = request.GET.get('search', '')
    category = request.GET.get('category', '')
    status = request.GET.get('status', '')

    if search:
        icecreams = icecreams.filter(
            name__icontains=search
        )

    if category:
        icecreams = icecreams.filter(
            category=category
        )

    if status == 'available':
        icecreams = icecreams.filter(is_available=True)

    elif status == 'unavailable':
        icecreams = icecreams.filter(is_available=False)

    context = {
        'icecreams': icecreams,
        'search': search,
        'selected_category': category,
        'selected_status': status,
        'categories': IceCream.CATEGORY_CHOICES,
    }

    return render(
        request,
        'dashboard/icecreams.html',
        context
    )


# ADD ICE CREAM

@staff_member_required(login_url='/admin/login/')
def add_icecream(request):

    if request.method == 'POST':

        form = IceCreamForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                'Ice cream added successfully!'
            )

            return redirect('dashboard_icecreams')

    else:
        form = IceCreamForm()

    return render(
        request,
        'dashboard/icecream_form.html',
        {
            'form': form,
            'page_title': 'Add New Ice Cream',
        }
    )


# EDIT ICE CREAM

@staff_member_required(login_url='/admin/login/')
def edit_icecream(request, pk):

    icecream = get_object_or_404(
        IceCream,
        pk=pk
    )

    if request.method == 'POST':

        form = IceCreamForm(
            request.POST,
            request.FILES,
            instance=icecream
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                'Ice cream updated successfully!'
            )

            return redirect('dashboard_icecreams')

    else:
        form = IceCreamForm(
            instance=icecream
        )

    return render(
        request,
        'dashboard/icecream_form.html',
        {
            'form': form,
            'page_title': 'Edit Ice Cream',
            'icecream': icecream,
        }
    )


# DELETE ICE CREAM

@staff_member_required(login_url='/admin/login/')
@require_POST
def delete_icecream(request, pk):

    icecream = get_object_or_404(
        IceCream,
        pk=pk
    )

    icecream.delete()

    messages.success(
        request,
        'Ice cream deleted successfully!'
    )

    return redirect('dashboard_icecreams')





# DASHBOARD VIEWS

@staff_member_required(login_url="/admin-login/")
def admin_dashboard(request):

    today = timezone.localdate()

    today_orders = Order.objects.filter(
        created_at__date=today
    )

    context = {
        "total_sales": today_orders.filter(
            status="completed"
        ).aggregate(total=Sum("total_price"))["total"] or Decimal("0.00"),

        "total_orders": Order.objects.count(),

        "today_orders": today_orders.count(),

        "total_products": Product.objects.count(),

        "total_icecreams": IceCream.objects.count(),

        "total_customers": get_user_model().objects.filter(
            is_staff=False,
            is_superuser=False
        ).count(),

        "pending_orders": Order.objects.filter(
            status="placed"
        ).count(),

        "low_stock": IceCream.objects.filter(
            stock_quantity__lte=5
        ).count(),

        "recent_orders": Order.objects.select_related(
            "user"
        ).order_by("-created_at")[:7],

        "best_sellers": OrderLine.objects.values(
            "product_name"
        ).annotate(
            sold=Sum("quantity")
        ).order_by("-sold")[:5],

        "monthly_sales": today_orders.aggregate(
            total=Sum("total_price")
        )["total"] or Decimal("0.00"),
    }

    return render(request, "dashboard/dashboard.html", context)



# Store product management
@staff_member_required(login_url="/admin-login/")
def dashboard_products(request):

    products = Product.objects.select_related(
        "category"
    ).order_by("-created_at")

    search = request.GET.get("search", "")

    if search:
        products = products.filter(name__icontains=search)

    return render(request, "dashboard/products.html", {
        "products": products,
        "search": search,
    })

# Orders management
@staff_member_required(login_url="/admin-login/")
def dashboard_orders(request):

    orders = Order.objects.select_related(
        "user"
    ).prefetch_related(
        "lines"
    ).order_by("-created_at")

    status = request.GET.get("status", "")

    if status:
        orders = orders.filter(status=status)

    return render(request, "dashboard/orders.html", {
        "orders": orders,
        "statuses": Order.STATUS_CHOICES,
        "selected_status": status,
    })


@staff_member_required(login_url="/adminlogin/")
def update_order_status(request, pk):

    order = get_object_or_404(Order, pk=pk)

    if request.method == "POST":
        form = OrderStatusForm(request.POST, instance=order)

        if form.is_valid():
            form.save()
            messages.success(request, f"Order #{order.pk} updated!")

    return redirect("dashboard_orders")

# Customers

@staff_member_required(login_url="/admin/login/")
def dashboard_customers(request):

    User = get_user_model()

    customers = User.objects.filter(
        is_staff=False,
        is_superuser=False
    ).order_by("-date_joined")

    search = request.GET.get("search", "")

    if search:
        customers = customers.filter(
            username__icontains=search
        ) | customers.filter(
            email__icontains=search
        )

    return render(request, "dashboard/customers.html", {
        "customers": customers,
        "search": search,
    })

# Inventory

@staff_member_required(login_url="admin-login/")
def dashboard_inventory(request):

    icecreams = IceCream.objects.all().order_by("stock_quantity")

    return render(request, "dashboard/inventory.html", {
        "icecreams": icecreams,
        "low_stock_count": IceCream.objects.filter(
            stock_quantity__lte=5
        ).count(),
    })

# Customer messages

@staff_member_required(login_url="admin_login")
def dashboard_messages(request):

    contact_messages = ContactMessage.objects.all().order_by(
        "-created_at"
    )

    return render(request, "dashboard/messages.html", {
        "contact_messages": contact_messages,
    })

@login_required
def my_orders(request):
    orders = Order.objects.filter(
        user=request.user
    ).order_by("-id")

    for order in orders:
        order.order_items = OrderLine.objects.filter(
            order=order
        )

    return render(request, "shop/my_orders.html", {
        "orders": orders,
    })

from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect


def admin_login(request):

    # If already logged in as admin, go to dashboard
    if request.user.is_authenticated:
        if request.user.is_staff or request.user.is_superuser:
            return redirect("admin_dashboard")

    error = ""

    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            if user.is_staff or user.is_superuser:
                login(request, user)
                return redirect("admin_dashboard")

            else:
                error = "You are not authorized as an admin."

        else:
            error = "Invalid username or password."

    return render(request, "dashboard/admin_login.html", {
        "error": error
    })

@require_POST
def admin_logout(request):
    logout(request)
    return redirect("admin_login")