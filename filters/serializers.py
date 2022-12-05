from rest_framework import serializers
from .models import TestSet, Comments, PostImage


class TestSetSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestSet
        fields = ['title', 'body','feature']

class CommentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comments
        fields = '__all__'


class PostImageSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(use_url=True)

    class Meta:
        models=PostImage
        fields = ['image']