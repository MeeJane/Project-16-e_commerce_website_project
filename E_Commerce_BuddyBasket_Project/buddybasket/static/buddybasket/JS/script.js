// BuddyBasket Custom JavaScript

// Function to show login alert when clicking on orders/cart
function showLoginAlert(event) {
    event.preventDefault();
    alert('😊 Please login or sign up to view orders and cart!');
    // Optional: Redirect to login page later
    // window.location.href = "/login/";
}

// Search bar smooth transition
document.addEventListener('DOMContentLoaded', function () {
    const searchInput = document.querySelector('.search-input-compact');
    if (searchInput) {
        searchInput.addEventListener('focus', function () {
            this.style.width = '250px';
        });
        searchInput.addEventListener('blur', function () {
            this.style.width = '200px';
        });
    }
});

// Optional: Add active class to current nav link
document.addEventListener('DOMContentLoaded', function () {
    const currentLocation = window.location.pathname;
    const navLinks = document.querySelectorAll('.nav-link');

    navLinks.forEach(link => {
        const linkPath = link.getAttribute('href');
        if (linkPath === currentLocation ||
            (currentLocation === '/' && linkPath === '/')) {
            link.classList.add('active');
        }
    });
});

// Optional: Cart badge update function (for later use)
function updateCartBadge(count) {
    const cartBadge = document.querySelector('.cart-badge');
    if (cartBadge) {
        if (count > 0) {
            cartBadge.style.display = 'inline';
            cartBadge.textContent = count;
        } else {
            cartBadge.style.display = 'none';
        }
    }
}

// Optional: Smooth scroll for anchor links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    });
});

// Countdown Timer for Big Day News
function startCountdown(days = 2, hours = 12, minutes = 30, seconds = 0) {
    const countdownDate = new Date();
    countdownDate.setDate(countdownDate.getDate() + days);
    countdownDate.setHours(countdownDate.getHours() + hours);
    countdownDate.setMinutes(countdownDate.getMinutes() + minutes);
    countdownDate.setSeconds(countdownDate.getSeconds() + seconds);

    const timer = setInterval(function () {
        const now = new Date().getTime();
        const distance = countdownDate - now;

        const days = Math.floor(distance / (1000 * 60 * 60 * 24));
        const hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
        const minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
        const seconds = Math.floor((distance % (1000 * 60)) / 1000);

        document.querySelector('.timer-box.days').textContent = String(days).padStart(2, '0');
        document.querySelector('.timer-box.hours').textContent = String(hours).padStart(2, '0');
        document.querySelector('.timer-box.minutes').textContent = String(minutes).padStart(2, '0');
        document.querySelector('.timer-box.seconds').textContent = String(seconds).padStart(2, '0');

        if (distance < 0) {
            clearInterval(timer);
            document.querySelector('.countdown-timer').innerHTML = '<span class="badge bg-danger">Offer Expired!</span>';
        }
    }, 1000);
}

// Start the countdown when page loads
document.addEventListener('DOMContentLoaded', function () {
    if (document.querySelector('.countdown-timer')) {
        startCountdown(2, 12, 30, 0); // 2 days, 12 hours, 30 minutes
    }
});

// Counter Animation for Stats
function animateCounter() {
    const counters = document.querySelectorAll('.stat-number');

    counters.forEach(counter => {
        const target = parseInt(counter.getAttribute('data-count'));
        let current = 0;
        const increment = target / 50; // Divide into 50 steps
        const timer = setInterval(() => {
            current += increment;
            if (current >= target) {
                counter.textContent = target;
                clearInterval(timer);
            } else {
                counter.textContent = Math.floor(current);
            }
        }, 30);
    });
}

// Start counter when slide becomes active
document.addEventListener('DOMContentLoaded', function () {
    // Check if first slide is active
    const firstSlide = document.querySelector('.carousel-item.active');
    if (firstSlide && firstSlide.querySelector('.stat-number')) {
        animateCounter();
    }

    // Listen for slide change
    const carousel = document.getElementById('heroCarousel');
    if (carousel) {
        carousel.addEventListener('slid.bs.carousel', function (event) {
            if (event.to === 0) { // First slide index
                setTimeout(animateCounter, 500); // Wait for animation
            }
        });
    }
});

