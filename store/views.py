# store/views.py

from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.mixins import UserPassesTestMixin

from .models import Book, Order, OrderItem

# --- Views cho người dùng xem và mua hàng ---

def book_list(request):
    """Hiển thị danh sách tất cả sách"""
    books = Book.objects.all()
    context = {'books': books}
    return render(request, 'store/book_list.html', context)

def book_detail(request, pk):
    """Hiển thị chi tiết một cuốn sách"""
    book = get_object_or_404(Book, pk=pk)
    context = {'book': book}
    return render(request, 'store/book_detail.html', context)

def buy_now(request, pk):
    """Xử lý việc mua sách (cả user và khách)"""
    book = get_object_or_404(Book, pk=pk)

    if request.method == 'POST':
        # Tạo đơn hàng
        order = Order()
        if request.user.is_authenticated:
            order.user = request.user
        else:
            # Lấy thông tin từ form của khách vãng lai
            order.guest_name = request.POST.get('name')
            order.guest_email = request.POST.get('email')
            order.guest_address = request.POST.get('address')
        
        # Kiểm tra xem thông tin khách có hợp lệ không (đơn giản)
        if not order.user and (not order.guest_name or not order.guest_email or not order.guest_address):
             # Có thể thêm message lỗi ở đây nếu muốn
             return redirect('buy_now', pk=book.pk)

        order.save() # Lưu đơn hàng để có ID

        # Thêm sách vào đơn hàng
        OrderItem.objects.create(order=order, book=book, quantity=1)

        # Chuyển hướng đến trang cảm ơn
        return redirect('order_success')

    context = {'book': book}
    return render(request, 'store/buy_now.html', context)

def order_success(request):
    """Hiển thị trang thông báo đặt hàng thành công"""
    return render(request, 'store/order_success.html')

# --- Views CRUD cho quản trị (ĐÃ ĐƯỢC BẢO VỆ) ---

class BookCreateView(UserPassesTestMixin, CreateView):
    model = Book
    fields = ['title', 'author', 'description', 'price', 'image']
    template_name = 'store/book_form.html'
    success_url = reverse_lazy('book_list')

    def test_func(self):
        # Chỉ cho phép user là staff (admin) truy cập
        return self.request.user.is_staff

class BookUpdateView(UserPassesTestMixin, UpdateView):
    model = Book
    fields = ['title', 'author', 'description', 'price', 'image']
    template_name = 'store/book_form.html'
    success_url = reverse_lazy('book_list')

    def test_func(self):
        return self.request.user.is_staff

class BookDeleteView(UserPassesTestMixin, DeleteView):
    model = Book
    template_name = 'store/book_confirm_delete.html'
    success_url = reverse_lazy('book_list')

    def test_func(self):
        return self.request.user.is_staff

# --- Views cho User Authentication ---

def register_view(request):
    if request.user.is_authenticated:
        return redirect('book_list') # Nếu đã đăng nhập thì về trang chủ
        
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user) # Tự động đăng nhập sau khi đăng ký thành công
            return redirect('book_list')
    else:
        form = UserCreationForm()
    return render(request, 'store/register.html', {'form': form})