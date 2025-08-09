# mybookstore/mybookstore/urls.py

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

# Import các view cần thiết để định nghĩa URL
from django.contrib.auth import views as auth_views
from store.views import register_view

urlpatterns = [
    path('adminlatadayne/', admin.site.urls),

    # URL của app store
    path('', include('store.urls')),
   
    # Thêm các dòng này vào để định nghĩa các URL authentication
    path('register/', register_view, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='store/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='book_list'), name='logout'),
]

# Cấu hình để hiển thị file media (ảnh ọt) lúc dev
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)