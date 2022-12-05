from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from filters.models import TestSet, Comments, PostImage, Tag, Categories
from .forms import TestSetForm
import secrets
import time

from django.views.generic import ListView
# Create your views here.
@login_required
def my_page(request):
    data = TestSet.objects.filter(author=request.user).order_by('-created_at')
    context = {
        'data':data
    }
    return render(request, 'filters/profile.html', context=context)


def page_detail(request, pk):
    data = TestSet.objects.get(pk=pk)
    request.session['key'] = pk
    liked = data.like_user.filter(pk = request.user.pk)
    if len(liked) == 1:
        likes = True
    else:
        likes = False

    tag_list = list()
    for item in data.tag.all():
        tag_list.append(item.name)


    count_likes = len(data.like_user.all())
    context = {
        'user': request.user,
        'data':data,
        'likes':likes,
        'tags':tag_list,
        'count_likes':count_likes,
    }
    return render(request, 'filters/detail.html', context=context)

@login_required
def test_input(request):

    request.session['temp_article'] = secrets.token_hex(nbytes=8) + str(int(time.time()))

    if request.method == 'POST':
        # get information
        title = request.POST['title']
        body = request.POST['body']

        data = TestSet()
        data.title = title
        data.body = body
        data.author = request.user
        data.image = request.session['temp_article']
        data.feature = request.POST['feature']

        category = Categories.objects.get(pk=request.POST['categories'])
        data.categories = category
        data.save()

        tags = request.POST['tag'].split(',')

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

        try:
            Image_object = PostImage.objects.get(temp=request.session['temp_article'])
            Image_object.post = data

        except:
            pass

        return redirect('page_detail', data.pk)

    forms = TestSetForm()
    context = {'form':forms}
    return render(request, 'filters/input.html', context=context)


def test_update(request):
    print(12345)
    pk = request.session['key']
    data = TestSet.objects.get(pk=pk)

    if data.author != request.user:
        return None
    form = TestSetForm(instance=data)
    request.session['temp_article'] = data.image
    if request.method == 'POST':
        title = request.POST['body']
        body = request.POST['body']

        data = TestSet()
        data.title = title
        data.body = body
        data.save()

    forms = TestSetForm()
    context = {
        'form':form,
        'pk': request.session['key']
    }
    return render(request, 'filters/update.html', context=context)



class LandingPage(ListView):
    model = TestSet
    template_name = 'filters/landing_page.html'
    def get_queryset(self):
        data = TestSet.objects.all().order_by('-created_at')
        return data

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        return context




