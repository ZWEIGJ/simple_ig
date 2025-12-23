from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls), # 管理后台 
    path('', include('app.urls')),   # 将所有请求交给 app 下的 urls.py 处理 
] 

# 允许在开发环境下通过 URL 访问上传的图片 
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)