from django.views import View
from django.http import Http404,HttpResponse
from wordpress.models import *
import json
from django.views.decorators.csrf import csrf_protect


class AJAXview(View):
    def get(self, request, *args, **kwargs):

        return HttpResponse('<h1>Page was not found</h1>')


    def post(self, request, *args, **kwargs):

        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)

        action = body['action']
        if action == 'removePost':
            post = Entities.objects.get(pk=body['id'])
            if post:
                post.delete()
        elif action == 'removePostType':
            post = Types.objects.get(pk=body['id'])
            if post:
                post.delete()
        if action == 'removeTerm':
            post = Terms.objects.get(pk=body['id'])
            if post:
                post.delete()
        return HttpResponse('good')