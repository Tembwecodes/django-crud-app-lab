from django.contrib import admin
from .models import Song, Review

# Register your models here.
admin.site.register(Song)
admin.site.register(Review)