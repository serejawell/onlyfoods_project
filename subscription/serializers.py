from rest_framework import serializers
from subscription.models import Subscription
from posts.models import Post


class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = ['id', 'author', 'title', 'description', 'price', 'created_at']


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'author', 'title', 'content', 'image', 'is_premium', 'created_at']
