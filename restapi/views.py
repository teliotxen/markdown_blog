import json
from django.http import JsonResponse
from rest_framework import status
from rest_framework.parsers import JSONParser
from rest_framework.views import APIView
from rest_framework.response import Response
from filters.serializers import TestSetSerializer, CommentsSerializer, PostImageSerializer
from filters.models import TestSet, Comments, PostImage, Tag
from .function import get_restapi_data


# Create your views here.
class TestSetApi(APIView):
    def get(self, request):
        pk = request.session['key']
        queryset = TestSet.objects.get(pk=pk)
        serializer = TestSetSerializer(queryset, many=False)
        return Response(serializer.data)

    def put(self, request):
        pk = request.session['key']
        queryset = TestSet.objects.get(pk=pk)
        update_data = JSONParser().parse(request)
        TestSet_Serializer = TestSetSerializer(queryset, data=update_data)

        if TestSet_Serializer.is_valid():
            TestSet_Serializer.save()
            return JsonResponse(TestSet_Serializer.data)
        else:
            print('fail')
        return JsonResponse({'message': 'Tutorial was deleted successfully!'}, status=status.HTTP_200_OK)


class LikeApi(APIView):

    def put(self, request):
        if request.user.is_authenticated:
            pk = request.session['key']
            article = TestSet.objects.get(pk=pk)
            if article.like_user.filter(pk=request.user.pk).exists():
                article.like_user.remove(request.user)
                article.save()
            else:
                article.like_user.add(request.user)
                article.save()
            return JsonResponse({'message': 'success!'}, status=status.HTTP_200_OK)

        return JsonResponse({'message': 'not auth'}, status=status.HTTP_401_UNAUTHORIZED)


class CommentsAPI(APIView):
    def get(self, request):
        pk = request.session['key']
        data = Comments.objects.filter(article=pk).order_by("-created_at")
        serializer = CommentsSerializer(data, many=True)
        return Response(serializer.data)

    def post(self, request):
        pk = request.session['key']

        if request.user.is_authenticated:

            res = get_restapi_data(request.POST)
            comment = Comments()
            comment.user = request.user
            comment.body = res['body']
            comment.article = TestSet.objects.get(pk=pk)
            comment.username = request.user.username
            comment.save()

            return JsonResponse({'message': 'success!'}, status=status.HTTP_200_OK)

        return JsonResponse({'message': 'not auth'}, status=status.HTTP_401_UNAUTHORIZED)


class ImageUploader(APIView):
    def get(self, request):
        pk = request.session['temp_article']
        data = PostImage.objects.filter(temp=pk)
        res = list()
        for item in data:
            res.append(item.image.url)
        return JsonResponse({'img': res, 'key': pk}, status=status.HTTP_200_OK)

    def post(self, request):
        data_order = PostImage.objects.filter(temp=request.session['temp_article'])
        if len(data_order) == 0:
            data_count = 0
        else:
            data_count = len(data_order)

        image = PostImage()
        image.image = request.FILES['file']
        image.temp = request.session['temp_article']
        image.user = request.user
        image.order = data_count
        image.save()

        return JsonResponse({'status': 'ok'}, status=status.HTTP_200_OK)

    def delete(self, request):
        pk = request.session['temp_article']
        res = get_restapi_data(request.POST)
        order_num = int(res['order'])
        data = PostImage.objects.filter(temp=pk, order=order_num)
        data.delete()
        return JsonResponse({'status': 'ok'}, status=status.HTTP_200_OK)


class TagUpdater(APIView):
    def get(self, request):
        pk = request.session['key']
        data = TestSet.objects.get(pk=pk)

        tag_list = ""

        for item in data.tag.all():
            tag_list+=item.name
            tag_list+=', '

        tag_list = tag_list[0:len(tag_list)-2]

        return JsonResponse({'tag':tag_list}, status=status.HTTP_200_OK)

    def put(self, request):
        pk = request.session['key']
        data = TestSet.objects.get(pk=pk)
        res = get_restapi_data(request.POST)
        tags = res['tags'].split(',')

        for item in data.tag.all():
            item.delete()

        for tag in tags:
            if not tag:
                continue
            else:
                tag = tag.strip()

                if len(Tag.objects.filter(name=tag)) == 0:
                    new_tag = Tag()
                    new_tag.name = tag
                    new_tag.save()
                    data.tag.add(new_tag)
                else:
                    new_tag = Tag.objects.get(name=tag)
                    data.tag.add(new_tag)

        data.save()

        return JsonResponse({'tag': 'ok'}, status=status.HTTP_200_OK)

