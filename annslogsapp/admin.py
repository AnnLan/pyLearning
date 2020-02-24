from django.contrib import admin

# Register your models here.
from annslogsapp.models import Topic
from annslogsapp.models import Entry
admin.site.register(Topic)
admin.site.register(Entry)
