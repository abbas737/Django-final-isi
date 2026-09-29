from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Avg, Count, Q

from .models import Article, Category, Favorite, ArticleReaction, ArticleRating
from .forms import ArticleForm


def is_admin(user):
    return (
        user.is_authenticated
        and hasattr(user, 'profile')
        and user.profile.role == 'admin'
    )


def get_user_role(user):

    if user.is_superuser:
        return 'super_admin'

    elif is_admin(user):
        return 'admin'

    elif user.is_authenticated:
        return 'user'

    else:
        return 'guest'


def article_list(request):
    articles = Article.objects.filter(
        status='published'
    ).annotate(
        like_count=Count(
            'reactions',
            filter=Q(reactions__reaction='like'),
            distinct=True
        ),
        dislike_count=Count(
            'reactions',
            filter=Q(reactions__reaction='dislike'),
            distinct=True
        ),
        average_rating=Avg(
            'ratings__value'
        )
    ).order_by('-created_at')

    favorite_article_ids = []

    if request.user.is_authenticated:
        favorite_article_ids = list(
            Favorite.objects.filter(
                user=request.user
            ).values_list(
                'article_id',
                flat=True
            )
        )

    role = get_user_role(request.user)

    return render(
        request,
        'articles/article_list.html',
        {
            'articles': articles,
            'role': role,
            'favorite_article_ids': favorite_article_ids
        }
    )

@login_required
def popular(request):

    articles = Article.objects.filter(
        status='published'
    ).annotate(

        like_count=Count(
            'reactions',
            filter=Q(reactions__reaction='like'),
            distinct=True
        ),

        dislike_count=Count(
            'reactions',
            filter=Q(reactions__reaction='dislike'),
            distinct=True
        ),

        average_rating=Avg(
            'ratings__value'
        )

    ).filter(
        average_rating__gte=4
    ).order_by('-average_rating')


    favorite_article_ids = []

    if request.user.is_authenticated:

        favorite_article_ids = list(
            Favorite.objects.filter(
                user=request.user
            ).values_list(
                'article_id',
                flat=True
            )
        )


    return render(
        request,
        'articles/popular.html',
        {
            'articles': articles,
            'favorite_article_ids': favorite_article_ids
        }
    )

@login_required
def categories(request):
    categories = Category.objects.all()

    return render(
        request,
        'articles/categories.html',
        {'categories': categories}
    )

@login_required
def category_detail(request, category_id):

    category = get_object_or_404(
        Category,
        id=category_id
    )


    articles = Article.objects.filter(
        category=category,
        status='published'
    ).annotate(

        like_count=Count(
            'reactions',
            filter=Q(reactions__reaction='like'),
            distinct=True
        ),

        dislike_count=Count(
            'reactions',
            filter=Q(reactions__reaction='dislike'),
            distinct=True
        ),

        average_rating=Avg(
            'ratings__value'
        )

    ).order_by('-created_at')


    favorite_article_ids = []

    if request.user.is_authenticated:

        favorite_article_ids = list(
            Favorite.objects.filter(
                user=request.user
            ).values_list(
                'article_id',
                flat=True
            )
        )


    return render(
        request,
        'articles/category_detail.html',
        {
            'category': category,
            'articles': articles,
            'favorite_article_ids': favorite_article_ids
        }
    )


@login_required
def authors(request):

    authors = User.objects.filter(
        is_superuser=False
    ).annotate(
        article_count=Count(
            'articles',
            filter=Q(articles__status='published')
        )
    ).order_by('username')

    return render(
        request,
        'articles/authors.html',
        {
            'authors': authors
        }
    )


@login_required
def favorites(request):

    articles = Article.objects.filter(
        status='published',
        favorites__user=request.user
    ).annotate(

        like_count=Count(
            'reactions',
            filter=Q(reactions__reaction='like'),
            distinct=True
        ),

        dislike_count=Count(
            'reactions',
            filter=Q(reactions__reaction='dislike'),
            distinct=True
        ),

        average_rating=Avg(
            'ratings__value'
        )

    ).order_by('-created_at')


    favorite_article_ids = list(
        Favorite.objects.filter(
            user=request.user
        ).values_list(
            'article_id',
            flat=True
        )
    )


    return render(
        request,
        'articles/favorites.html',
        {
            'articles': articles,
            'favorite_article_ids': favorite_article_ids
        }
    )


@login_required
def article_create(request):

    if request.method == 'POST':
        form = ArticleForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():
            article = form.save(commit=False)
            article.author = request.user

            if request.user.is_superuser or is_admin(request.user):
                article.status = 'published'
            else:
                article.status = 'pending'

            article.save()

            return redirect('article_list')

    else:
        form = ArticleForm()

    return render(
        request,
        'articles/article_create.html',
        {
            'form': form
        }
    )