// Update FAB badges
function updateFABBadges() {
    const cartBadge = document.getElementById('cartBadge');
    const wishlistBadge = document.getElementById('wishlistBadge');
    const ordersBadge = document.getElementById('ordersBadge');

    const fabCartBadge = document.getElementById('fabCartBadge');
    const fabWishlistBadge = document.getElementById('fabWishlistBadge');
    const fabOrdersBadge = document.getElementById('fabOrdersBadge');

    if (fabCartBadge && cartBadge) {
        fabCartBadge.textContent = cartBadge.textContent;
        fabCartBadge.style.display = cartBadge.style.display;
    }

    if (fabWishlistBadge && wishlistBadge) {
        fabWishlistBadge.textContent = wishlistBadge.textContent;
        fabWishlistBadge.style.display = wishlistBadge.style.display;
    }

    if (fabOrdersBadge && ordersBadge) {
        fabOrdersBadge.textContent = ordersBadge.textContent;
        fabOrdersBadge.style.display = ordersBadge.style.display;
    }
}

// Call on page load and whenever badges update
document.addEventListener('DOMContentLoaded', updateFABBadges);

// Countdown Timer for Big Day Sale
function startSaleCountdown() {
    // Set the date we're counting down to (2 days from now)
    const countDownDate = new Date();
    countDownDate.setDate(countDownDate.getDate() + 2);
    countDownDate.setHours(23, 59, 59, 999);

    const timer = setInterval(function () {
        const now = new Date().getTime();
        const distance = countDownDate - now;

        // Time calculations
        const days = Math.floor(distance / (1000 * 60 * 60 * 24));
        const hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
        const minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
        const seconds = Math.floor((distance % (1000 * 60)) / 1000);

        // Display the result
        document.getElementById("days").innerHTML = String(days).padStart(2, '0');
        document.getElementById("hours").innerHTML = String(hours).padStart(2, '0');
        document.getElementById("minutes").innerHTML = String(minutes).padStart(2, '0');
        document.getElementById("seconds").innerHTML = String(seconds).padStart(2, '0');

        // If the countdown is over
        if (distance < 0) {
            clearInterval(timer);
            document.querySelector('.countdown-wrapper').innerHTML = '<h3 class="text-white">Sale Ended!</h3>';
        }
    }, 1000);
}

// Start timer when page loads
document.addEventListener('DOMContentLoaded', function () {
    if (document.getElementById('days')) {
        startSaleCountdown();
    }
});


// ====== Shopping Cart Functionality ======

// Cart data (in real app, this would come from backend)
let cartItems = [];
let wishlistItems = [];

// Update quantity and total price
function incrementQuantity(btn) {
    const selector = btn.closest('.quantity-selector');
    const input = selector.querySelector('.qty-input');
    const currentVal = parseInt(input.value);
    const max = parseInt(input.getAttribute('max'));

    if (currentVal < max) {
        input.value = currentVal + 1;
        updateTotalPrice(selector);
    }
}

function decrementQuantity(btn) {
    const selector = btn.closest('.quantity-selector');
    const input = selector.querySelector('.qty-input');
    const currentVal = parseInt(input.value);

    if (currentVal > 1) {
        input.value = currentVal - 1;
        updateTotalPrice(selector);
    }
}

function updateTotalPrice(selector) {
    const productCard = selector.closest('.product-card');
    const priceElement = productCard.querySelector('.current-price');
    const price = parseFloat(priceElement.textContent.replace('₹', '').replace(',', ''));
    const quantity = parseInt(selector.querySelector('.qty-input').value);
    const totalElement = productCard.querySelector('.total-value');

    totalElement.textContent = '₹' + (price * quantity).toLocaleString('en-IN');
}

// Add to cart
function addToCart(productId) {
    showLoginAlert(event, 'cart');
    // In real app, you'd send to backend
    updateCartBadge(3); // Example
}

// Buy now
function buyNow(productId) {
    showLoginAlert(event, 'cart');
}

// Initialize favorite buttons on page load
document.addEventListener('DOMContentLoaded', function () {
    // Check each product card's data-wishlisted attribute and set the button accordingly
    document.querySelectorAll('.product-card').forEach(card => {
        const isWishlisted = card.dataset.wishlisted === 'true';
        const favBtn = card.querySelector('.favorite-btn');
        const heartIcon = favBtn ? favBtn.querySelector('i') : null;

        if (isWishlisted && favBtn && heartIcon) {
            favBtn.classList.add('active');
            heartIcon.classList.remove('far');
            heartIcon.classList.add('fas');
        }
    });
});

