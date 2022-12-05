from django.contrib import admin
from filters.models import TestSet, Comments, PostImage,Tag, Categories
# Register your models here.
admin.site.register(TestSet)
admin.site.register(Comments)
admin.site.register(PostImage)
admin.site.register(Tag)
admin.site.register(Categories)
