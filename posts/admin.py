from django.contrib import admin

from posts import models

# Register your models here.

admin.site.register(models.Posting)
admin.site.register(models.Comment)
admin.site.register(models.Like)
