# store/admin.py
from django.contrib import admin
from .models import Book, Order, OrderItem

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0 # không hiển thị thêm dòng trống

class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', '__str__', 'created_at', 'is_completed')
    list_filter = ('is_completed', 'created_at')
    inlines = [OrderItemInline]

admin.site.register(Book)
admin.site.register(Order, OrderAdmin)