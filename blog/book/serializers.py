from rest_framework import serializers
from .models import *


class PostSerializer(serializers.ModelSerializer):
    picture = serializers.ImageField(max_length=None,use_url=True)

    class Meta:
        model = Post
        fields = ('id','name','picture','description')