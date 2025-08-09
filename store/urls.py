# store/urls.py

from django.urls import path
from . import views

urlpatterns = [
    # URLs cho người dùng xem và mua
    path('', views.book_list, name='book_list'),
    path('book/<int:pk>/', views.book_detail, name='book_detail'),
    path('buy/<int:pk>/', views.buy_now, name='buy_now'),
    path('order-success/', views.order_success, name='order_success'),

    # URLs CRUD Sách (đã được bảo vệ trong views)
    path('book/new/', views.BookCreateView.as_view(), name='book_create'),
    path('book/<int:pk>/edit/', views.BookUpdateView.as_view(), name='book_update'),
    path('book/<int:pk>/delete/', views.BookDeleteView.as_view(), name='book_delete'),
]