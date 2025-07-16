from django.contrib import admin

from django.contrib import admin
from .models import User, Category, Brand, Instrument, Offer, Order, Delivery, Review, Payment, Wishlist, Notification

admin.site.register(User)
admin.site.register(Category)
admin.site.register(Brand)
admin.site.register(Instrument)
admin.site.register(Offer)
admin.site.register(Order)
admin.site.register(Delivery)
admin.site.register(Review)
admin.site.register(Payment)
admin.site.register(Wishlist)
admin.site.register(Notification)

