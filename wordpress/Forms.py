from django import forms
from ckeditor.widgets import CKEditorWidget
from .models import Entities,Types, Terms
from photologue.models import Photo
from var_dump import var_dump
from .Entities.Taxonomies import Tag,Category
from .Entities.Posts import PostType
from mptt.fields import TreeNodeChoiceField
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth.models import User

import re


class PostTypeForm(forms.Form):
    # type = forms.ModelChoiceField(label='Тип записи', queryset=Types.objects.all(),widget=forms.HiddenInput())
    title = forms.CharField(label='Заголовок',max_length=150,  widget=forms.TextInput(attrs={'class':'form-control'}))
    slug = forms.SlugField(label='Slug', max_length=150, widget=forms.TextInput(attrs={'class':'form-control'}))
    image = forms.ImageField(label='Изображение', required=False,
                              widget=forms.FileInput(attrs={'class': 'form-control'}))

class EntitiesForm(forms.Form):
    type = None
    def __init__(self, *args, **kwargs):
        self.type = kwargs.pop('type', None)  # THIS PARAMETER
        super().__init__(*args, **kwargs)
        self.fields['tags'] = forms.ModelMultipleChoiceField(label='Теги',
                                                            queryset=Terms.objects.filter(type='tag',postTypes__in=[self.type.id]),
                                                            required=False,
                                                            widget=forms.CheckboxSelectMultiple())
        self.fields['categories'] = forms.ModelMultipleChoiceField(label='Категории',
                                                            queryset=Terms.objects.filter(type='category',postTypes__in=[self.type.id]),
                                                            required=False,
                                                            widget=forms.CheckboxSelectMultiple())


    title = forms.CharField(label='Заголовок',max_length=150,  widget=forms.TextInput(attrs={'class':'form-control'}))
    slug = forms.SlugField(label='Slug', max_length=150, widget=forms.TextInput(attrs={'class':'form-control'}))
    content = forms.CharField(label='Контент', required=False, widget=CKEditorWidget(attrs={'class':'form-control','rows':5}))
    image = forms.ImageField(label='Изображение', required=False,
                              widget=forms.FileInput(attrs={'class': 'form-control'}))

class CategoryForm(forms.Form):

    title = forms.CharField(label='Заголовок',max_length=150,  widget=forms.TextInput(attrs={'class':'form-control'}))
    slug = forms.SlugField(label='Slug', max_length=150, widget=forms.TextInput(attrs={'class':'form-control'}))
    image = forms.ImageField(label='Изображение', required=False,
                              widget=forms.FileInput(attrs={'class': 'form-control'}))
    description = forms.CharField(label='Описание', required=False, widget=CKEditorWidget(attrs={'class':'form-control','rows':5}))
    postTypes = forms.ModelMultipleChoiceField(label='Типы записей', queryset=Types.objects.all(),widget=forms.CheckboxSelectMultiple())
    parent = TreeNodeChoiceField(queryset=Terms.objects.filter(type='category'), required=False, widget=forms.Select(attrs={'class':'form-control'}))

class TagForm(forms.Form):

    title = forms.CharField(label='Заголовок',max_length=150,  widget=forms.TextInput(attrs={'class':'form-control'}))
    slug = forms.SlugField(label='Slug', max_length=150, widget=forms.TextInput(attrs={'class':'form-control'}))
    image = forms.ImageField(label='Изображение', required=False,
                              widget=forms.FileInput(attrs={'class': 'form-control'}))
    description = forms.CharField(label='Описание', required=False, widget=CKEditorWidget(attrs={'class':'form-control','rows':5}))
    postTypes = forms.ModelMultipleChoiceField(label='Типы записей', queryset=Types.objects.all(),widget=forms.CheckboxSelectMultiple())

