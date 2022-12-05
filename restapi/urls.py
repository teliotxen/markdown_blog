from django.urls import path
from restapi.views import TestSetApi, LikeApi, CommentsAPI, ImageUploader, TagUpdater

urlpatterns = [
    path('TestSet/', TestSetApi.as_view(), name='api_get'),
    path('LikeApi/', LikeApi.as_view(), name='api_like'),
    path('CommentsApi/', CommentsAPI.as_view(), name='api_comments'),
    path('uploader/', ImageUploader.as_view(), name='api_image'),
    path('tagUpdater/', TagUpdater.as_view(), name='api_tags'),


]
