
from django.contrib import admin
from .models import *


# CATEGORY ADMIN
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    search_fields = ("name",)
    prepopulated_fields = {"slug": ("name",)}


# PRODUCT ADMIN
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "category",
        "price",
        "is_available",
        "is_featured",
    )
    list_filter = ("category", "is_available", "is_featured")
    search_fields = ("name", "description")
    prepopulated_fields = {"slug": ("name",)}
    list_editable = ("price", "is_available", "is_featured")


# ORDER LINE INLINE
class OrderLineInline(admin.TabularInline):
    model = OrderLine
    extra = 0
    readonly_fields = ("product_name", "unit_price", "quantity")


# ORDER ADMIN
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "full_name",
        "total_price",
        "status",
        "created_at",
    )
    list_filter = ("status", "created_at")
    search_fields = ("full_name", "email", "user__username")
    inlines = [OrderLineInline]
    list_editable = ("status",)


# CART LINE INLINE
class CartLineInline(admin.TabularInline):
    model = CartLine
    extra = 0


# CART ADMIN
@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ("user", "created_at")
    inlines = [CartLineInline]


# CONTACT MESSAGE ADMIN
@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "subject", "created_at")
    list_filter = ("created_at",)
    search_fields = ("name", "email", "subject")


# ICE CREAM ADMIN
@admin.register(IceCream)
class IceCreamAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "category",
        "price",
        "stock_quantity",
        "is_available",
        "is_featured",
    )
    list_filter = ("category", "is_available", "is_featured")
    search_fields = ("name", "description")
    prepopulated_fields = {"slug": ("name",)}
    list_editable = (
        "price",
        "stock_quantity",
        "is_available",
        "is_featured",
    )
    ordering = ("name",)



