<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Order Confirmed - Gainz Tracker</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&display=swap" rel="stylesheet">
    <style>


        .success-icon {
            animation: checkmark 0.8s ease-in-out 0.3s both;
        }

        @keyframes checkmark {
            0% {
                transform: scale(0) rotate(45deg);
                opacity: 0;
            }
            50% {
                transform: scale(1.2) rotate(45deg);
                opacity: 1;
            }
            100% {
                transform: scale(1) rotate(45deg);
                opacity: 1;
            }
        }

        .fade-in-up {
            animation: fadeInUp 0.8s ease-out both;
        }

        .fade-in-up.delay-200 {
            animation-delay: 0.2s;
        }

        .fade-in-up.delay-400 {
            animation-delay: 0.4s;
        }

        .fade-in-up.delay-600 {
            animation-delay: 0.6s;
        }

        @keyframes fadeInUp {
            from {
                opacity: 0;
                transform: translateY(30px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }

        .order-card {
            background: rgba(255, 255, 255, 0.05);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(0, 221, 135, 0.3);
        }

        .pulse-glow {
            animation: pulseGlow 2s ease-in-out infinite;
        }

        @keyframes pulseGlow {
            0%, 100% {
                box-shadow: 0 0 20px rgba(0, 221, 135, 0.3);
            }
            50% {
                box-shadow: 0 0 40px rgba(0, 221, 135, 0.5);
            }
        }
    </style>
</head>
<body class="bg-gray-900 text-white">
<div class="heroback py-8 w-full mx-auto">
    <!-- Success Icon and Main Message -->
    <div class="container mx-auto px-4 text-center pt-16">
        <div class="success-icon w-24 h-24 mx-auto mb-8">
            <div class="w-24 h-24 rounded-full bg-[#00dd87] flex items-center justify-center pulse-glow">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-12 w-12 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="3">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M5 13l4 4L19 7" />
                </svg>
            </div>
        </div>

        <h1 class="text-5xl md:text-6xl font-orbital font-bold text-[#00dd87] mb-4 fade-in-up">
            Order Confirmed!
        </h1>

        <p class="text-xl md:text-2xl text-white mb-2 fade-in-up delay-200">
            Your personalized nutrition plan is on its way
        </p>

        <p class="text-lg text-gray-300 mb-8 fade-in-up delay-400">
            Thank you for choosing <a class="text-gradient-2 font-bold" href="/">Gainz Tracker</a> to fuel your fitness journey!
        </p>
    </div>

    <!-- Order Details Card -->
    <div class="container mx-auto px-4 max-w-2xl mb-12 fade-in-up delay-600">
        <div class="order-card rounded-lg p-8">
            <h2 class="text-2xl font-orbital font-bold text-[#00dd87] mb-6 text-center">Order Details (Coming soon - visit instacart for details)</h2>

<!--            <div class="space-y-4">-->
<!--                <div class="flex justify-between items-center py-3 border-b border-gray-700">-->
<!--                    <span class="text-gray-300">Order Number:</span>-->
<!--                    <span class="font-bold text-white">#GT-2025-001234</span>-->
<!--                </div>-->

<!--                <div class="flex justify-between items-center py-3 border-b border-gray-700">-->
<!--                    <span class="text-gray-300">Delivery Date:</span>-->
<!--                    <span class="font-bold text-[#00dd87]">Tomorrow, 2-4 PM</span>-->
<!--                </div>-->

<!--                <div class="flex justify-between items-center py-3 border-b border-gray-700">-->
<!--                    <span class="text-gray-300">Items:</span>-->
<!--                    <span class="font-bold text-white">5 Recipes + Ingredients</span>-->
<!--                </div>-->

<!--                <div class="flex justify-between items-center py-3 border-b border-gray-700">-->
<!--                    <span class="text-gray-300">Total:</span>-->
<!--                    <span class="font-bold text-[#00dd87] text-xl">$47.99</span>-->
<!--                </div>-->

<!--                <div class="flex justify-between items-center py-3">-->
<!--                    <span class="text-gray-300">Delivery Address:</span>-->
<!--                    <span class="font-bold text-white text-right">-->
<!--                            123 Fitness Lane<br>-->
<!--                            Health City, HC 12345-->
<!--                        </span>-->
<!--                </div>-->
<!--            </div>-->
        </div>
    </div>

    <!-- What's Next Section -->
    <div class="container mx-auto px-4 max-w-4xl mb-12">
        <h2 class="text-3xl font-orbital font-bold text-center text-white mb-8 fade-in-up">
            What's Next?
        </h2>

        <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div class="bg-gray-800 p-6 rounded-lg shadow-lg text-center fade-in-up">
                <div class="w-16 h-16 rounded-full bg-[#00dd8733] flex items-center justify-center mb-4 mx-auto">
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-8 w-8 text-[#00dd87]" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                    </svg>
                </div>
                <h3 class="text-xl font-bold text-[#00dd87] mb-2">Track Your Order</h3>
                <p class="text-gray-300">
                    We'll send you real-time updates about your delivery status via email and SMS.
                </p>
            </div>

            <div class="bg-gray-800 p-6 rounded-lg shadow-lg text-center fade-in-up delay-200">
                <div class="w-16 h-16 rounded-full bg-[#00dd8733] flex items-center justify-center mb-4 mx-auto">
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-8 w-8 text-[#00dd87]" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                    </svg>
                </div>
                <h3 class="text-xl font-bold text-[#00dd87] mb-2">Recipe Instructions</h3>
                <p class="text-gray-300">
                    Access your personalized recipes and cooking instructions in your dashboard.
                </p>
            </div>

            <div class="bg-gray-800 p-6 rounded-lg shadow-lg text-center fade-in-up delay-400">
                <div class="w-16 h-16 rounded-full bg-[#00dd8733] flex items-center justify-center mb-4 mx-auto">
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-8 w-8 text-[#00dd87]" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
                    </svg>
                </div>
                <h3 class="text-xl font-bold text-[#00dd87] mb-2">Join Community</h3>
                <p class="text-gray-300">
                    Share your cooking experience and connect with other fitness enthusiasts.
                </p>
            </div>
        </div>
    </div>

    <!-- Action Buttons -->
    <div class="container mx-auto px-4 text-center mb-12 fade-in-up delay-600">
        <div class="flex flex-col sm:flex-row gap-4 justify-center items-center">
            <a href="https://www.instacart.com/" target='_blank' class="bg-[#00dd87] hover:bg-[#00bb74] text-black font-bold py-3 px-8 rounded-full transition-all w-full sm:w-auto">
                View Order Status
            </a>

            <a href='/shopping-list' class="border-2 border-[#00dd87] text-[#00dd87] hover:bg-[#00dd87] hover:text-black font-bold py-3 px-8 rounded-full transition-all w-full sm:w-auto">
                Continue Shopping
            </a>

            <button class="bg-transparent border-2 border-gray-600 text-gray-300 hover:border-gray-400 hover:text-white font-bold py-3 px-8 rounded-full transition-all w-full sm:w-auto">
                Download Receipt
            </button>
        </div>
    </div>

    <!-- Contact Support -->
    <div class="container mx-auto px-4 text-center mb-8 fade-in-up delay-600">
        <div class="bg-gray-800 p-6 rounded-lg max-w-2xl mx-auto">
            <h3 class="text-xl font-bold text-[#00dd87] mb-3">Need Help?</h3>
            <p class="text-gray-300 mb-4">
                Our customer support team is here to help with any questions about your order.
            </p>
            <div class="flex flex-col sm:flex-row gap-4 justify-center">
                <a href="mailto:info@gainztracker.com" class="text-[#00dd87] hover:underline flex items-center justify-center gap-2">
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 8l7.89 4.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
                    </svg>
                    info@gainztracker.com
                </a>
                <a href="tel:763-742-3162" class="text-[#00dd87] hover:underline flex items-center justify-center gap-2">
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z" />
                    </svg>
                    763-742-3162
                </a>
            </div>
        </div>
    </div>
</div>

<script>
    // Add some interactive elements
    document.addEventListener('DOMContentLoaded', function() {
        // Animate elements on page load
        const elements = document.querySelectorAll('.fade-in-up');
        elements.forEach((el, index) => {
            setTimeout(() => {
                el.style.opacity = '1';
                el.style.transform = 'translateY(0)';
            }, index * 200);
        });

        // Add click handlers for buttons (you would replace these with actual functionality)
        document.querySelector('button:contains("View Order Status")')?.addEventListener('click', function() {
            alert('Redirecting to order tracking...');
        });

        document.querySelector('button:contains("Continue Shopping")')?.addEventListener('click', function() {
            window.location.href = '/nutrition'; // or wherever your main shopping page is
        });

        document.querySelector('button:contains("Download Receipt")')?.addEventListener('click', function() {
            alert('Receipt download starting...');
        });
    });
</script>
</body>
</html>