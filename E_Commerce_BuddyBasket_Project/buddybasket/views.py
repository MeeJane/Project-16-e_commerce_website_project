import razorpay
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseBadRequest
import json
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages


from .models import (
    Category,
    Product,
    Cart,
    CartItem,
    Order,
    OrderItem,
    Wishlist,
    WishlistItem,
    ShippingAddress,
)


def home(request):
    """Homepage view"""
    categories = Category.objects.filter(parent__isnull=True, is_active=True)
    featured_products = Product.objects.filter(is_featured=True, is_active=True)[:8]

    # Get wishlisted product IDs if user is logged in
    wishlisted_ids = []
    if request.user.is_authenticated:
        try:
            wishlist = Wishlist.objects.get(user=request.user)
            wishlisted_ids = wishlist.items.values_list("product_id", flat=True)
        except Wishlist.DoesNotExist:
            wishlisted_ids = []

    context = {
        "categories": categories,
        "featured_products": featured_products,
        "wishlisted_ids": list(wishlisted_ids),  # Convert to list for template
    }
    return render(request, "buddybasket/home.html", context)


def all_products(request):
    """Show all products"""
    products = Product.objects.filter(is_active=True)

    # Get wishlisted product IDs if user is logged in
    wishlisted_ids = []
    if request.user.is_authenticated:
        try:
            wishlist = Wishlist.objects.get(user=request.user)
            wishlisted_ids = wishlist.items.values_list("product_id", flat=True)
        except Wishlist.DoesNotExist:
            wishlisted_ids = []

    context = {
        "products": products,
        "wishlisted_ids": list(wishlisted_ids),
    }
    return render(request, "buddybasket/product_list.html", context)


def category_products(request, category_slug):
    """Show products in a category"""
    category = get_object_or_404(Category, slug=category_slug, is_active=True)

    # Get all products in this category and its subcategories
    if category.parent is None:  # Main category
        # Get all subcategories
        subcategories = Category.objects.filter(parent=category, is_active=True)
        products = Product.objects.filter(
            category__in=[category] + list(subcategories), is_active=True
        )
    else:  # Subcategory
        products = Product.objects.filter(category=category, is_active=True)

    # Get wishlisted product IDs if user is logged in
    wishlisted_ids = []
    if request.user.is_authenticated:
        try:
            wishlist = Wishlist.objects.get(user=request.user)
            wishlisted_ids = wishlist.items.values_list("product_id", flat=True)
        except Wishlist.DoesNotExist:
            wishlisted_ids = []

    context = {
        "category": category,
        "products": products,
        "wishlisted_ids": list(wishlisted_ids),
    }
    return render(request, "buddybasket/product_list.html", context)


def product_detail(request, category_slug, product_slug):
    """Show single product detail"""
    product = get_object_or_404(Product, slug=product_slug, is_active=True)

    context = {
        "product": product,
    }
    return render(request, "buddybasket/product_detail.html", context)


def search_products(request):
    """Search products by name or category"""
    query = request.GET.get("q", "")
    products = Product.objects.filter(is_active=True)

    if query:
        products = products.filter(
            Q(name__icontains=query)
            | Q(category__name__icontains=query)
            | Q(description__icontains=query)
        ).distinct()

    # Get wishlisted product IDs if user is logged in
    wishlisted_ids = []
    if request.user.is_authenticated:
        try:
            wishlist = Wishlist.objects.get(user=request.user)
            wishlisted_ids = wishlist.items.values_list("product_id", flat=True)
        except Wishlist.DoesNotExist:
            wishlisted_ids = []

    context = {
        "products": products,
        "query": query,
        "wishlisted_ids": list(wishlisted_ids),
    }
    return render(request, "buddybasket/product_list.html", context)


def about(request):
    """About Us page"""
    return render(request, "buddybasket/about.html")


def contact(request):
    """Contact Us page"""
    return render(request, "buddybasket/contact.html")


