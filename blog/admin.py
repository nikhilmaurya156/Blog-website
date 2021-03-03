from django.contrib import admin
from .models import Post, AddingComment, PostDetail, Suggestion, Bookmark

admin.site.register(Post)
admin.site.register(AddingComment)
admin.site.register(PostDetail)
admin.site.register(Suggestion)
admin.site.register(Bookmark)