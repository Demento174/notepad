from django import template
from wordpress.Entities import PostTypeInterface,CategoryInterface,TagInterface,PostInterface
from wordpress.models import *

register = template.Library()



@register.inclusion_tag('include/_sidebar.html')
def sidebar():
    return {
        'postTypes': PostTypeInterface.get_all_short(),
        'categories': CategoryInterface.get_tree(),
        'tags': TagInterface.get_all_short(),

    }

@register.inclusion_tag('include/_header.html')
def header():
    return {
        'postTypes': PostTypeInterface.get_all_short(),
        'categories': CategoryInterface.get_all_short(),
        'tags': TagInterface.get_all_short(),
        'modelPostType': PostTypeInterface,
        'modelCategory': CategoryInterface,
        'modelTag': TagInterface,
        'modelPost': PostInterface,
    }

