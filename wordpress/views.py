from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView

import wordpress.models
from wordpress.models import Entities,Terms
from wordpress.Entities.Interfaces import *
from django.views.generic.edit import UpdateView, FormView
from .Forms import *
from django.urls import reverse
from var_dump import var_dump
from django.contrib.auth.mixins import LoginRequiredMixin
class PostsListView(LoginRequiredMixin,ListView):
    model = Entities
    paginate_by = 5
    template_name = "wordpress/PostsList.html"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)

        if 'postType' in self.kwargs:
            context['title'] =f"Тип записи: {PostTypeInterface.get_by_slug(self.kwargs['postType'])}"
        elif 'type' in self.kwargs:
            if self.kwargs['type'] == Terms.TaxonomiesTypes[0][0]:
                context['title'] =f"Категория: {CategoryInterface.get_by_slug(self.kwargs['slug'])}"
            if self.kwargs['type'] == Terms.TaxonomiesTypes[1][0]:
                context['title'] =f"Тег: {TagInterface.get_by_slug(self.kwargs['slug'])}"

        return context

    def get_queryset(self,*args,**kwargs):

        if 'postType' in self.kwargs:
            return PostInterface.get_all_by_type(self.kwargs['postType'])
        elif 'type' in self.kwargs:
            if self.kwargs['type']==Terms.TaxonomiesTypes[0][0]:
                return CategoryInterface.get_posts_by_categories_slug(self.kwargs['slug'])
            if self.kwargs['type'] == Terms.TaxonomiesTypes[1][0]:
                return TagInterface.get_posts_by_tag_slug(self.kwargs['slug'])
        return PostInterface.get_all()

class EntityDetailView(LoginRequiredMixin,DetailView):

    model = Entities
    template_name = 'wordpress/DetailView/Entity.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object'] = PostInterface.get_by_id(context['object'].pk)
        return context

#---------------------------------------[ EDIT ]

class EditPostType(LoginRequiredMixin,FormView):

    form_class = PostTypeForm
    template_name = 'wordpress/Edit/EditPostType.html'
    model = Types

    def get_success_url(self):
        return reverse('wp_posts_type', kwargs={'postType': self.kwargs['postType']})

    def get_initial(self):
        post = PostTypeInterface.get_by_slug(self.kwargs['postType'])
        return {
            'id':post.id,
            'title': post.title,
            'slug': post.slug,
            'image': post.image,
        }

    def form_valid(self, form):
        model = Types.objects.get(slug=self.kwargs['postType'])
        data = form.cleaned_data

        model.title = data['title']
        model.slug = data['slug']

        model.save()
        self.kwargs['postType'] = model.slug
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        post = PostTypeInterface.get_by_slug(self.kwargs['postType'])
        context = super().get_context_data(**kwargs)
        context['id'] = post.id
        return context

class EditPost(LoginRequiredMixin,FormView):
    form_class = EntitiesForm
    template_name = 'wordpress/Edit/EditPost.html'
    model = Entities

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['type'] = PostType.query().by_slug(self.kwargs['type'])
        return kwargs

    def get_success_url(self):
        return reverse('wp_entity',kwargs={'type':self.kwargs['type'],'slug':self.kwargs['slug']})

    def get_initial(self):
        post = PostInterface.get_by_slug(self.kwargs['slug'])

        return {
            'title': post.title,
            'slug': post.slug,
            'content': post.content,
            'tags': [i.id for i in post.get_tags()],
            'categories': [i.id for i in post.get_categories()]
        }

    def form_valid(self, form):

        model = Entities.objects.get(slug = self.kwargs['slug'])
        data = form.cleaned_data

        if (self.kwargs['slug'] != data['slug']) and Entities.objects.filter(slug = data['slug'], type__slug = self.kwargs['type'] ).exists():
            raise Exception(f"post (post type: {self.kwargs['type']}) already exists for this slug - {data['slug']}")


        model.title = data['title']
        model.slug = data['slug']
        model.content = data['content']
        model.image = data['image']

        model.save()

        if len(model.terms.all()) > 0:
            [model.terms.remove(term) for term in model.terms.all()]
        [model.terms.add(term) for term in data['categories']]
        [model.terms.add(term) for term in data['tags']]

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        post = PostInterface.get_by_slug(self.kwargs['slug'])
        context = super().get_context_data(**kwargs)
        context['type'] = post.type
        context['id'] = post.id
        return context