from django.http import JsonResponse
import json


def cart_view(request):
    """Shopping cart page"""
    if not request.user.is_authenticated:
        context = {
            "cart_items": [],
            "subtotal": 0,
            "total": 0,
            "discount": 0,
        }
        return render(request, "buddybasket/cart.html", context)

    # Get or create cart for logged in user
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = cart.items.all().select_related("product__category")

    # Calculate totals
    subtotal = cart.subtotal
    shipping = 0 if subtotal >= 499 else 40
    total = subtotal + shipping

    context = {
        "cart_items": cart_items,
        "subtotal": subtotal,
        "total": total,
        "discount": 0,
    }
    return render(request, "buddybasket/cart.html", context)


def add_to_cart(request, product_id):
    """Add item to cart"""
    print(f"===== ADD TO CART CALLED for product {product_id} =====")
    print(f"User: {request.user}")
    print(f"Authenticated: {request.user.is_authenticated}")
    print(f"Method: {request.method}")

    if not request.user.is_authenticated:
        return JsonResponse({"success": False, "error": "Login required"}, status=401)

    if request.method == "POST":
        try:
            product = Product.objects.get(id=product_id, is_active=True)
            print(f"Product found: {product.name}")

            cart, created = Cart.objects.get_or_create(user=request.user)
            print(f"Cart: {cart.id}, Created: {created}")

            # Check if item already in cart
            cart_item, created = CartItem.objects.get_or_create(
                cart=cart, product=product, defaults={"quantity": 1}
            )
            print(f"CartItem: {cart_item}, Created: {created}")

            if not created:
                # Increase quantity if already exists
                cart_item.quantity += 1
                cart_item.save()
                print(f"Quantity increased to: {cart_item.quantity}")

            print(f"Total items in cart: {cart.total_items}")

            return JsonResponse(
                {
                    "success": True,
                    "cart_count": cart.total_items,
                    "message": "Added to cart successfully",
                }
            )

        except Product.DoesNotExist:
            print(f"Product {product_id} not found!")
            return JsonResponse(
                {"success": False, "error": "Product not found"}, status=404
            )

    return JsonResponse({"success": False, "error": "Invalid request"}, status=400)


def update_cart(request, item_id):
    """Update cart item quantity"""
    if not request.user.is_authenticated:
        return JsonResponse({"success": False, "error": "Login required"}, status=401)

    if request.method == "POST":
        try:
            cart_item = CartItem.objects.get(id=item_id, cart__user=request.user)
            data = json.loads(request.body)
            quantity = int(data.get("quantity", 1))

            if quantity <= 0:
                cart_item.delete()
                message = "Item removed"
                item_total = 0
            else:
                if quantity > cart_item.product.stock:
                    return JsonResponse(
                        {
                            "success": False,
                            "error": f"Only {cart_item.product.stock} available",
                        },
                        status=400,
                    )

                cart_item.quantity = quantity
                cart_item.save()
                message = "Quantity updated"
                item_total = float(cart_item.total_price)

            cart = (
                cart_item.cart if quantity > 0 else Cart.objects.get(user=request.user)
            )

            return JsonResponse(
                {
                    "success": True,
                    "message": message,
                    "cart_count": cart.total_items,
                    "subtotal": float(cart.subtotal),
                    "item_total": item_total,
                }
            )

        except CartItem.DoesNotExist:
            return JsonResponse(
                {"success": False, "error": "Item not found"}, status=404
            )

    return JsonResponse({"success": False, "error": "Invalid request"}, status=400)


def remove_from_cart(request, item_id):
    """Remove item from cart"""
    if not request.user.is_authenticated:
        return JsonResponse({"success": False, "error": "Login required"}, status=401)

    if request.method == "POST":
        try:
            cart_item = CartItem.objects.get(id=item_id, cart__user=request.user)
            cart = cart_item.cart
            cart_item.delete()

            return JsonResponse(
                {
                    "success": True,
                    "message": "Item removed",
                    "cart_count": cart.total_items,
                    "subtotal": float(cart.subtotal),
                }
            )

        except CartItem.DoesNotExist:
            return JsonResponse(
                {"success": False, "error": "Item not found"}, status=404
            )

    return JsonResponse({"success": False, "error": "Invalid request"}, status=400)


