from .models import Category, Cart, Wishlist, Order


def navbar_categories(request):
    """Return main categories for navbar dropdown on ALL pages"""
    categories = Category.objects.filter(parent__isnull=True, is_active=True)
    return {"categories": categories}


def navbar_badges(request):
    """Return badge counts for navbar and FAB"""
    context = {
        "cart_count": 0,
        "wishlist_count": 0,
        "orders_count": 0,
    }

    if request.user.is_authenticated:
        # Get cart count
        try:
            cart = Cart.objects.get(user=request.user)
            context["cart_count"] = cart.total_items
        except Cart.DoesNotExist:
            pass

        # Get wishlist count
        try:
            wishlist = Wishlist.objects.get(user=request.user)
            context["wishlist_count"] = wishlist.total_items
        except Wishlist.DoesNotExist:
            pass

        # Get orders count (pending/processing)
        context["orders_count"] = (
            Order.objects.filter(user=request.user).exclude(status="delivered").count()
        )

    return context
