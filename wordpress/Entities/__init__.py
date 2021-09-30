from .Interfaces import *


from .Posts import Post
from .Taxonomies import Category,Tag
from abc import ABCMeta, abstractmethod
from django.db import models


def get_post_by_id(id):
  return Post.convert(Post.query().query_by_id(id))

def get_post_by_slug(slug,type):
    return Post.get_by_slug(type,slug)

def get_all_posts(type=None):
    return Post.get_all(type)

#--------------------------[ Categories ]
def get_category_by_id(id):
    return Category.get_by_id(id)

def get_category_by_slug(slug):
    return Category.get_by_slug(slug)

def get_all_category():
    return Category.get_all()

#--------------------------[ Tags ]
def get_tag_by_id(id):
    return Category.get_by_id(id)

def get_tag_by_slug(slug):
    return Category.get_by_slug(slug)

def get_all_tags():
    return Category.all()

#--------------------------[ other function ]
def get_category_tree():
    result = []
    for cat in get_all_category():
        if cat.parent is None:
            result.append(cat.family)

    return result



