from django.urls import path
from .views import *
from .Apps import AJAXview
urlpatterns = [
        path('', PostsListView.as_view(), name='wp_index'),

        #ajax
        path('wp-admin/admin-ajax.php/', AJAXview.as_view(), name='wp_posts_type_create'),

        #output
        path('posts/<str:postType>/', PostsListView.as_view(), name='wp_posts_type'),
        path('term/<str:type>/<slug:slug>/', PostsListView.as_view(), name='wp_term'),
        path('entity/<str:type>/<slug:slug>/', EntityDetailView.as_view(), name='wp_entity'),

        #edit
        path('edit/posts/<str:postType>/', EditPostType.as_view(), name='wp_posts_type_edit'),
        path('edit/term/<str:type>/<slug:slug>/', EditTerm.as_view(), name='wp_term_edit'),
        path('edit/entity/<str:type>/<slug:slug>/', EditPost.as_view(), name='wp_entity_edit'),

        #create
        path('create/posts/', CreatePostType.as_view(), name='wp_posts_type_create'),
        path('create/term/<str:type>/', CreateTerm.as_view(), name='wp_term_create'),
        path('create/entity/<str:type>/', CreatePost.as_view(), name='wp_entity_create'),


        ]

