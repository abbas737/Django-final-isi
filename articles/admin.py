from django.contrib import admin

from .models import (
    Category,
    Article,
    ArticleReaction,
    ArticleRating,
    Favorite
)


admin.site.register(Category)
admin.site.register(Article)
admin.site.register(ArticleReaction)
admin.site.register(ArticleRating)
admin.site.register(Favorite)