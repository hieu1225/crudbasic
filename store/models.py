# store/models.py
from django.db import models
from django.contrib.auth.models import User

# Model cho Sách
class Book(models.Model):
    title = models.CharField(max_length=200, verbose_name="Tên sách")
    author = models.CharField(max_length=200, verbose_name="Tác giả")
    description = models.TextField(blank=True, null=True, verbose_name="Mô tả")
    price = models.DecimalField(max_digits=10, decimal_places=0, verbose_name="Giá bán")
    image = models.ImageField(upload_to='book_images/', blank=True, null=True, verbose_name="Ảnh bìa")

    def __str__(self):
        return self.title

# Model cho Đơn hàng
class Order(models.Model):
    # Dành cho người dùng đã đăng ký
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    
    # Dành cho khách vãng lai
    guest_name = models.CharField(max_length=100, blank=True, null=True, verbose_name="Tên khách hàng")
    guest_email = models.EmailField(blank=True, null=True, verbose_name="Email khách")
    guest_address = models.CharField(max_length=255, blank=True, null=True, verbose_name="Địa chỉ giao hàng")
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Ngày đặt")
    is_completed = models.BooleanField(default=False, verbose_name="Đã hoàn thành")

    def __str__(self):
        if self.user:
            return f"Đơn hàng của {self.user.username}"
        return f"Đơn hàng của khách {self.guest_name}"

# Model chi tiết đơn hàng (Sách nào trong đơn hàng nào)
class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} x {self.book.title} trong {self.order}"