function toggleFavorite(btn, productId) {
    const loginStatus = document.getElementById('user-login-status');
    const isLoggedIn = loginStatus && loginStatus.dataset.loggedIn === 'true';

    if (!isLoggedIn) {
        window.location.href = '/login/?next=' + window.location.pathname;
        return;
    }

    // Check if already active (in wishlist)
    const isActive = btn.classList.contains('active');

    fetch(`/add-to-wishlist/${productId}/`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': getCookie('csrftoken'),
            'Content-Type': 'application/json',
        },
    })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                if (data.added) {
                    // Item was added to wishlist
                    btn.classList.add('active');
                    btn.querySelector('i').classList.remove('far');
                    btn.querySelector('i').classList.add('fas');
                    showNotification('❤️ Added to wishlist!');

                    // Update wishlist badge
                    const wishlistBadge = document.getElementById('wishlistBadge');
                    if (wishlistBadge) {
                        wishlistBadge.textContent = data.wishlist_count;
                        wishlistBadge.style.display = 'flex';
                    }

                    // Update FAB badge if exists
                    const fabWishlistBadge = document.getElementById('fabWishlistBadge');
                    if (fabWishlistBadge) {
                        fabWishlistBadge.textContent = data.wishlist_count;
                    }
                } else {
                    // Already in wishlist - ask to remove
                    if (confirm('Remove from wishlist?')) {
                        // Get the wishlist item ID first
                        fetch(`/get-wishlist-item/${productId}/`, {
                            method: 'GET',
                            headers: {
                                'X-CSRFToken': getCookie('csrftoken'),
                            },
                        })
                            .then(res => res.json())
                            .then(itemData => {
                                if (itemData.success && itemData.item_id) {
                                    // Now remove it using the item ID
                                    fetch(`/remove-from-wishlist/${itemData.item_id}/`, {
                                        method: 'POST',
                                        headers: {
                                            'X-CSRFToken': getCookie('csrftoken'),
                                        },
                                    })
                                        .then(res => res.json())
                                        .then(removeData => {
                                            if (removeData.success) {
                                                btn.classList.remove('active');
                                                btn.querySelector('i').classList.remove('fas');
                                                btn.querySelector('i').classList.add('far');
                                                showNotification('Removed from wishlist');

                                                // Update badges
                                                const wishlistBadge = document.getElementById('wishlistBadge');
                                                if (wishlistBadge) {
                                                    wishlistBadge.textContent = removeData.wishlist_count;
                                                    if (removeData.wishlist_count === 0) {
                                                        wishlistBadge.style.display = 'none';
                                                    }
                                                }

                                                // Update FAB badge
                                                const fabWishlistBadge = document.getElementById('fabWishlistBadge');
                                                if (fabWishlistBadge) {
                                                    fabWishlistBadge.textContent = removeData.wishlist_count;
                                                }
                                            }
                                        });
                                }
                            });
                    }
                }
            }
        })
        .catch(error => {
            console.error('Error:', error);
            showNotification('❌ Something went wrong');
        });
}

// Update badges
function updateCartBadge(count) {
    const badge = document.getElementById('cartBadge');
    if (count > 0) {
        badge.textContent = count;
        badge.style.display = 'flex';
    } else {
        badge.style.display = 'none';
    }
}

function updateWishlistBadge(count) {
    const badge = document.getElementById('wishlistBadge');
    if (count > 0) {
        badge.textContent = count;
        badge.style.display = 'flex';
    } else {
        badge.style.display = 'none';
    }
}

function updateOrdersBadge(count) {
    const badge = document.getElementById('ordersBadge');
    if (count > 0) {
        badge.textContent = count;
        badge.style.display = 'flex';
    } else {
        badge.style.display = 'none';
    }
}

// Show login alert with context
function showLoginAlert(event, feature) {
    event.preventDefault();

    let message = '';
    switch (feature) {
        case 'cart':
            message = '😊 Please login to add items to cart!';
            break;
        case 'wishlist':
            message = '😊 Please login to save items to wishlist!';
            break;
        case 'orders':
            message = '😊 Please login to view your orders!';
            break;
        case 'payment':
            message = '😊 Please login to make payments!';
            break;
        default:
            message = '😊 Please login to continue!';
    }

    alert(message);
}

// // Initialize on page load
// document.addEventListener('DOMContentLoaded', function () {
//     // Set initial badge values (example)
//     updateCartBadge(3);
//     updateWishlistBadge(0);
//     updateOrdersBadge(2);
// });

// Countdown Timer for Big Day Sale
function startSaleCountdown() {
    // Set the date we're counting down to (2 days from now)
    const countDownDate = new Date();
    countDownDate.setDate(countDownDate.getDate() + 2);
    countDownDate.setHours(23, 59, 59, 999);

    const timer = setInterval(function () {
        const now = new Date().getTime();
        const distance = countDownDate - now;

        // Time calculations
        const days = Math.floor(distance / (1000 * 60 * 60 * 24));
        const hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
        const minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
        const seconds = Math.floor((distance % (1000 * 60)) / 1000);

        // Display the result
        document.getElementById("days").innerHTML = String(days).padStart(2, '0');
        document.getElementById("hours").innerHTML = String(hours).padStart(2, '0');
        document.getElementById("minutes").innerHTML = String(minutes).padStart(2, '0');
        document.getElementById("seconds").innerHTML = String(seconds).padStart(2, '0');

        // If the countdown is over
        if (distance < 0) {
            clearInterval(timer);
            document.querySelector('.countdown-wrapper').innerHTML = '<h3 class="text-white">Sale Ended!</h3>';
        }
    }, 1000);
}