def clear_cart(request):
    """Clear all items from cart"""
    if not request.user.is_authenticated:
        return JsonResponse({"success": False, "error": "Login required"}, status=401)

    if request.method == "POST":
        cart = Cart.objects.get(user=request.user)
        cart.items.all().delete()

        return JsonResponse(
            {"success": True, "message": "Cart cleared", "cart_count": 0}
        )

    return JsonResponse({"success": False, "error": "Invalid request"}, status=400)


from django.contrib.auth import authenticate, login


def login_view(request):
    """Login page - Complete functionality"""
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        remember = request.POST.get("remember")

        # Find user by email
        try:
            user = User.objects.get(email=email)
            username = user.username
        except User.DoesNotExist:
            messages.error(request, "No account found with this email!")
            return render(request, "buddybasket/login.html")

        # Authenticate
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            # Set session expiry based on remember me
            if not remember:
                request.session.set_expiry(0)  # Session expires when browser closes

            messages.success(
                request, f"Welcome back, {user.first_name or user.username}! 🎉"
            )
            return redirect("home")
        else:
            messages.error(request, "Invalid password!")

    return render(request, "buddybasket/login.html")


from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import render, redirect


def register_view(request):
    """Register page - Complete functionality"""
    if request.method == "POST":
        # Get form data
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")
        terms = request.POST.get("terms")

        # Validation
        errors = []

        if not terms:
            errors.append("You must agree to the Terms & Conditions")

        if password != confirm_password:
            errors.append("Passwords do not match")

        if len(password) < 6:
            errors.append("Password must be at least 6 characters long")

        if User.objects.filter(username=username).exists():
            errors.append("Username already taken")

        if User.objects.filter(email=email).exists():
            errors.append("Email already registered")

        if errors:
            for error in errors:
                messages.error(request, error)
            return render(request, "buddybasket/register.html")

        # Create user
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
        )

        # Success message and redirect
        messages.success(request, "Account created successfully! 🎉 Please login.")
        return redirect("login")

    # GET request - show registration form
    return render(request, "buddybasket/register.html")


def logout_view(request):
    """Logout user"""
    logout(request)
    messages.success(request, "Logged out successfully! 👋")
    return redirect("home")


def checkout_view(request):
    """Checkout page"""
    if not request.user.is_authenticated:
        return redirect("login")

    try:
        # Get the user's cart
        cart = Cart.objects.get(user=request.user)
        cart_items = cart.items.all()

        # Calculate totals
        subtotal = cart.subtotal
        shipping = 0 if subtotal >= 499 else 40
        total = subtotal + shipping

    except Cart.DoesNotExist:
        # If cart doesn't exist, show empty checkout
        cart_items = []
        subtotal = 0
        shipping = 40
        total = 0

    context = {
        "cart_items": cart_items,
        "subtotal": subtotal,
        "total": total,
    }
    return render(request, "buddybasket/checkout.html", context)


def order_confirmation(request):
    """Order confirmation page"""
    return render(request, "buddybasket/order_confirmation.html")


def get_or_create_wishlist(user):
    """Helper function to get or create wishlist"""
    wishlist, created = Wishlist.objects.get_or_create(user=user)
    return wishlist


def wishlist_view(request):
    """Wishlist page"""
    if not request.user.is_authenticated:
        return redirect("login")

    wishlist = get_or_create_wishlist(request.user)
    wishlist_items = wishlist.items.all().select_related("product__category")

    context = {
        "wishlist_items": wishlist_items,
        "total_items": wishlist.total_items,
    }
    return render(request, "buddybasket/wishlist.html", context)


