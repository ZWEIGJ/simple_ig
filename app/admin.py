from django.contrib import admin
from .models import Post, Like, Follow

# 注册模型，这样你就能在 /admin 后台增删改查了 [cite: 317]
admin.site.register([Post, Like, Follow])