class EditTerm(LoginRequiredMixin,FormView):

    form_class = None
    template_name = 'wordpress/Edit/EditTerm.html'
    model = Types

    def get_form_class(self):
        if self.kwargs['type'] == 'category':
            return CategoryForm
        elif self.kwargs['type'] == 'tag':
            return TagForm

    def get_success_url(self):
        return reverse('wp_term', kwargs={'type': self.kwargs['type'], 'slug': self.kwargs['slug']})

    def get_initial(self):
        if self.kwargs['type'] == 'category':
            post = CategoryInterface.get_by_slug(self.kwargs['slug'])
        elif self.kwargs['type'] == 'tag':
            post = TagInterface.get_by_slug(self.kwargs['slug'])

        model = Terms.objects.get(slug = self.kwargs['slug'],type=self.kwargs['type'])
        parameters = {
            'title': post.title,
            'slug': post.slug,
            'description': post.description,
            'postTypes': model.postTypes.all(),
        }
        if self.kwargs['type'] == 'category':
            parameters['parent'] = model.parent
        return parameters

    def form_valid(self, form):
        model = Terms.objects.get(type=self.kwargs['type'], slug=self.kwargs['slug'])
        data = form.cleaned_data


        model.title = data['title']
        model.slug = data['slug']
        model.description = data['description']
        # model.postTypes = data['postTypes']

        if len(model.postTypes.all())>0:
            [model.postTypes.remove(postType) for postType in model.postTypes.all()]
        [model.postTypes.add(postType) for postType in data['postTypes']]

        if self.kwargs['type'] == 'category':
            model.parent = data['parent']

        model.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        post = Terms.objects.get(type=self.kwargs['type'],slug = self.kwargs['slug'])
        context = super().get_context_data(**kwargs)
        context['type'] = post.type
        context['id'] = post.id
        return context

#---------------------------------------[ CREATE ]
class CreatePostType(LoginRequiredMixin,FormView):
    form_class = PostTypeForm
    template_name = 'wordpress/Edit/Edit.html'
    model = Types

    def get_success_url(self):
        return reverse('wp_posts_type', kwargs={'postType': self.kwargs['postType']})

    def form_valid(self, form):
        model = Types()
        data = form.cleaned_data

        model.title = data['title']
        model.slug = data['slug']
        model.image = data['image']

        model.save()
        self.kwargs['postType'] = data['slug']
        return super().form_valid(form)

class CreatePost(LoginRequiredMixin,FormView):
    form_class = EntitiesForm
    template_name = 'wordpress/Edit/Edit.html'
    model = Entities

    def get_success_url(self):
        return reverse('wp_entity',kwargs={'type':self.kwargs['type'],'slug':self.kwargs['slug']})

    def form_valid(self, form):

        data = form.cleaned_data
        postType = PostType.query().by_slug(self.kwargs['type'])

        if Entities.objects.filter(slug = data['slug'], type__slug = self.kwargs['type'] ).exists():
            raise Exception(f"post (post type: {self.kwargs['type']}) already exists for this slug - {data['slug']}")

        post = Entities.objects.create(
            type=postType,
            title=data['title'],
            slug=data['slug'],
            content=data['content'],
            image=data['image'])
        post.save()
        [post.terms.add(term) for term in data['categories']]
        [post.terms.add(term) for term in data['tags']]
        post.save()

        self.kwargs['slug'] = post.slug
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()

        kwargs['type'] = PostType.query().by_slug(self.kwargs['type'])
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['type'] = self.kwargs['type']
        return context

class CreateTerm(LoginRequiredMixin,FormView):

    form_class = None
    template_name = 'wordpress/Edit/Edit.html'
    model = Types

    def get_form_class(self):
        if self.kwargs['type'] == 'category':
            return CategoryForm
        elif self.kwargs['type'] == 'tag':
            return TagForm

    def get_success_url(self):
        return reverse('wp_term', kwargs={'type': self.kwargs['type'], 'slug': self.kwargs['slug']})

    def form_valid(self, form):
        data = form.cleaned_data

        model = Terms(type = self.kwargs['type'],title = data['title'],slug = data['slug'],description = data['description'])
        model.save()
        self.kwargs['slug'] = model.slug
        [model.postTypes.add(postType.id) for postType in data['postTypes']]

        if self.kwargs['type'] == 'category':
            model.parent = data['parent']



        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['type'] = self.kwargs['type']
        return context