def add_to_wishlist(request, product_id):
    """Add item to wishlist"""
    if not request.user.is_authenticated:
        return JsonResponse({"success": False, "error": "Login required"}, status=401)

    if request.method == "POST":
        try:
            product = Product.objects.get(id=product_id, is_active=True)
            wishlist = get_or_create_wishlist(request.user)

            # Check if item already in wishlist
            wishlist_item, created = WishlistItem.objects.get_or_create(
                wishlist=wishlist, product=product
            )

            return JsonResponse(
                {
                    "success": True,
                    "added": created,
                    "wishlist_count": wishlist.total_items,
                    "message": (
                        "Added to wishlist" if created else "Already in wishlist"
                    ),
                }
            )

        except Product.DoesNotExist:
            return JsonResponse(
                {"success": False, "error": "Product not found"}, status=404
            )

    return JsonResponse({"success": False, "error": "Invalid request"}, status=400)


def remove_from_wishlist(request, item_id):
    """Remove item from wishlist"""
    if not request.user.is_authenticated:
        return JsonResponse({"success": False, "error": "Login required"}, status=401)

    if request.method == "POST":
        try:
            wishlist_item = WishlistItem.objects.get(
                id=item_id, wishlist__user=request.user
            )
            wishlist = wishlist_item.wishlist
            wishlist_item.delete()

            return JsonResponse(
                {
                    "success": True,
                    "message": "Item removed",
                    "wishlist_count": wishlist.total_items,
                }
            )

        except WishlistItem.DoesNotExist:
            return JsonResponse(
                {"success": False, "error": "Item not found"}, status=404
            )

    return JsonResponse({"success": False, "error": "Invalid request"}, status=400)


def get_wishlist_item(request, product_id):
    """Get wishlist item ID by product ID"""
    if not request.user.is_authenticated:
        return JsonResponse({"success": False, "error": "Login required"}, status=401)

    try:
        wishlist = Wishlist.objects.get(user=request.user)
        wishlist_item = WishlistItem.objects.get(
            wishlist=wishlist, product_id=product_id
        )
        return JsonResponse({"success": True, "item_id": wishlist_item.id})
    except (Wishlist.DoesNotExist, WishlistItem.DoesNotExist):
        return JsonResponse({"success": False, "item_id": None})


def move_to_cart(request, item_id):
    """Move item from wishlist to cart"""
    if not request.user.is_authenticated:
        return JsonResponse({"success": False, "error": "Login required"}, status=401)

    if request.method == "POST":
        try:
            # Get wishlist item
            wishlist_item = WishlistItem.objects.get(
                id=item_id, wishlist__user=request.user
            )
            product = wishlist_item.product

            # Get or create cart
            cart, _ = Cart.objects.get_or_create(user=request.user)

            # Add to cart
            cart_item, created = CartItem.objects.get_or_create(
                cart=cart, product=product, defaults={"quantity": 1}
            )

            if not created:
                cart_item.quantity += 1
                cart_item.save()

            # Remove from wishlist
            wishlist = wishlist_item.wishlist
            wishlist_item.delete()

            return JsonResponse(
                {
                    "success": True,
                    "message": "Moved to cart",
                    "wishlist_count": wishlist.total_items,
                    "cart_count": cart.total_items,
                }
            )

        except WishlistItem.DoesNotExist:
            return JsonResponse(
                {"success": False, "error": "Item not found"}, status=404
            )

    return JsonResponse({"success": False, "error": "Invalid request"}, status=400)


def order_history(request):
    """Show all orders for logged in user"""
    if not request.user.is_authenticated:
        return redirect("login")

    orders = (
        Order.objects.filter(user=request.user)
        .prefetch_related("items__product")
        .order_by("-created_at")
    )

    context = {
        "orders": orders,
    }
    return render(request, "buddybasket/order_history.html", context)


