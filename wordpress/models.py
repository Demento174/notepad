from django.db import models
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField
from mptt.models import MPTTModel, TreeForeignKey
from django.urls import reverse
from photologue.models import Photo

# Create your models here.


class Types(models.Model):
    title = models.CharField(verbose_name='Заголовок', max_length=150)
    slug = models.SlugField(verbose_name='Slug', max_length=150)
    image = models.ForeignKey(Photo, related_name='type',verbose_name='Изображение',null=True,blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.slug

    def get_absolute_url(self):

        parameters = {
            'postType':self.slug
        }

        return reverse('wp_posts_type',kwargs=parameters)

    def get_absolute_url_edit(self):

        parameters = {
            'postType':self.slug
        }

        return reverse('wp_posts_type_edit',kwargs=parameters)

    def get_absolute_url_create():

        return reverse('wp_posts_type_create')

    class Meta:
        verbose_name = 'Тип записи'
        verbose_name_plural = 'Типы записей'
        ordering = ['title']

class Entities(models.Model):
    type = models.ForeignKey(Types,related_name='entities_type', verbose_name='Тип записи', on_delete=models.CASCADE)
    title = models.CharField(verbose_name='Заголовок', max_length=150)
    slug = models.SlugField(verbose_name='Slug', max_length=150)
    content = RichTextUploadingField(config_name='default', verbose_name='Контент', blank=True, null=True)
    terms = models.ManyToManyField('Terms',related_name='entities_terms',verbose_name='Категории,теги')
    image = models.ForeignKey(Photo, related_name='entities', verbose_name='Изображение', null=True, blank=True,
                              on_delete=models.SET_NULL)
    created_at = models.DateTimeField(verbose_name='Дата создания', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='Дата последнего изменения', auto_now=True)

    def __str__(self):
        return f'{self.type.title} : {self.title}'

    def get_absolute_url(self):
        parameters = {
            'type':self.type.slug,
            'slug':self.slug
        }

        return reverse('wp_entity',kwargs=parameters)

    def get_absolute_url_edit(self):
        parameters = {
            'type':self.type.slug,
            'slug':self.slug
        }

        return reverse('wp_entity_edit',kwargs=parameters)

    @staticmethod
    def get_absolute_url_create(type):
        parameters = {
            'type':type,
        }
        return reverse('wp_entity_create',kwargs=parameters)

    class Meta:
        verbose_name = 'Запись'
        verbose_name_plural = 'Записи'
        ordering = ['title']

class Terms(MPTTModel):
    TaxonomiesTypes = [
        ('category', 'category'),
        ('tag', 'tag'),
    ]

    type = models.CharField(max_length=8, verbose_name='Тип таксономии', choices=TaxonomiesTypes, default='category')
    title = models.CharField(verbose_name='Заголовок', max_length=150)
    slug = models.SlugField(verbose_name='Slug', max_length=150)
    description = models.TextField(verbose_name='Описание', blank=True, null=True)
    postTypes = models.ManyToManyField(Types,related_name='terms_types', blank=True)
    parent = TreeForeignKey('self', on_delete=models.SET_NULL, related_name='children', blank=True, null=True)
    fields = models.ManyToManyField('Fields', related_name='terms_fields', blank=True)
    image = models.ForeignKey(Photo, related_name='terms', verbose_name='Изображение', null=True, blank=True,
                              on_delete=models.SET_NULL)
    created_at = models.DateTimeField(verbose_name='Дата создания', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='Дата последнего изменения', auto_now=True)

    def get_absolute_url(self):
        parameters = {
            'type':self.type,
            'slug': self.slug
        }
        return reverse('wp_term',kwargs=parameters)

    def get_absolute_url_edit(self):
        parameters = {
            'type': self.type,
            'slug': self.slug
        }
        return reverse('wp_term_edit', kwargs=parameters)

    @staticmethod
    def get_absolute_url_create(type):
        parameters = {
            'type': type,
        }
        return reverse('wp_term_create', kwargs=parameters)

    def __str__(self):
        return f'{self.type} : {self.title}'

    class Meta:
        verbose_name = 'Таксономия'
        verbose_name_plural = 'Таксономии'
        ordering = ['title']

    class MPTTMeta:
        verbose_name = 'Таксономия'
        verbose_name_plural = 'Таксономии'
        ordering = ['title']

class Fields(models.Model):
    FieldsTypes = [
        ('int', 'Числовой'),
        ('string', 'Строковый'),
        ('wysiwyg', 'Редактор'),
        ('textArea', 'Текстовое поле'),
        ('text', 'текст'),
        ('link', 'Ссылка'),
    ]

    type = models.CharField(max_length=150, verbose_name='Тип поля', choices=FieldsTypes, default='int')
    title = models.CharField(verbose_name='Заголовок', max_length=150)
    selector = models.CharField(verbose_name='Селектор', max_length=150)

    entityType = models.ForeignKey(Types, verbose_name='Тип записи',related_name='fields_type',blank=True, null=True, on_delete=models.CASCADE)
    termType = TreeForeignKey(Terms, verbose_name='Тип Таксономии', related_name='fields_term',blank=True, null=True, on_delete=models.CASCADE)
    def __str__(self):
        return f'{self.title} <{self.type}>'

    class Meta:
        verbose_name = 'Поле'
        verbose_name_plural = 'Поля'
        ordering = ['title', 'type']

class FieldsValues(models.Model):
    value = models.JSONField(verbose_name='Значение', blank=True,null=True)
    key = models.SlugField(verbose_name='Ключ-внешний ID', max_length=150)
    field = models.ForeignKey(Fields, verbose_name='Поле',related_name='fieldsValues_field', on_delete=models.CASCADE)
    post = models.ForeignKey(Types, verbose_name='Запись',related_name='fieldsValues_post', on_delete=models.CASCADE, blank=True, null=True)
    term = TreeForeignKey(Terms, verbose_name='Таксономия',related_name='fieldsValues_term', on_delete=models.CASCADE, blank=True, null=True)
    created_at = models.DateTimeField(verbose_name='Дата создания', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='Дата последнего изменения', auto_now=True)

    def save(self,*args, **kwargs):
        self.key=f'{self.field.selector}_{self.pk}'
        super().save(*args,**kwargs)


    def __str__(self):
        return f'Значение {self.field.title}'

    class Meta:
        verbose_name = 'Поле'
        verbose_name_plural = 'Поля'
        ordering = ['field', 'post', 'term']