from django.conf import settings
from django.db import models

class Bottletext(models.Model):
    """漂流瓶内容及相关信息"""
    title = models.TextField(max_length=100, default = '默认标题')
    text = models.TextField(max_length=2000)
    image = models.ImageField(upload_to='images/', max_length=100000000)
    date_added = models.DateTimeField(auto_now_add=True)
    date_unlock = models.DateTimeField()
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='created_bottletexts', null=True, blank=True)
    receiver = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='received_bottletexts', null=True, blank=True)


    def __str__(self):
        """返回文本字段"""
        return self.text


#心愿单模型
class Topic(models.Model):
    """心愿单的主题"""
    text = models.CharField(max_length=200)
    date_added = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,related_name='created_topic', null=True, blank=True)

    def __str__(self):
        """返回字符串表示"""
        return self.text


class Entry(models.Model):
    """Something specific in a topic."""
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    text = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = 'entries'
 
    def __str__(self):
        """Return a string representation of the model."""
        if len(self.text) > 50:
            return f"{self.text[:50]}..."
        else:
            return f"{self.text}"