def order_detail(request, order_id):
    """Show specific order details"""
    if not request.user.is_authenticated:
        return redirect("login")

    order = get_object_or_404(Order, id=order_id, user=request.user)

    context = {
        "order": order,
    }
    return render(request, "buddybasket/order_detail.html", context)


def create_order(request):
    """Create a new order from checkout data"""
    if not request.user.is_authenticated:
        return JsonResponse({"success": False, "error": "Login required"}, status=401)

    if request.method == "POST":
        try:
            data = json.loads(request.body)

            # Get user's cart
            cart = Cart.objects.get(user=request.user)

            # Calculate totals
            subtotal = cart.subtotal
            shipping = 0 if subtotal >= 499 else 40
            total = subtotal + shipping

            # Get or create shipping address
            shipping_address, _ = ShippingAddress.objects.get_or_create(
                user=request.user,
                defaults={
                    "full_name": f"{data.get('first_name')} {data.get('last_name')}",
                    "phone": data.get("phone"),
                    "address_line1": data.get("address_line1"),
                    "address_line2": data.get("address_line2", ""),
                    "city": data.get("city"),
                    "state": data.get("state"),
                    "postal_code": data.get("pincode"),
                    "is_default": True,
                },
            )

            # Determine payment status based on payment method
            payment_method = data.get("payment_method", "cod")
            payment_status = "paid" if payment_method == "razorpay" else "pending"

            # Create order
            order = Order.objects.create(
                user=request.user,
                shipping_address=shipping_address,
                subtotal=subtotal,
                shipping_cost=shipping,
                tax=0,
                total=total,
                payment_method=payment_method,
                status="pending",
                payment_status=payment_status,
                # Add Razorpay fields if they exist
                razorpay_order_id=data.get("razorpay_order_id", ""),
                razorpay_payment_id=data.get("razorpay_payment_id", ""),
                razorpay_signature=data.get("razorpay_signature", ""),
            )

            # Create order items from cart
            for cart_item in cart.items.all():
                OrderItem.objects.create(
                    order=order,
                    product=cart_item.product,
                    product_name=cart_item.product.name,
                    product_price=cart_item.product.price,
                    quantity=cart_item.quantity,
                )

            # Clear the cart
            cart.items.all().delete()

            return JsonResponse(
                {
                    "success": True,
                    "order_id": order.id,
                    "order_number": order.order_number,
                }
            )

        except Cart.DoesNotExist:
            return JsonResponse(
                {"success": False, "error": "Cart not found"}, status=404
            )
        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)}, status=500)

    return JsonResponse({"success": False, "error": "Invalid request"}, status=400)


def get_order(request, order_id):
    """Get order details for confirmation page"""
    if not request.user.is_authenticated:
        return JsonResponse({"success": False, "error": "Login required"}, status=401)

    try:
        order = Order.objects.get(id=order_id, user=request.user)

        order_data = {
            "order_number": order.order_number,
            "created_at": order.created_at.isoformat(),
            "subtotal": float(order.subtotal),
            "shipping": float(order.shipping_cost),
            "total": float(order.total),
            "payment_method": order.payment_method,
            "status": order.status,
            "shipping_address": {
                "full_name": order.shipping_address.full_name,
                "address_line1": order.shipping_address.address_line1,
                "address_line2": order.shipping_address.address_line2,
                "city": order.shipping_address.city,
                "state": order.shipping_address.state,
                "postal_code": order.shipping_address.postal_code,
                "phone": order.shipping_address.phone,
            },
        }

        return JsonResponse({"success": True, "order": order_data})

    except Order.DoesNotExist:
        return JsonResponse({"success": False, "error": "Order not found"}, status=404)


