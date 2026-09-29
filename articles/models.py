from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Article(models.Model):

    STATUS_CHOICES = [
        ('pending', 'Gözləyir'),
        ('published', 'Yayımlandı'),
        ('rejected', 'Rədd edildi'),
    ]

    title = models.CharField(max_length=255)

    image = models.ImageField(
    upload_to='articles/',
    blank=True,
    null=True
)

    content = models.TextField()

    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='articles'
    )

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='articles'
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )

    def __str__(self):
        return self.title


class ArticleReaction(models.Model):
    REACTION_CHOICES = [
        ('like', 'Like'),
        ('dislike', 'Dislike'),
    ]

    article = models.ForeignKey(
        Article,
        on_delete=models.CASCADE,
        related_name='reactions'
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    reaction = models.CharField(
        max_length=10,
        choices=REACTION_CHOICES
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['article', 'user'],
                name='unique_article_reaction'
            )
        ]


class Favorite(models.Model):
    article = models.ForeignKey(
        Article,
        on_delete=models.CASCADE,
        related_name='favorites'
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='favorites'
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['article', 'user'],
                name='unique_article_favorite'
            )
        ]
    def __str__(self):
        return f'{self.user.username} - {self.article.title}'

class ArticleRating(models.Model):
    article = models.ForeignKey(
        Article,
        on_delete=models.CASCADE,
        related_name='ratings'
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    value = models.IntegerField()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['article', 'user'],
                name='unique_article_rating'
            )
        ]

    def __str__(self):
        return f'{self.user.username} - {self.article.title} - {self.value}'

    
    