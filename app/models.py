from django.db import models
from django.contrib.auth.models import User

# 1. 帖子模型：存储照片和文字 [cite: 148]
class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts') # [cite: 149]
    image = models.ImageField(upload_to='posts/%Y/%m/%d/') # 按年月日存放图片 [cite: 150]
    caption = models.TextField(blank=True) # 描述 [cite: 151]
    created_at = models.DateTimeField(auto_now_add=True) # 自动记录时间 [cite: 152]

    class Meta:
        ordering = ['-created_at'] # 默认显示最新的帖子 [cite: 154]

# 2. 点赞模型：记录谁给哪条帖子点过赞 [cite: 155]
class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE) # [cite: 156]
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes') # [cite: 157]

    class Meta:
        unique_together = ('user', 'post') # 约束：一个人对一条帖只能点赞一次 [cite: 159]

# 3. 关注模型：记录用户之间的关注关系 [cite: 160]
class Follow(models.Model):
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following') # 粉丝 [cite: 161]
    followed = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followers') # 被关注者 [cite: 162]

    class Meta:
        unique_together = ('follower', 'followed') # 约束：不能重复关注 [cite: 164]

# 4 评论模型：存储谁、在什么时候、对哪条帖子说了什么
class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)

    def __clstr__(self):
        return f'{self.author.username}: {self.content[:20]}'