from typing import Any

from django.contrib.auth.models import User
from django.db import models

from lib.models.soft_delete import SoftDeleteable, SoftDeleteManager


# Create your models here.
class Resume(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    introduce = models.CharField(max_length=200)
    profile = models.TextField()
    online = models.BooleanField(default=False)
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    bookmark = models.ManyToManyField(User, related_name="bookmarks")  # 收藏，多對多

    # 後臺資料庫可以印出名字(客製化)
    def __str__(self):
        return f"{self.name} {(self.email)}"

    def bookmarked_by(self, user):
        return self.bookmark.filter(id=user.id).exists()


class Comment(SoftDeleteable, models.Model):
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE)  # 建立外建
    content = models.TextField(null=False)  # 還是可以有空的，因為空字串也是
    created_at = models.DateTimeField(auto_now_add=True)
    deleted_at = models.DateTimeField(default=None, null=True)
    objects = SoftDeleteManager()
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)

    class Meta:
        indexes = [
            models.Index(fields=["deleted_at"]),  # 創建索引值
        ]
