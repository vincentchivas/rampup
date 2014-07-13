from django.contrib import admin
from blog.models import Users
from blog.models import Author,Book

admin.site.register(Users)
admin.site.register(Book)
admin.site.register(Author)
