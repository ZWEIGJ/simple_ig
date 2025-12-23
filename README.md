# Simple IG (Django Project)

一个基于 Django 开发的精简版 Instagram。

## 核心功能
- 用户注册/登录/退出
- 个人主页（支持上传真实头像）
- 发布图片帖子
- 点赞与评论（支持作者删除评论/帖子）
- 关注系统与动态 Feed 流

## 如何运行
1. 安装依赖：`pip install -r requirements.txt`
2. 执行迁移：`python manage.py migrate`
3. 启动服务器：`python manage.py runserver`