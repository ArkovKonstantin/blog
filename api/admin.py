from django.contrib import admin

# Register your models here.
from api.models import *

admin.site.register(Topic)
admin.site.register(Comment)
admin.site.register(TopicLike)