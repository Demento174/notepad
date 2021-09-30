from django.shortcuts import render
from django.views.generic.list import ListView
from wordpress.models import Entities
from wordpress.Entities import *
# Create your views here.

class PostsListView(ListView):
    model = Entities
    paginate_by = 5
    template_name = "wordpress/PostsList.html"

    # def get_queryset(self):
    #     return []


def index(request):
    return render(request,"wordpress/PostsList.html",{"items":get_all_posts()})