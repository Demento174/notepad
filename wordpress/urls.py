from django.urls import path
from .views import *
urlpatterns = [
        path('', PostsListView.as_view(), name='wp_index'),
        # path('', index, name='wp_index'),
        path('<str:type>/<identifier>/', PostsListView.as_view(), name='wp_entity'),
        path('posts/<str:postType>/', PostsListView.as_view(), name='wp_post_type'),
        path('<str:type>/<identifier>/', PostsListView.as_view(), name='wp_term'),
        # path('news/<int:pk>', ViewNews.as_view(), name='single_news'),
        # path('news/add-news',CreateNews.as_view(),name='add_news'),
    ]