@login_required
def article_edit(request, article_id):

    
    if request.user.is_superuser or is_admin(request.user):

        article = get_object_or_404(
            Article,
            id=article_id
        )

    
    else:

        article = get_object_or_404(
            Article,
            id=article_id,
            author=request.user
        )


    if request.method == 'POST':

        form = ArticleForm(
            request.POST,
            request.FILES,
            instance=article
        )

        if form.is_valid():

            article = form.save(commit=False)


            if request.user.is_superuser or is_admin(request.user):
                article.status = 'published'

            else:
                article.status = 'pending'

            article.save()

            return redirect('article_list')

    else:

        form = ArticleForm(
            instance=article
        )


    return render(
        request,
        'articles/article_edit.html',
        {
            'form': form,
            'article': article
        }
    )


@login_required
def article_delete(request, article_id):

    if request.user.is_superuser or is_admin(request.user):

        article = get_object_or_404(
            Article,
            id=article_id
        )

    else:

        article = get_object_or_404(
            Article,
            id=article_id,
            author=request.user
        )


    if request.method == 'POST':

        article.delete()

        return redirect('article_list')


    return render(
        request,
        'articles/article_delete.html',
        {
            'article': article
        }
    )



@login_required
def article_like(request, article_id):

    article = get_object_or_404(
        Article,
        id=article_id,
        status='published'
    )

    reaction = ArticleReaction.objects.filter(
        article=article,
        user=request.user
    ).first()

    if reaction and reaction.reaction == 'like':
        reaction.delete()

    elif reaction:
        reaction.reaction = 'like'
        reaction.save()

    else:
        ArticleReaction.objects.create(
            article=article,
            user=request.user,
            reaction='like'
        )

    return redirect('article_list')


@login_required
def article_dislike(request, article_id):

    article = get_object_or_404(
        Article,
        id=article_id,
        status='published'
    )

    reaction = ArticleReaction.objects.filter(
        article=article,
        user=request.user
    ).first()

    if reaction and reaction.reaction == 'dislike':
        reaction.delete()

    elif reaction:
        reaction.reaction = 'dislike'
        reaction.save()

    else:
        ArticleReaction.objects.create(
            article=article,
            user=request.user,
            reaction='dislike'
        )

    return redirect('article_list')


@login_required
def article_favorite(request, article_id):

    article = get_object_or_404(
        Article,
        id=article_id,
        status='published'
    )

    favorite = Favorite.objects.filter(
        article=article,
        user=request.user
    ).first()

    if favorite:
        favorite.delete()

    else:
        Favorite.objects.create(
            article=article,
            user=request.user
        )

    return redirect('article_list')

@login_required
def article_rating(request, article_id):

    article = get_object_or_404(
        Article,
        id=article_id,
        status='published'
    )

    if request.method == 'POST':

        value = request.POST.get('rating')

        if value:
            value = int(value)

            if 1 <= value <= 5:

                ArticleRating.objects.update_or_create(
                    article=article,
                    user=request.user,
                    defaults={
                        'value': value
                    }
                )

    return redirect('article_list')

@login_required
def author_articles(request, author_id):

    author = get_object_or_404(
        User,
        id=author_id,
        is_superuser=False
    )

    articles = Article.objects.filter(
        author=author,
        status='published'
    ).select_related(
        'category',
        'author'
    ).annotate(

        like_count=Count(
            'reactions',
            filter=Q(reactions__reaction='like'),
            distinct=True
        ),

        dislike_count=Count(
            'reactions',
            filter=Q(reactions__reaction='dislike'),
            distinct=True
        ),

        average_rating=Avg(
            'ratings__value'
        )

    ).order_by('-created_at')


    categories = Category.objects.filter(
        articles__author=author,
        articles__status='published'
    ).distinct()


    category_id = request.GET.get('category')

    if category_id:
        articles = articles.filter(
            category_id=category_id
        )


    favorite_article_ids = []

    if request.user.is_authenticated:

        favorite_article_ids = list(
            Favorite.objects.filter(
                user=request.user
            ).values_list(
                'article_id',
                flat=True
            )
        )


    return render(
        request,
        'articles/author_articles.html',
        {
            'author': author,
            'articles': articles,
            'categories': categories,
            'selected_category': category_id,
            'favorite_article_ids': favorite_article_ids,
        }
    )


@login_required
def admin_dashboard(request):

    if not is_admin(request.user):
        return redirect('article_list')

    users = User.objects.filter(
        is_superuser=False
    ).select_related(
        'profile'
    ).order_by('username')

    articles = Article.objects.all().order_by('-created_at')

    return render(
        request,
        'articles/admin_dashboard.html',
        {
            'users': users,
            'articles': articles
        }
    )


@login_required
def block_user(request, user_id):

    if not is_admin(request.user):
        return redirect('article_list')

    user_to_block = get_object_or_404(
        User,
        id=user_id,
        is_superuser=False
    )

    
    if user_to_block == request.user:
        return redirect('admin_dashboard')

    profile = user_to_block.profile

    profile.is_blocked = not profile.is_blocked
    profile.save()

    return redirect('admin_dashboard')