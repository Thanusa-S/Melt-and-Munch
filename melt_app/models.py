from django.db import models
from decimal import Decimal
from django.conf import settings
from django.core.validators import MinValueValidator
from django.utils.text import slugify




# Create your models here.


# 1. CATEGORY MODEL
class Category(models.Model):
    name = models.CharField(max_length=80, unique=True)
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)

        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


# 2. PRODUCT MODEL
class Product(models.Model):
    name = models.CharField(max_length=150)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField()

    price = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        validators=[MinValueValidator(Decimal("0.00"))]
    )

    image = models.ImageField(
        upload_to="products/",
        blank=True,
        null=True
    )

    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name="products"
    )

    is_featured = models.BooleanField(default=False)
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)

        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


## 3. CART MODEL
class Cart(models.Model):

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="shopping_cart"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def total_price(self):
        return sum(
            (line.subtotal for line in self.lines.all()),
            Decimal("0.00")
        )

    @property
    def item_count(self):
        return sum(line.quantity for line in self.lines.all())

    def __str__(self):
        return f"Cart for {self.user}"


# 4. CART LINE MODEL
class CartLine(models.Model):

    cart = models.ForeignKey(
        Cart,
        on_delete=models.CASCADE,
        related_name="lines"
    )

    # For ordinary products
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    # For ice cream products
    icecream = models.ForeignKey(
        "IceCream",
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    quantity = models.PositiveIntegerField(
        default=1,
        validators=[MinValueValidator(1)]
    )
    scoops = models.PositiveIntegerField(default=1)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["cart", "product"],
                condition=models.Q(product__isnull=False),
                name="unique_product_per_cart"
            ),
            models.UniqueConstraint(
                fields=["cart", "icecream"],
                condition=models.Q(icecream__isnull=False),
                name="unique_icecream_per_cart"
            )
        ]

    @property
    def item(self):
        return self.icecream if self.icecream_id else self.product

    @property
    def subtotal(self):
        return self.item.price * self.quantity * self.scoops

    def __str__(self):
        return f"{self.item.name} x {self.quantity}"


# 5. ORDER MODEL

class Order(models.Model):

    STATUS_CHOICES = [
        ("placed", "Placed"),
        ("processing", "Processing"),
        ("shipped", "Shipped"),
        ("completed", "Completed"),
        ("cancelled", "Cancelled"),
    ]

    ORDER_TYPE_CHOICES = [
        ("delivery", "Home Delivery"),
        ("takeaway", "Take Away"),
    ]

    PAYMENT_CHOICES = [
        ("cod", "Cash on Delivery"),
        ("upi", "UPI"),
        ("card", "Credit / Debit Card"),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="orders"
    )

    full_name = models.CharField(max_length=150)
    email = models.EmailField()
    phone = models.CharField(max_length=25)

    address = models.TextField(blank=True)
    city = models.CharField(max_length=100, blank=True)
    postal_code = models.CharField(max_length=15, blank=True)

    # NEW FIELD
    order_type = models.CharField(
        max_length=20,
        choices=ORDER_TYPE_CHOICES,
        default="delivery"
    )

    # NEW FIELD
    payment_method = models.CharField(
        max_length=20,
        choices=PAYMENT_CHOICES,
        default="cod"
    )

    total_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="placed"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.pk}"



# 6. ORDER LINE MODEL

class OrderLine(models.Model):

    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="lines"
    )

    product_name = models.CharField(max_length=150)

    unit_price = models.DecimalField(
        max_digits=8,
        decimal_places=2
    )

    quantity = models.PositiveIntegerField(
        validators=[MinValueValidator(1)]
    )

    # NEW FIELD
    scoops = models.PositiveIntegerField(default=1)

    @property
    def subtotal(self):
        return self.unit_price * self.quantity * self.scoops

    def __str__(self):
        return self.product_name



# 7. CONTACT MESSAGE MODEL
class ContactMessage(models.Model):

    name = models.CharField(max_length=120)
    email = models.EmailField()
    subject = models.CharField(max_length=160)
    message = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.subject


# 8. ICE CREAM MODEL
class IceCream(models.Model):

    CATEGORY_CHOICES = [
        ("classic", "Classic"),
        ("chocolate", "Chocolate"),
        ("fruit", "Fruit"),
        ("sundae", "Sundae"),
        ("premium", "Premium"),
        ("special", "Special"),
    ]

    name = models.CharField(max_length=150)

    slug = models.SlugField(
        unique=True,
        blank=True
    )

    category = models.CharField(
        max_length=30,
        choices=CATEGORY_CHOICES
    )

    description = models.TextField()

    price = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        validators=[MinValueValidator(Decimal("0.00"))]
    )

    image = models.ImageField(
        upload_to="ice_creams/",
        blank=True,
        null=True
    )

    is_available = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)

    stock_quantity = models.PositiveIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["name"]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)

        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