@login_required
def create_razorpay_order(request):
    """Create a Razorpay order for checkout"""
    if request.method == "POST":
        try:
            # Get user's cart and calculate total
            cart = Cart.objects.get(user=request.user)
            total_amount = int(cart.subtotal * 100)  # Convert to paise

            # Initialize Razorpay client
            client = razorpay.Client(
                auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET)
            )

            # Create order
            razorpay_order = client.order.create(
                {
                    "amount": total_amount,
                    "currency": settings.RAZORPAY_CURRENCY,
                    "payment_capture": 1,  # Auto capture payment
                }
            )

            # Store order details in session for verification
            request.session["razorpay_order_id"] = razorpay_order["id"]
            request.session["razorpay_amount"] = total_amount

            return JsonResponse(
                {
                    "success": True,
                    "razorpay_key_id": settings.RAZORPAY_KEY_ID,
                    "razorpay_order_id": razorpay_order["id"],
                    "amount": total_amount,
                    "currency": settings.RAZORPAY_CURRENCY,
                    "user_name": request.user.get_full_name() or request.user.username,
                    "user_email": request.user.email,
                    "user_contact": "",  # You can get this from user profile
                }
            )

        except Cart.DoesNotExist:
            return JsonResponse(
                {"success": False, "error": "Cart not found"}, status=404
            )
        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)}, status=500)

    return JsonResponse({"success": False, "error": "Invalid request"}, status=400)


@csrf_exempt
def razorpay_callback(request):
    """Handle Razorpay payment callback"""
    if request.method != "POST":
        return redirect("checkout")

    # Get session data
    session_data = request.session.get("razorpay_order_id")
    if not session_data:
        messages.error(request, "Session expired. Please try again.")
        return redirect("checkout")

    # Get payment details from Razorpay POST data [citation:1]
    razorpay_payment_id = request.POST.get("razorpay_payment_id")
    razorpay_order_id = request.POST.get("razorpay_order_id")
    razorpay_signature = request.POST.get("razorpay_signature")

    # Verify the order ID matches session
    if razorpay_order_id != request.session.get("razorpay_order_id"):
        messages.error(request, "Payment verification failed (order mismatch).")
        return redirect("checkout")

    # Initialize Razorpay client
    client = razorpay.Client(
        auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET)
    )

    # Verify payment signature [citation:1][citation:7]
    params_dict = {
        "razorpay_order_id": razorpay_order_id,
        "razorpay_payment_id": razorpay_payment_id,
        "razorpay_signature": razorpay_signature,
    }

    try:
        # Verify signature
        client.utility.verify_payment_signature(params_dict)

        # Get user's cart
        cart = Cart.objects.get(user=request.user)

        # Get shipping address (you may need to get this from session)
        # For now, get the default shipping address
        shipping_address = ShippingAddress.objects.filter(
            user=request.user, is_default=True
        ).first()

        # Create order
        order = Order.objects.create(
            user=request.user,
            shipping_address=shipping_address,
            subtotal=cart.subtotal,
            shipping_cost=0 if cart.subtotal >= 499 else 40,
            tax=0,
            total=cart.subtotal + (0 if cart.subtotal >= 499 else 40),
            payment_method="Razorpay",
            payment_status="paid",
            razorpay_order_id=razorpay_order_id,
            razorpay_payment_id=razorpay_payment_id,
            razorpay_signature=razorpay_signature,
        )

        # Create order items
        for cart_item in cart.items.all():
            OrderItem.objects.create(
                order=order,
                product=cart_item.product,
                product_name=cart_item.product.name,
                product_price=cart_item.product.price,
                quantity=cart_item.quantity,
            )

        # Clear the cart
        cart.items.all().delete()

        # Clear session data
        request.session.pop("razorpay_order_id", None)
        request.session.pop("razorpay_amount", None)

        messages.success(
            request, f"Payment successful! Order #{order.order_number} has been placed."
        )
        return redirect("order_confirmation", order_id=order.id)

    except razorpay.errors.SignatureVerificationError:
        messages.error(request, "Payment verification failed. Please contact support.")
        return redirect("checkout")
    except Exception as e:
        messages.error(request, f"An error occurred: {str(e)}")
        return redirect("checkout")
