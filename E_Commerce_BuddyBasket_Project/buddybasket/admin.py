from django.contrib import admin
from .models import Category, Product, Cart, CartItem, Order, OrderItem, ShippingAddress

# Register your models here.


class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "parent", "is_active", "created_at"]
    list_filter = ["is_active", "parent"]
    search_fields = ["name", "description"]
    prepopulated_fields = {"slug": ("name",)}
    list_editable = ["is_active"]


admin.site.register(Category, CategoryAdmin)


class ProductAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "category",
        "price",
        "stock",
        "is_active",
        "is_featured",
        "created_at",
    ]
    list_filter = ["is_active", "is_featured", "category"]
    search_fields = ["name", "description"]
    prepopulated_fields = {"slug": ("name",)}
    list_editable = ["price", "stock", "is_active", "is_featured"]


admin.site.register(Product, ProductAdmin)


class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0
    readonly_fields = ["created_at"]


class CartAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "total_items", "created_at", "updated_at"]
    list_filter = ["created_at"]
    search_fields = ["user__username", "user__email"]
    inlines = [CartItemInline]
    readonly_fields = ["id", "created_at", "updated_at"]


admin.site.register(Cart, CartAdmin)


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ["product_name", "product_price", "quantity"]


class OrderAdmin(admin.ModelAdmin):
    list_display = [
        "order_number",
        "user",
        "total",
        "status",
        "payment_status",
        "created_at",
    ]
    list_filter = ["status", "payment_status", "created_at"]
    search_fields = ["order_number", "user__username", "user__email"]
    list_editable = ["status", "payment_status"]
    inlines = [OrderItemInline]
    readonly_fields = [
        "order_number",
        "subtotal",
        "shipping_cost",
        "tax",
        "total",
        "created_at",
    ]
    fieldsets = (
        ("Order Information", {"fields": ("order_number", "user", "shipping_address")}),
        ("Totals", {"fields": ("subtotal", "shipping_cost", "tax", "total")}),
        ("Status", {"fields": ("status", "payment_status", "payment_method")}),
        ("Notes", {"fields": ("notes",)}),
        ("Dates", {"fields": ("created_at", "paid_at")}),
    )


admin.site.register(Order, OrderAdmin)


class ShippingAddressAdmin(admin.ModelAdmin):
    list_display = ["full_name", "user", "city", "state", "is_default"]
    list_filter = ["is_default", "country", "state"]
    search_fields = ["full_name", "address_line1", "city"]
    list_editable = ["is_default"]


admin.site.register(ShippingAddress, ShippingAddressAdmin)


# Optional: If you want to see CartItems separately too
class CartItemAdmin(admin.ModelAdmin):
    list_display = ["cart", "product", "quantity", "total_price", "created_at"]
    list_filter = ["created_at"]
    search_fields = ["product__name", "cart__user__username"]


admin.site.register(CartItem, CartItemAdmin)


class OrderItemAdmin(admin.ModelAdmin):
    list_display = ["order", "product_name", "quantity", "total_price"]
    list_filter = ["order__status"]
    search_fields = ["product_name", "order__order_number"]


admin.site.register(OrderItem, OrderItemAdmin)