// Start timer when page loads
document.addEventListener('DOMContentLoaded', function () {
    if (document.getElementById('days')) {
        startSaleCountdown();
    }
});


// Add to cart from product detail page
// Check if user is logged in
function isUserLoggedIn() {
    // Check for user-specific elements
    const userDropdown = document.querySelector('.dropdown .nav-link i.fa-user-circle');
    const cartBadge = document.getElementById('cartBadge');

    // If cart badge is visible and user icon exists, assume logged in
    return (userDropdown !== null && cartBadge && cartBadge.style.display !== 'none');
}

// Add to cart from product detail page
// Add to cart from product detail page
function addToCartFromDetail(productId) {
    const loginStatus = document.getElementById('user-login-status');
    const isLoggedIn = loginStatus && loginStatus.dataset.loggedIn === 'true';

    if (isLoggedIn) {
        fetch(`/add-to-cart/${productId}/`, {
            method: 'POST',
            headers: {
                'X-CSRFToken': getCookie('csrftoken'),
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ quantity: 1 })
        })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    showNotification('✅ Added to cart!');

                    // Update cart badge
                    const cartBadge = document.getElementById('cartBadge');
                    if (cartBadge) {
                        cartBadge.textContent = data.cart_count;
                        cartBadge.style.display = 'flex';
                    }

                    // Redirect to cart page
                    setTimeout(() => {
                        window.location.href = '/cart/';
                    }, 1000);
                } else {
                    showNotification('❌ ' + data.error);
                }
            })
            .catch(error => {
                console.error('Error:', error);
                showNotification('❌ Something went wrong');
            });
    } else {
        window.location.href = '/login/?next=' + window.location.pathname;
    }
}

// Helper function to get CSRF token
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// Show notification function (add this if you don't have it)
function showNotification(message) {
    // Check if notification already exists
    const existingNotification = document.querySelector('.notification-popup');
    if (existingNotification) {
        existingNotification.remove();
    }

    // Create notification element
    const notification = document.createElement('div');
    notification.className = 'notification-popup';
    notification.style.position = 'fixed';
    notification.style.top = '20px';
    notification.style.left = '50%';
    notification.style.transform = 'translateX(-50%)';
    notification.style.backgroundColor = 'var(--primary)';
    notification.style.color = 'white';
    notification.style.padding = '12px 25px';
    notification.style.borderRadius = '50px';
    notification.style.boxShadow = '0 5px 15px rgba(255,107,74,0.3)';
    notification.style.zIndex = '9999';
    notification.style.fontWeight = '500';
    notification.style.animation = 'slideDown 0.3s ease';
    notification.style.border = '2px solid rgba(255,255,255,0.3)';
    notification.innerHTML = message;

    document.body.appendChild(notification);

    // Remove after 2 seconds
    setTimeout(() => {
        notification.style.animation = 'slideUp 0.3s ease';
        setTimeout(() => {
            notification.remove();
        }, 300);
    }, 2000);
}

// Add animation styles if not present
if (!document.querySelector('#notification-styles')) {
    const style = document.createElement('style');
    style.id = 'notification-styles';
    style.textContent = `
        @keyframes slideDown {
            from {
                opacity: 0;
                transform: translate(-50%, -20px);
            }
            to {
                opacity: 1;
                transform: translate(-50%, 0);
            }
        }
        @keyframes slideUp {
            from {
                opacity: 1;
                transform: translate(-50%, 0);
            }
            to {
                opacity: 0;
                transform: translate(-50%, -20px);
            }
        }
    `;
    document.head.appendChild(style);
}


// Handle protected icon clicks (wishlist, orders, payment)
// Handle protected icon clicks (orders, payment only - wishlist now has direct link)
function handleProtectedClick(event, feature) {
    event.preventDefault();

    const loginStatus = document.getElementById('user-login-status');
    const isLoggedIn = loginStatus && loginStatus.dataset.loggedIn === 'true';

    if (isLoggedIn) {
        switch (feature) {
            case 'orders':
                window.location.href = '/orders/'; // Create this page later
                break;
            case 'payment':
                window.location.href = '/payment-methods/'; // Create this page later
                break;
            default:
                console.log('Feature:', feature);
        }
        alert(`✅ ${feature} page will be implemented soon!`);
    } else {
        window.location.href = '/login/?next=' + window.location.pathname;
    }
}