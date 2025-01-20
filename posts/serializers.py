from rest_framework import serializers
from .models import Post

class PostSerializer(serializers.ModelSerializer):
    author_avatar = serializers.SerializerMethodField()
    author_name = serializers.SerializerMethodField()
    author_nickname = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = [
            'id', 'title', 'content', 'image', 'is_premium',
            'author_avatar', 'author_name', 'author_nickname', 'created_at'
        ]

    def get_author_avatar(self, obj):
        return obj.author.avatar.url if obj.author.avatar else None

    def get_author_name(self, obj):
        return f"{obj.author.first_name} {obj.author.last_name}"

    def get_author_nickname(self, obj):
        return obj.author.nickname
