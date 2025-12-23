from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('app.urls')), # 核心：将根目录请求全部交给 app 路由处理
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)