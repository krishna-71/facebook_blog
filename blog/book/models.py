from django.db import models

try:
    from ..authentication.models import User

except:
    from authentication.models import User


class Post(models.Model):
    objects = None
    id = models.AutoField(primary_key=True)
    owner = models.ForeignKey(to=User, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    picture = models.ImageField(upload_to='Images',default='Images/None/No-img.jpg')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
