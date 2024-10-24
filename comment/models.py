from django.db import models

# Create your models here.


class Comment(models.Model):
    text = models.TextField(max_length=255, blank=False, null=False)

    task = models.ForeignKey('task.Task', on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='comments')

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text[:20]
