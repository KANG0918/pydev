from django.db import models


# Create your models here.
class Resume(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    introduce = models.CharField(max_length=200)
    profile = models.TextField()
    online = models.BooleanField(default=False)

    # 後臺資料庫可以印出名字(客製化)
    def __str__(self):
        return f"{self.name} {(self.email)}"
