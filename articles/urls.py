from django.urls import path
from . import views

urlpatterns = [
    path('', views.article_list, name='article_list'),

    path('popular/', views.popular, name='popular'),

    path('categories/', views.categories, name='categories'),
    path('categories/<int:category_id>/', views.category_detail, name='category_detail'),

    path('authors/', views.authors, name='authors'),

    path('favorites/', views.favorites, name='favorites'),

    path('create/', views.article_create, name='article_create'),

    path('<int:article_id>/edit/', views.article_edit, name='article_edit'),
    path('<int:article_id>/delete/', views.article_delete, name='article_delete'),

    path('<int:article_id>/like/', views.article_like, name='article_like'),
    path('<int:article_id>/dislike/', views.article_dislike, name='article_dislike'),
    path('<int:article_id>/favorite/', views.article_favorite, name='article_favorite'),
    path('<int:article_id>/rating/', views.article_rating, name='article_rating'),
    path('authors/<int:author_id>/', views.author_articles, name='author_articles'),

    path('dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('dashboard/users/<int:user_id>/block/',views.block_user,name='block_user'),
]