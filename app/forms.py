from django import forms
from .models import Post

class PostForm(forms.ModelForm):
    class Meta:
        model = Post # 关联我们之前定义的 Post 模型 [cite: 176]
        fields = ['image', 'caption'] # 界面上只显示图片上传和描述输入框 [cite: 177]