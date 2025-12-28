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
    
# 5 用户资料扩展模型：为用户添加头像等额外信息
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='avatars/', default='avatars/default.png')

    def __str__(self):
        return f'{self.user.username} Profile'
    


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='avatars/', default='avatars/default.jpg')
    # 新增：个性签名，限制 150 字，允许为空
    bio = models.TextField(max_length=150, blank=True, verbose_name="个性签名")

    def __str__(self):
        return f'{self.user.username} Profile'
    


from django.db.models.signals import post_save
from django.dispatch import receiver

# 当 User 模型保存后，触发这个函数
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        # 如果是新创建的用户，则创建 Profile
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    # 确保每次保存 User 时，Profile 也会被保存
    instance.profile.save()