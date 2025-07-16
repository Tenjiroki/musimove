from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings



# 1. Користувач (User)
class User(AbstractUser):
    email = models.EmailField(unique=True)

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='musimi_user_groups',
        blank=True,
        help_text='The groups this user belongs to.'
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='musimi_user_permissions',
        blank=True,
        help_text='Specific permissions for this user.'
    )


# 2. Категорія (Category)
class Category(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


# 3. Бренд (Brand)
class Brand(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    year_founded = models.IntegerField(null=True, blank=True)
    description = models.TextField(blank=True)
    rating = models.FloatField(default=0)

    def __str__(self):
        return self.name


# 4. Інструмент (Instrument)
class Instrument(models.Model):
    id = models.AutoField(primary_key=True)
    code = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    brand = models.ForeignKey(Brand, on_delete=models.SET_NULL, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.code} - {self.name}"


# 5. Офери (Offer)
class Offer(models.Model):
    STATUS_CHOICES = [
        ('available', 'Available'),
        ('booked', 'Booked'),
        ('sold', 'Sold'),
    ]

    id = models.AutoField(primary_key=True)
    instrument = models.ForeignKey(Instrument, on_delete=models.CASCADE)
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='offers')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(
        max_length=50,
        choices=STATUS_CHOICES,
        default='available'
    )

    class Meta:
        indexes = [
            models.Index(fields=['instrument']),
            models.Index(fields=['seller']),
            models.Index(fields=['status']),
        ]
        ordering = ['-status', 'price']  # Спочатку доступні, потім сортування за ціною

    def __str__(self):
        return f"Offer #{self.id}: {self.instrument.name} - {self.price} грн (Status: {self.status})"

    def clean(self):
        """Ensure that price is not negative."""
        if self.price < 0:
            raise ValidationError("Price cannot be negative.")
        super().clean()

# 6. Замовлення (Order)
class Order(models.Model):
    id = models.AutoField(primary_key=True)
    offer = models.ForeignKey(Offer, on_delete=models.CASCADE)
    buyer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sales')
    status = models.CharField(max_length=50, choices=[('processing', 'Processing'), ('shipped', 'Shipped'), ('delivered', 'Delivered')], default='processing')
    order_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.id}"




# 7. Доставка (Delivery)
class Delivery(models.Model):
    id = models.AutoField(primary_key=True)
    order = models.OneToOneField('Order', on_delete=models.CASCADE, related_name='delivery')
    status = models.CharField(
        max_length=50,
        choices=[
            ('pending', 'Pending'),
            ('in_transit', 'In Transit'),
            ('delivered', 'Delivered')
        ],
        default='pending'
    )
    delivery_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Delivery #{self.id} for Order #{self.order.id}"



# 8. Відгуки (Review)
class Review(models.Model):
    id = models.AutoField(primary_key=True)
    order = models.OneToOneField('Order', on_delete=models.CASCADE, related_name='review')
    reviewer = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE,
        related_name='given_reviews'
    )
    reviewed_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='received_reviews'
    )
    rating = models.PositiveIntegerField(default=5)
    comment = models.TextField(blank=True)
    review_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review #{self.id} by {self.reviewer.username} for Order #{self.order.id}"


# 9. Оплата (Payment)
class Payment(models.Model):
    id = models.AutoField(primary_key=True)
    order = models.OneToOneField('Order', on_delete=models.CASCADE, related_name='payment')
    payment_type = models.CharField(
        max_length=50,
        choices=[
            ('card', 'Card'),
            ('cash', 'Cash'),
            ('paypal', 'PayPal')
        ],
        default='card'
    )
    payment_date = models.DateTimeField(auto_now_add=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Payment #{self.id} for Order #{self.order.id}"


# 10. Вішліст (Wishlist)
class Wishlist(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    instrument = models.ForeignKey(Instrument, on_delete=models.CASCADE)
    comment = models.TextField(blank=True)

    def __str__(self):
        return f"Wishlist #{self.id} - {self.user.username}"


# 11. Сповіщення (Notification)
class Notification(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.CharField(max_length=255)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification #{self.id} for {self.user.username}"
    

