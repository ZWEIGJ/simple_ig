# Simple IG (Django Project)

一个基于 Django 开发的精简版 Instagram。

## 核心功能
- 用户注册/登录/退出
- 个人主页（支持上传真实头像）
- 发布图片帖子
- 点赞与评论（支持作者删除评论/帖子）
- 关注系统与动态 Feed 流


## 搭建虚拟环境
虚拟环境的作用是为这个项目创建一个独立的 Python 运行空间，防止不同项目之间的软件包版本产生冲突
创建命令：运行 python -m venv venv 。
激活环境
Windows 用户：输入 venv\Scripts\activate 。
Mac/Linux 用户：输入 source venv/bin/activate 。
激活成功后，命令行提示符前通常会出现 (venv) 字样


## 如何运行
1. 安装依赖：`pip install -r requirements.txt`
2. 执行迁移：`python manage.py migrate`
3. 启动服务器：`python manage.py runserver`