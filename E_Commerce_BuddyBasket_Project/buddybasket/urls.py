from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("products/", views.all_products, name="all_products"),
    path(
        "category/<slug:category_slug>/",
        views.category_products,
        name="category_products",
    ),
    path(
        "product/<slug:category_slug>/<slug:product_slug>/",
        views.product_detail,
        name="product_detail",
    ),
    path("search/", views.search_products, name="search_products"),
    # New pages
    path("about/", views.about, name="about"),
    path("contact/", views.contact, name="contact"),
    path("cart/", views.cart_view, name="cart"),
    path("login/", views.login_view, name="login"),
    path("register/", views.register_view, name="register"),
    path("logout/", views.logout_view, name="logout"),
    path("checkout/", views.checkout_view, name="checkout"),
    path("order-confirmation/", views.order_confirmation, name="order_confirmation"),
    # CART OPERATION URLS - Add these lines
    path("add-to-cart/<int:product_id>/", views.add_to_cart, name="add_to_cart"),
    path("update-cart/<int:item_id>/", views.update_cart, name="update_cart"),
    path(
        "remove-from-cart/<int:item_id>/",
        views.remove_from_cart,
        name="remove_from_cart",
    ),
    path("clear-cart/", views.clear_cart, name="clear_cart"),
    path("wishlist/", views.wishlist_view, name="wishlist"),
    path(
        "add-to-wishlist/<int:product_id>/",
        views.add_to_wishlist,
        name="add_to_wishlist",
    ),
    path(
        "remove-from-wishlist/<int:item_id>/",
        views.remove_from_wishlist,
        name="remove_from_wishlist",
    ),
    path("move-to-cart/<int:item_id>/", views.move_to_cart, name="move_to_cart"),
    path(
        "get-wishlist-item/<int:product_id>/",
        views.get_wishlist_item,
        name="get_wishlist_item",
    ),
    path("orders/", views.order_history, name="order_history"),
    path("order/<int:order_id>/", views.order_detail, name="order_detail"),
    path("create-order/", views.create_order, name="create_order"),
    path("get-order/<int:order_id>/", views.get_order, name="get_order"),
    # Add these to your urlpatterns
    path(
        "create-razorpay-order/",
        views.create_razorpay_order,
        name="create_razorpay_order",
    ),
    path("razorpay-callback/", views.razorpay_callback, name="razorpay_callback"),
]
